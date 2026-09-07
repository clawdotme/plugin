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
