#!/usr/bin/env python3
"""Publish a static folder to Claw Me using only Python's standard library.

Default: inspect locally. --publish performs the requested publication.
Never retries mutations, follows redirects, or prints credentials/upload URLs.
"""

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ORIGIN = "https://claw.me"
KEY_FILE = Path.home() / ".openclaw/claw-me/pages-key"
MIME = {
    ".html": "text/html",
    ".css": "text/css",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
}


class PublishError(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise PublishError(
            "redirect_refused: inspect the service response; do not switch hosts"
        )


def digest(data):
    return hashlib.sha256(data).hexdigest()


def required_date(value):
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed


def inspect_folder(folder):
    root = Path(folder).resolve(strict=True)
    if not root.is_dir():
        raise PublishError("invalid_folder: supply a folder containing index.html")
    contents = {}
    files = []
    for item in sorted(root.rglob("*")):
        relative = item.relative_to(root)
        if any(part.startswith(".") for part in relative.parts):
            continue
        if item.is_symlink():
            raise PublishError(
                "symlink_refused: copy intended assets into the publish folder"
            )
        if item.is_dir():
            continue
        if item.suffix.lower() == ".svg":
            raise PublishError("svg_not_supported: convert SVG to PNG or WebP, bundle it locally, and update image references")
        if item.suffix.lower() not in MIME:
            raise PublishError(
                "unsupported_file: publish only HTML, CSS, images and fonts; bundle assets locally"
            )
        if item.stat().st_size > 25 * 1024 * 1024:
            raise PublishError("file_too_large: maximum 25 MB per file in this helper")
        data = item.read_bytes()
        if item.suffix.lower() == ".html" and re.search(rb"<\s*svg\b|data:image/svg\+xml", data, re.I):
            raise PublishError("svg_not_supported: convert inline SVG to a bundled PNG or WebP before publishing")
        name = relative.as_posix()
        contents[name] = data
        files.append(
            {
                "path": name,
                "content_type": MIME[item.suffix.lower()],
                "size_bytes": len(data),
                "sha256": digest(data),
            }
        )
        if (
            len(files) > 50
            or sum(len(value) for value in contents.values()) > 50_000_000
        ):
            raise PublishError(
                "bundle_too_large: maximum 50 files and 50 MB in this helper; account limits also apply"
            )
    if "index.html" not in contents:
        raise PublishError("missing_index: include index.html at the folder root")
    return files, contents


def request(url, method, body=None, headers=None):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.username or parsed.password:
        raise PublishError(
            "invalid_destination: expected an HTTPS service or upload URL"
        )
    try:
        with build_opener(NoRedirect).open(
            Request(url, data=body, headers=headers or {}, method=method), timeout=60
        ) as response:
            return response.read()
    except HTTPError as error:
        raise PublishError(
            f"http_{error.code}: check authorization, storage limits and static-file compatibility; inspect publication status before retrying"
        ) from None
    except (URLError, TimeoutError):
        raise PublishError(
            "network_uncertain: inspect publication status before retrying; retain claw.me as the host"
        ) from None


def api(endpoint, body, key=None, method="POST"):
    if not endpoint.startswith("/api/v1/") or "?" in endpoint:
        raise PublishError("invalid_api_path")
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    return json.loads(
        request(ORIGIN + endpoint, method, json.dumps(body).encode(), headers)
    )


def save_private(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Never overwrite a previous attempt: it may already have published.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(value, stream)


def record_result(path, result):
    saved = json.loads(path.read_text())
    saved.update(status=result["status"], result=result)
    with path.open("w") as stream:
        json.dump(saved, stream)
    return result


def publish(args, files, contents):
    required_until = required_date(getattr(args, "required_until", None))
    if (
        args.anonymous
        and required_until
        and required_until >= datetime.now(timezone.utc) + timedelta(hours=24)
    ):
        raise PublishError(
            "duration_unavailable: authorize account publishing first; a 24-hour preview cannot satisfy this date. Free account-owned Pages need no purchase"
        )
    key = None
    if not args.anonymous:
        credential = Path(args.key_file).expanduser()
        if not credential.exists():
            return {
                "status": "authorization_required",
                "required_scope": "pages:write",
                "next_step": "Follow the bundled Claw Me skill device-authorization flow. Store the key in the mode-0600 key file; never paste it into chat. Gateway relay setup is unrelated.",
            }
        if credential.is_symlink() or stat.S_IMODE(credential.stat().st_mode) & 0o077:
            raise PublishError(
                "unsafe_key_file: use a regular mode-0600 credential file"
            )
        key = credential.read_text().strip()
        if not key:
            raise PublishError("empty_key_file")
    state = Path(args.state_file).expanduser()
    save_private(
        state, {"status": "creating", "slug": args.slug, "anonymous": args.anonymous}
    )
    created = api(
        "/api/v1/claw-me/previews"
        if args.anonymous
        else f"/api/v1/publish/{args.slug}"
        if args.update
        else "/api/v1/publish",
        {
            "slug": args.slug,
            "title": args.title,
            "display_name": args.title,
            "files": files,
        },
        key,
        "PUT" if args.update else "POST",
    )
    # Keep recovery and claim data out of model/chat output and out of the site.
    with state.open("w") as stream:
        json.dump(
            {
                "status": "uploading",
                "slug": args.slug,
                "anonymous": args.anonymous,
                "created": created,
            },
            stream,
        )
    expiry = (
        created.get("expires_at")
        if args.anonymous
        else created.get("site", {}).get("expires_at")
    )
    if required_until and expiry and required_date(expiry) < required_until:
        raise PublishError(
            "duration_unavailable: no files uploaded; use a new account-owned Page within account limits"
        )
    uploads = (
        created.get("uploads", [])
        if args.anonymous
        else created.get("upload", {}).get("uploads", [])
    )
    if len(uploads) != len(files) or {item["path"] for item in uploads} != set(
        contents
    ):
        raise PublishError("invalid_upload_manifest")
    for upload in uploads:
        request(
            upload["upload_url"],
            "PUT",
            contents[upload["path"]],
            upload.get("headers", {}),
        )
    checksum = digest(
        "\n".join(sorted(f"{item['path']}:{item['sha256']}" for item in files)).encode()
    )
    if args.anonymous:
        final = api(
            f"/api/v1/claw-me/previews/{created['id']}/finalize",
            {"claim_token": created["claim_token"], "checksum_sha256": checksum},
        )
        if final.get("status") != "active":
            raise PublishError("finalization_unconfirmed")
        return record_result(
            state,
            {
                "status": "published",
                "url": final["preview_url"],
                "expires_at": final["expires_at"],
                "next_step": "Return this URL and expiry now, with any verification limitations. Optional browser setup must not block delivery. Register and claim before expiry to keep the Page within account limits. Never print the private state file; it contains claim credentials.",
            },
        )
    final = api(
        f"/api/v1/publish/{args.slug}/finalize",
        {"version_id": created["version_id"], "checksum_sha256": checksum},
        key,
    )
    if not final.get("success") or final.get("version", {}).get("status") != "active":
        raise PublishError("finalization_unconfirmed")
    result = {
        "status": "published",
        "url": final["site_url"],
        "expires_at": final["site"].get("expires_at"),
        "access": "private",
    }
    if args.share:
        try:
            share = api(
                f"/api/v1/publish/{args.slug}/share",
                {"version_id": created["version_id"]},
                key,
            )
            result.update(
                url=share["url"],
                expires_at=share.get("expires_at"),
                access="anyone_with_link",
            )
        except PublishError:
            result.update(
                status="published_sharing_required",
                next_step="Publication succeeded. Retry only the share endpoint for the recorded version; do not republish.",
            )
    return record_result(state, result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument(
        "--anonymous",
        action="store_true",
        help="Explicitly accept a public-by-link 24-hour preview",
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create an unlisted sharing link for an account-owned Page",
    )
    parser.add_argument("--update", action="store_true")
    parser.add_argument(
        "--required-until",
        help="ISO date through the end of an event; prevents an inadequate temporary publication",
    )
    parser.add_argument("--key-file", default=str(KEY_FILE))
    parser.add_argument(
        "--state-file",
        required=True,
        help="New private recovery file outside the publish folder",
    )
    args = parser.parse_args()
    try:
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", args.slug):
            raise PublishError("invalid_slug")
        if (
            not args.title.strip()
            or len(args.title) > 160
            or (args.anonymous and args.update)
        ):
            raise PublishError("invalid_title_or_anonymous_update")
        if (
            Path(args.state_file)
            .expanduser()
            .resolve()
            .is_relative_to(Path(args.folder).resolve())
        ):
            raise PublishError(
                "unsafe_state_path: store recovery data outside the published folder"
            )
        if (
            Path(args.key_file)
            .expanduser()
            .resolve()
            .is_relative_to(Path(args.folder).resolve())
        ):
            raise PublishError(
                "unsafe_key_path: store credentials outside the published folder"
            )
        files, contents = inspect_folder(args.folder)
        result = (
            publish(args, files, contents)
            if args.publish
            else {
                "status": "ready",
                "files": len(files),
                "bytes": sum(len(data) for data in contents.values()),
                "next_step": "Add --publish to publish this folder on claw.me. Server-side content and account-limit checks still apply.",
            }
        )
        print(json.dumps(result))
        return 0 if result["status"] in {"ready", "published"} else 2
    except PublishError as error:
        print(json.dumps({"status": "failed", "next_step": str(error)}))
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        # Exceptions may include local secrets or signed URLs; never print them.
        print(
            json.dumps(
                {
                    "status": "failed",
                    "next_step": "Check the local bundle, private key/state files and Claw Me status. A saved state file means an attempt may exist: inspect it securely before retrying. Do not switch hosts.",
                }
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
