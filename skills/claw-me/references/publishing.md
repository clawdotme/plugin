# Claw Me publishing reference

Claw Me exposes publishing through the authenticated Streamable HTTP MCP endpoint at `https://claw.me/api/v1/mcp`.

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
