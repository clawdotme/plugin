#!/usr/bin/env python3
"""Build a local review gallery for the ten selected template-and-prompt pairs."""
import argparse
import html
import json
import re
from pathlib import Path
from build import ROOT, build


def render(output):
    review = json.loads((ROOT / 'review-set.json').read_text())
    catalog = {item['slug']: item for item in json.loads((ROOT / 'catalog.json').read_text())}
    assert len(review['slugs']) == 10 and len(set(review['slugs'])) == 10
    assert len({catalog[slug]['category'] for slug in review['slugs']}) == 10
    output.mkdir(parents=True, exist_ok=True)
    css = re.search(r'<style>(.*?)</style>', build(review['slugs'][0]).decode(), re.S).group(1)
    e = html.escape
    def shell(title, body):
        return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{css}</style></head><body class="review-board">{body}</body></html>'
    cards = []
    for number, slug in enumerate(review['slugs'], 1):
        entry = catalog[slug]
        brief = json.loads((ROOT / slug / 'creation-brief.json').read_text())
        (output / f'{slug}.html').write_bytes(build(slug))
        screenshot = f'screenshots/{slug}-1440.png'
        preview = (f'<img src="{screenshot}" alt="Preview: {e(entry["title"])}">'
                   if (output / screenshot).is_file() else
                   f'<iframe loading="lazy" sandbox="" title="Preview: {e(entry["title"])}" src="{slug}.html"></iframe>')
        cards.append(f'<article class="card"><p class="eyebrow">{number:02d} / {e(entry["category"].replace("-", " "))}</p>{preview}<h2><a href="{slug}-review.html">{e(entry["title"])}</a></h2><p>{e(entry["description"])}</p><a class="pill" href="{slug}-review.html">Review template &amp; prompts →</a></article>')
        prompts = []
        for key, title in [('customizationPrompt','Start with this template'),('creationPrompt','Build your own version')]:
            prompts.append(f'<details><summary>{title}</summary><label>Edit the prompt<textarea aria-label="{title} prompt">{e(brief[key])}</textarea></label><button type="button" data-copy>Copy prompt</button><span role="status"></span></details>')
        answers = ''.join(f'<dt>{e(key)}</dt><dd>{e(value)}</dd>' for key,value in brief['exampleAnswers'].items())
        body = f'''<header><a href="index.html">← All ten templates</a><strong>{e(entry['title'])}</strong><a href="{slug}.html" target="_blank">Open full page</a></header><main class="review-detail"><section><nav aria-label="Preview width"><button type="button" data-width="100%" aria-pressed="true">Desktop</button><button type="button" data-width="390px" aria-pressed="false">Mobile</button></nav><iframe class="review-preview" sandbox="" title="{e(entry['title'])} preview" src="{slug}.html"></iframe></section><aside><p class="eyebrow">{e(entry['category'].replace('-', ' '))}</p><h1>{e(entry['title'])}</h1><p>{e(entry['description'])}</p><p class="note">Review edition. The page is static; the prompts can be edited and copied here.</p>{''.join(prompts)}<details><summary>Example brief</summary><p>{e(brief['creationPromptOrigin'])}</p><dl>{answers}</dl></details></aside></main>'''
        body += '''<script>
for (const button of document.querySelectorAll('[data-copy]')) button.addEventListener('click', async () => {
 const section=button.closest('details'), text=section.querySelector('textarea'), status=section.querySelector('[role=status]');
 try {await navigator.clipboard.writeText(text.value); status.textContent='Copied';} catch {text.focus();text.select();status.textContent='Select and copy the prompt manually.';}
});
for (const button of document.querySelectorAll('[data-width]')) button.addEventListener('click', () => {
 document.querySelector('.review-preview').style.maxWidth=button.dataset.width;
 for(const other of document.querySelectorAll('[data-width]')) other.setAttribute('aria-pressed',String(other===button));
});
</script>'''
        (output / f'{slug}-review.html').write_text(shell(entry['title']+' · Review',body))
    body = '<header><strong>CLAW ME / REVIEW SET 01</strong><span class="pill">10 complete pairs · 10 categories</span></header><main><section class="intro"><p class="eyebrow">Templates &amp; Prompts</p><h1>Ten useful starting points.<br>Make each one yours.</h1><p class="lead">Review the finished page, the customization prompt, and the creation brief together. All content is illustrative. These are local review previews, not published user Pages.</p></section><div class="review-catalog">'+''.join(cards)+'</div></main><footer>Each entry includes a static template, two prompts, and its sample answers. The remaining 90 planned entries are outside this review set.</footer>'
    (output / 'index.html').write_text(shell('Templates & Prompts · Review ten',body))
    print(f'Built {len(review["slugs"])} complete review pairs in {output}')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    render(parser.parse_args().output)
