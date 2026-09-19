## Publishing skill and preflight

Install the official Claw Me skill and its publish.py helper from https://claw.me/plugins. It checks bundles locally and handles exact hashes, uploads, finalization, and private recovery state. Direct REST remains supported.

SVG files, inline <svg>, and SVG data URLs are unsupported. Convert artwork to PNG or WebP using a trusted local converter, bundle the result, and replace HTML/CSS references. Renaming a file is not conversion. The server repeats safety validation at finalization.

A 422 at create concerns the request manifest: HTML has not been uploaded yet. Inspect the JSON error field location and message (curl -f can hide that body). Check byte counts, hash format, paths, and the endpoint schema. A 422 at finalize may identify unsafe HTML or an upload mismatch. Never expose claim tokens or presigned URLs while diagnosing errors.

If the authorized account needs an alias, link directly to https://claw.me/getting-started?step=address and resume the same Agent after saving. Do not request another authorization. Pages, Drive, Agent context, and Activity default to enabled; keep owner-only incoming email and the sharing switch until the owner explicitly changes them.

# Claw Me publishing reference

Claw Me exposes publishing through the authenticated Streamable HTTP MCP endpoint at `https://claw.me/api/v1/mcp`.

It also exposes a deliberately narrow anonymous REST flow for disposable static previews. That flow bypasses account authorization and existing credentials: use it only when the user explicitly asks to publish or says “claw me that,” accepts a public-by-link preview that expires within 24 hours.

## Use your own account

“Account owner” means you, the user of a Claw Me account, not the owner of the claw.me domain. You do not need DNS access or permission from the service operator to host a Page.

For a durable Page, reuse your existing account. If you have not signed up, create an account at https://claw.me/register, accept the terms, and verify your email before starting a short-lived Agent approval request. Existing users can sign in at https://claw.me/login. Account feature setup can then continue with the Agent where supported. Do not ask users to forward approval codes to whoever owns claw.me. If account status is unknown, explain signup or sign-in first; do not infer it from an email address.

Anonymous 24-hour previews require no account, sign-in, or pairing. An authorization code is not an account or a sign-in link. If a request was already created, complete signup and return to its approval link; create a new request only after expiry when still needed. Preserve private request state.

## Required scope

Request `pages:write` for publishing and link sharing, and `pages:read` only when listing Pages is needed. The MCP tools accept these canonical scopes; `artifacts:write` and `artifacts:read` are legacy aliases, not additional grants. Do not request umbrella scopes.

## Publish a local folder

Prefer the bundled standard-library Python helper when the client can run commands and the completed website is already in a folder. It hashes exact bytes, uploads assets, confirms finalization, and emits JSON. It never installs a hosting service or starts a local server.

```sh
python scripts/publish.py ./site --slug emba-golf --title "EMBA golf tournament" --state-file ~/.claw-me/emba-golf-attempt.json
```

This first call is a local preflight. Add `--publish --share` when the user requested publication and a link for friends. It reads the mode-0600 Pages key from `~/.openclaw/claw-me/pages-key`, or an explicitly supplied `--key-file`. Missing authorization returns `authorization_required`: follow the device flow in SKILL.md, not Gateway relay setup.

Use `--anonymous --publish` only when a public-by-link preview expiring after 24 hours meets the user's request. For an upcoming event, unless the user explicitly requests a disposable preview irrespective of its date, pass `--required-until` with an ISO date through the end of the event. This blocks an anonymous preview whose lifetime is inadequate. Use account-owned publishing for future events beyond 24 hours; Free does not require a purchase. Do not publish a temporary preview first and call that complete. Keep the state file outside the site folder. It contains private recovery/claim data and must never be pasted into chat, committed, or uploaded. Use a fresh state filename for each intentional new attempt. An existing file stops execution before another create: inspect the prior attempt securely instead of deleting the file and retrying blindly. `--update` explicitly updates an account-owned slug.

The helper accepts up to 50 files and 50 MB of static HTML/CSS, bundled images, and fonts; server-side content checks and existing account quotas still apply. It refuses symlinks, JavaScript, and unsupported file types, and skips hidden files. A `published_sharing_required` result means the site exists but sharing needs recovery; retry only the share endpoint for the recorded version.

## Publish contract

Call `artifact_publish` with:

```json
{
  "slug": "launch-notes",
  "title": "Launch notes",
  "files": [
    {
      "path": "index.html",
      "content_type": "text/html",
      "size_bytes": 1240,
      "sha256": "<sha256>"
    }
  ]
}
```

The result creates or reuses a private site and returns an immutable version, presigned upload targets, and a finalize path. Upload exactly the declared bytes, then call the finalize path. A version does not become current until finalization succeeds.

## Access

- `private`: account owner and approved account grants only.
- `link`: unguessable, optionally expiring share token.
- `password`: password-protected grant.
- `account`: explicit account allowlist.
- `public`: only after the user explicitly requests it.

Never include credentials or private environment values in a Page bundle. Use scoped server-side variables or proxy routes when a Page needs a secret-backed operation.

## Anonymous static preview contract

