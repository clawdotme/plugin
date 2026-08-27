# Claw Me publishing reference

Claw Me exposes publishing through the authenticated Streamable HTTP MCP endpoint at `https://claw.me/api/v1/mcp`.

It also exposes a deliberately narrow anonymous REST flow for disposable static previews. That flow is the exception to account authorization: use it only when the user explicitly asks to publish or says “claw me that,” has no Claw Me credential, and accepts a public-by-link preview that expires within 24 hours.

## Required scope

Use `artifacts:write` for `artifact_publish`. Use `artifacts:read` for `artifact_list`. An owner may instead issue the broader `claw-me:mcp` scope.

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
      "checksum_sha256": "<sha256>"
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

Anonymous previews support static files only, are unindexed, and accept at most 50 files, 50 MB total, and 25 MB per file. Creation is limited to three previews per source per hour. Uploaded HTML receives a service-controlled footer that says it is powered by claw.me and expires within 24 hours. The URL returns 404 at the original 24-hour expiry even if it was finalized later. If the agent cannot perform presigned uploads, direct the user to `https://claw.me/preview` for the equivalent browser flow.
