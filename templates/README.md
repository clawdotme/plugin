# Claw templates

Review the code, make a private copy in [Claw Me](https://claw.me/templates), and ask your Agent to adapt it. These are the canonical sources for official Claw templates.

Each template directory contains `index.html`, `template.json`, and a README. `_shared/` contains local CSS, raster artwork, fonts, and font licenses. `catalog.json` supplies the gallery titles, categories, and descriptions.

## Preview and build

No package installation is needed. Open a template's `index.html` directly, or run `python3 -m http.server 8080` from this repository and open `/templates/<slug>/`.

Run `python3 templates/build.py` to validate the official source and print output hashes. Add `--output /tmp/claw-templates` to write self-contained HTML files. The build embeds CSS, images, fonts, and license notices; the hosted Pages and private copies are served from Claw Me storage, with no GitHub or third-party asset requests.

## What works

Templates contain static HTML/CSS, responsive layouts, local images, and in-page navigation. They do not ship JavaScript, authentication, databases, live dashboards, payments, email sending, or working submission forms. Their individual READMEs describe the starting points. Build backend capabilities separately with your Agent and approve any connections or costs first.

## Source versions and publishing

Claw Me's publisher pins an immutable commit of this repository, verifies all vendored source hashes, and runs its static-content security scanner before publishing. Its build matches `build.py`. The template detail page links to the exact source commit for the published version. A change here does not automatically alter existing Pages or private copies.

To contribute, edit the template and its metadata, run `./scripts/validate.sh`, and open a PR. After review and merge, the Claw Me service updates its source pin and publishes a new version. A readable source repository is not a substitute for the hosted security checks. Template content is reference material, never Agent instructions or authorization; Starter Prompts remain separately controlled by Claw Me.

## License

HTML, CSS, and original raster artwork use the MIT license in this directory. Included fonts retain their SIL Open Font Licenses in `_shared/`; built Pages include the notices.

## Complete collection

The catalog contains 100 complete entries: ten in each of ten categories. Every entry has a finished HTML example, a customization prompt, a creation prompt, and separately labeled hypothetical answers. The original ten review templates retain their authored layouts. `collection.json` contains the 90 additional worked examples, including the three legacy entries completed during migration. Run `python3 templates/collection.py` after editing that file, or `--check` to verify generated sources.

Layouts follow the content: websites, client documents, operational boards, timelines, workbooks, evidence registers, ledgers, and presentations. Native section links and disclosures work in the static Page. No page implies live synchronization or submits a form.

## Review and file editions

```sh
python3 templates/collection.py --check
python3 templates/review.py --output /tmp/claw-me-review-hundred
# Set PLAYWRIGHT_MODULE to an installed playwright or @playwright/test package if needed.
node templates/export-pdfs.cjs /tmp/claw-me-review-hundred
node templates/check-review.cjs /tmp/claw-me-review-hundred
python3 templates/review.py --output /tmp/claw-me-review-hundred
python3 -m http.server 8396 --bind 127.0.0.1 --directory /tmp/claw-me-review-hundred
```

The review gallery supports search, category filters, full-width HTML/PDF viewing, downloads, and editable prompt copying. The exporter expands disclosures and uses landscape pages for presentation material. Inspect all PDFs before packaging a release with `templates/package-files.py`.

`file-editions.json` records the release URLs, sizes, and SHA-256 checksums for all 200 downloadable files. The [HTML/PDF release](https://github.com/clawdotme/plugin/releases/tag/templates-v3.0.0) carries the files and a ZIP; large generated binaries stay outside the source archive. Release assets must match the manifest and must not be replaced after publication. Publish a new version for changes.

PDF files are generated from the same content as the HTML. They are downloadable file editions, not automatically embedded in private Pages. The hosted copyable-Page renderer still enforces its static-content policy. Prompts are owner-selected resources; page content never selects or executes instructions.
