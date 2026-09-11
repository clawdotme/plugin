# Claw Me publishing reference

Claw Me exposes publishing through the authenticated Streamable HTTP MCP endpoint at `https://claw.me/api/v1/mcp`.

It also exposes a deliberately narrow anonymous REST flow for disposable static previews. That flow is the exception to account authorization: use it only when the user explicitly asks to publish or says “claw me that,” has no Claw Me credential, and accepts a public-by-link preview that expires within 24 hours.

## Required scope

Request `pages:write` for publishing and link sharing, and `pages:read` only when listing Pages is needed. The MCP tools accept these canonical scopes; `artifacts:write` and `artifacts:read` are legacy aliases, not additional grants. Do not request umbrella scopes.

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

Anonymous previews support static files only, are unindexed, and accept at most 50 files, 50 MB total, and 25 MB per file. Creation is limited to three previews per source per hour. Uploaded HTML receives a service-controlled primary-green banner with a live expiry countdown and a link to configure a paid plan and add-ons. The URL returns 404 at the original 24-hour expiry even if it was finalized later. If the agent cannot perform presigned uploads, direct the user to `https://claw.me/preview` for the equivalent browser flow.

## Complete a website with REST

1. POST `/api/v1/publish` with `slug`, `display_name`, and `files` (`path`, `content_type`, `size_bytes`, `sha256`). To update an existing slug, PUT `/api/v1/publish/{slug}` instead.
2. Inspect `site.expires_at` before uploading. If the Page expires before the requested event, resolve the owner's durable plan choice first.
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