Create the upload session without an Authorization header:

```http
POST https://claw.me/api/v1/claw-me/previews
Content-Type: application/json

{
  "title": "Hello World",
  "files": [
    {
      "path": "index.html",
      "content_type": "text/html",
      "size_bytes": 125,
      "sha256": "<sha256-of-exact-file-bytes>"
    }
  ]
}
```

Upload each file's exact bytes with `PUT` to its returned `upload_url` and include every returned header. Then finalize:

```http
POST https://claw.me/api/v1/claw-me/previews/{id}/finalize
Content-Type: application/json

{
  "claim_token": "<one-time-token-from-create>",
  "checksum_sha256": "<sha256-of-sorted-path:file-sha256-lines>"
}
```

The manifest checksum input is the newline-joined, lexicographically sorted list of `path:file_sha256` values encoded as UTF-8. Return the `preview_url` and `expires_at` from the response. Never return the claim token, object keys, or presigned URLs to the user.

Anonymous previews support static files only, are unindexed, and accept at most 50 files, 50 MB total, and 25 MB per file. Creation is limited to three previews per source per hour. Uploaded HTML receives a service-controlled primary-green banner with a live expiry countdown and a link to register and claim the preview within account limits. The URL returns 404 at the original 24-hour expiry even if it was finalized later. If the agent cannot perform presigned uploads, direct the user to `https://claw.me/preview` for the equivalent browser flow.

## Complete a website with REST

1. POST `/api/v1/publish` with `slug`, `display_name`, and `files` (`path`, `content_type`, `size_bytes`, `sha256`). To update an existing slug, PUT `/api/v1/publish/{slug}` instead.
2. Inspect `site.expires_at` before uploading. If the Page expires before the requested event, create a new account-owned Page within account limits first.
3. PUT each file's exact bytes to `upload.uploads[].upload_url` with its returned headers. Never attach the API bearer to storage uploads or follow redirects with it.
4. POST `/api/v1/publish/{slug}/finalize` with `version_id` and `checksum_sha256`. Compute the manifest checksum as SHA-256 of UTF-8 newline-joined, sorted `path:file-sha256` lines, with no trailing newline. Finalization validates every uploaded asset; creation alone is not publication.
5. When the user requested a shareable link, POST `/api/v1/publish/{slug}/share` with that finalized `version_id` and optional ISO `expires_at`. This uses `pages:write` and creates an unlisted, version-bound anyone-with-link URL without making the Page publicly indexed. A stale version returns 409: inspect the new version before sharing it. A new link replaces the previous link. Return `url`, `grant_type`, and `expires_at`; do not send the link to friends unless separately asked.

After a network timeout, inspect the existing Page before retrying a create or finalize. Do not claim success or switch hosting providers because an API call failed.

## Supported embedded map

Pages accept only OpenStreetMap's HTTPS export embed, with a bounding box, a marker, and `layer=mapnik`. Verify coordinates from the venue or a map provider; the numbers below are illustrative. Longitude comes first in `bbox`; latitude comes first in `marker`.

```html
<iframe title="Venue map" width="100%" height="360" loading="lazy"
  sandbox="allow-scripts allow-same-origin" referrerpolicy="no-referrer"
  src="https://www.openstreetmap.org/export/embed.html?bbox=4.5,51.5,4.8,51.7&amp;marker=51.6,4.6&amp;layer=mapnik"></iframe>
<a class="button" href="https://www.google.com/maps/dir/?api=1&amp;destination=51.6%2C4.6">Driving directions</a>
```

Do not use Google Maps iframes, `srcdoc`, event handlers, extra sandbox permissions, or API keys. The embedded map loads from OpenStreetMap in the visitor's browser; other images, fonts, and styles must be bundled locally. Use a styled anchor rather than a form or `<button>` for directions. If finalization rejects the supported frame on an older deployment, retain the site and explain the limitation; offer a bundled static map image and directions link instead of switching hosts.

In OpenClaw, use `claw_me_publish_website` with `anonymous: true` for an explicitly requested anonymous preview. This bypasses the stored Pages key even when one exists. Omit `update`, use `access: "link"` or omit access, and do not request private access. If an older installed tool has no `anonymous` parameter, use the bundled Python helper with `--anonymous`; do not call the authenticated native tool.

## Complete and report safely

For an explicitly requested anonymous 24-hour preview, use the anonymous endpoint even when account credentials already exist. Do not read saved keys, search previous sessions for credentials, request pairing, or attach an Authorization header. Use the current documented contract rather than guessing an endpoint.

Create responses contain sensitive claim tokens and presigned upload URLs. Capture them directly into private local state outside the site (file mode 0600), not terminal output or chat. Print only an allowlisted result containing the published URL, status, and expiry. Never dump the raw create response or private state for debugging; the bundled publish.py helper already separates private state from its JSON output.

After finalization succeeds, return the published URL and expiry. Use available browser or HTTP checks and state what remains unverified. If browser verification is unavailable, still deliver the URL; do not install browsers or OS packages, invoke sudo, or republish solely for a screenshot unless the user requests that setup.
