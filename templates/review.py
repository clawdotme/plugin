#!/usr/bin/env python3
"""Build a local review gallery for the selected template-and-prompt pairs."""
import argparse
import html
import json
import re
from pathlib import Path
from build import ROOT, build


def render(output):
    review = json.loads((ROOT / 'review-set.json').read_text())
    catalog = {item['slug']: item for item in json.loads((ROOT / 'catalog.json').read_text())}
    assert len(review['slugs']) == 100 and len(set(review['slugs'])) == 100
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
        preview = (f'<img loading="lazy" src="{screenshot}" alt="Preview: {e(entry["title"])}">'
                   if (output / screenshot).is_file() else
                   f'<iframe loading="lazy" sandbox="" title="Preview: {e(entry["title"])}" src="{slug}.html"></iframe>')
        cards.append(f'<article class="card" data-category="{e(entry["category"])}" data-search="{e((entry["title"]+" "+entry["description"]).lower())}"><p class="eyebrow">{number:02d} / {e(entry["category"].replace("-", " "))}</p>{preview}<h2><a href="{slug}-review.html">{e(entry["title"])}</a></h2><p>{e(entry["description"])}</p><a class="pill" href="{slug}-review.html">Review template &amp; prompts →</a></article>')
        file_controls = (f'<button type="button" data-format="pdf">PDF</button><a href="{slug}.pdf" download>Download PDF</a>' if (output / f'{slug}.pdf').is_file() else '')
        prompts = []
        for key, title in [('customizationPrompt','Start with this template'),('creationPrompt','Build your own version')]:
            prompts.append(f'<details><summary>{title}</summary><label>Edit the prompt<textarea aria-label="{title} prompt">{e(brief[key])}</textarea></label><button type="button" data-copy>Copy prompt</button><span role="status"></span></details>')
        answers = ''.join(f'<dt>{e(key)}</dt><dd>{e(value)}</dd>' for key,value in brief['exampleAnswers'].items())
        body = f'''<header><a href="index.html">← All templates</a><strong>{e(entry['title'])}</strong><a href="{slug}.html" target="_blank">Open full page</a><a href="{slug}.html" download>Download HTML</a></header><main class="review-detail"><section class="review-stage"><nav aria-label="Preview width"><button type="button" data-format="html" aria-pressed="true">HTML</button>{file_controls}<button type="button" data-width="100%" aria-pressed="true">Desktop</button><button type="button" data-width="390px" aria-pressed="false">Mobile</button></nav><iframe class="review-preview" data-html="{slug}.html" data-pdf="{slug}.pdf" sandbox="" title="{e(entry['title'])} preview" src="{slug}.html"></iframe></section><aside><p class="eyebrow">{e(entry['category'].replace('-', ' '))}</p><h1>{e(entry['title'])}</h1><p>{e(entry['description'])}</p><p class="note">Start from this example, or adapt the brief below.</p>{''.join(prompts)}<details><summary>Example brief</summary><p>{e(brief['creationPromptOrigin'])}</p><dl>{answers}</dl></details></aside></main>'''
        body += '''<script>
for (const button of document.querySelectorAll('[data-copy]')) button.addEventListener('click', async () => {
 const section=button.closest('details'), text=section.querySelector('textarea'), status=section.querySelector('[role=status]');
 try {await navigator.clipboard.writeText(text.value); status.textContent='Copied';} catch {text.focus();text.select();status.textContent='Select and copy the prompt manually.';}
});
for (const button of document.querySelectorAll('[data-format]')) button.addEventListener('click', () => {
 const frame=document.querySelector('.review-preview');
 if(button.dataset.format==='pdf') {frame.removeAttribute('sandbox');frame.src=frame.dataset.pdf;}
 else {frame.setAttribute('sandbox','');frame.src=frame.dataset.html;}
 for(const other of document.querySelectorAll('[data-format]')) other.setAttribute('aria-pressed',String(other===button));
});
for (const button of document.querySelectorAll('[data-width]')) button.addEventListener('click', () => {
 document.querySelector('.review-preview').style.maxWidth=button.dataset.width;
 for(const other of document.querySelectorAll('[data-width]')) other.setAttribute('aria-pressed',String(other===button));
});
</script>'''
        (output / f'{slug}-review.html').write_text(shell(entry['title']+' · Review',body))
    from collection import CATEGORIES, LABELS
    filters='<button type="button" data-category="all" aria-pressed="true">All 100</button>'+''.join(f'<button type="button" data-category="{c}" aria-pressed="false">{e(label)} · 10</button>' for c,label in zip(CATEGORIES,LABELS))
    body = '<header><strong>CLAW ME / TEMPLATES &amp; PROMPTS</strong><span class="pill">100 editions · 10 categories</span></header><main><section class="intro"><h1>Start with something useful.</h1><p class="lead">100 worked examples, each with an HTML page, matching PDF, and two ways to make it yours. All example content is illustrative.</p></section><label class="review-search">Find a template<input type="search" aria-label="Search templates" placeholder="Try handover, workshop, budget…"></label><nav class="review-filters" aria-label="Template categories">'+filters+'</nav><p role="status" id="result-count">100 templates</p><div class="review-catalog">'+''.join(cards)+'</div><p id="empty-results" hidden>No matching templates. Try another category or search.</p></main><footer>HTML and PDF editions from one source. Every template includes customization and creation prompts with hypothetical sample answers.</footer>'
    body += """<script>
let selected='all';const search=document.querySelector('[type=search]');
function filter(){let count=0;for(const card of document.querySelectorAll('.review-catalog article')){const show=(selected==='all'||card.dataset.category===selected)&&card.dataset.search.includes(search.value.toLowerCase().trim());card.hidden=!show;if(show)count++;}document.querySelector('#result-count').textContent=count+' templates';document.querySelector('#empty-results').hidden=count>0;}
search.addEventListener('input',filter);for(const button of document.querySelectorAll('.review-filters button'))button.addEventListener('click',()=>{selected=button.dataset.category;for(const other of document.querySelectorAll('.review-filters button'))other.setAttribute('aria-pressed',String(other===button));filter();});
</script>"""
    (output / 'index.html').write_text(shell('Templates & Prompts · All 100',body))
    print(f'Built {len(review["slugs"])} complete review pairs in {output}')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    render(parser.parse_args().output)
