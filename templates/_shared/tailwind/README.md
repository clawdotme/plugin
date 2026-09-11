# Claw Me Tailwind starter

Use the parent portal.css theme tokens and bundled Archivo/Bitter fonts. Author component rules in input.css with Tailwind 3.4.19 @apply, scoped under your template body class. Custom layout is welcome; retain typography, colors, and accessible semantics by default.

Compile with Tailwind CLI 3.4.19:

```sh
tailwindcss -c templates/_shared/tailwind/tailwind.config.cjs -i templates/_shared/tailwind/input.css -o /tmp/claw-components.css
python3 templates/_shared/tailwind/update.py /tmp/claw-components.css
python3 templates/build.py --output /tmp/claw-templates
```

update.py replaces only the generated section of portal.css. Commit input and compiled CSS together. No browser runtime, remote fonts, or CDN is required. Recompile whenever changing Tailwind rules. The compiled output deliberately uses scoped semantic selectors compatible with the static publisher.
