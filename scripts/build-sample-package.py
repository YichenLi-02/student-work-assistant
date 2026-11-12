"""Build/check the English sample browser and current file manifest.

Uses only the standard library. Never changes source messages, quotes, original
annotations, reviewer notes or test inputs.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'samples_deidentified'
TEXT_SUFFIXES = {'.md', '.json', '.jsonl', '.py', '.html', '.css'}


def read_jsonl(name: str) -> list[dict]:
    return [json.loads(line) for line in (DATA / name).read_text(encoding='utf-8').splitlines() if line.strip()]


def validate(rows: list[dict], candidates: list[dict], translations: dict) -> None:
    by_id = {row['sample_id']: row for row in rows}
    if len(by_id) != len(rows) or len(rows) != 50:
        raise ValueError('Expected 50 unique message IDs')
    if Counter(row['direction'] for row in rows) != {'inbound': 40, 'outbound': 10}:
        raise ValueError('Expected 40 inbound / 10 outbound messages')
    if Counter(row['split'] for row in rows) != {'dev': 19, 'holdout': 21, 'style_reference': 10}:
        raise ValueError('Unexpected split counts')
    for row in rows:
        if row['direction'] == 'inbound':
            review = row.get('annotation') or {}
            if review.get('status') != 'human_reviewed' or not review.get('reviewed_by'):
                raise ValueError(f"Missing human-review record: {row['sample_id']}")
            if row['sample_id'] not in translations['mail']:
                raise ValueError(f"Missing English annotation: {row['sample_id']}")
        elif row['sample_id'] not in translations['style']:
            raise ValueError(f"Missing English style annotation: {row['sample_id']}")
    if len(candidates) != 32 or len({c['candidate_id'] for c in candidates}) != 32:
        raise ValueError('Expected 32 unique time candidates')
    if len({c['sample_id'] for c in candidates}) != 24:
        raise ValueError('Expected time evidence in 24 messages')
    for candidate in candidates:
        evidence = candidate['evidence']
        body = by_id[candidate['sample_id']]['body_redacted']
        start, end = evidence['start_char'], evidence['end_char']
        if evidence['source_id'] != candidate['sample_id'] or not (0 <= start < end <= len(body)):
            raise ValueError(f"Invalid source/offset: {candidate['candidate_id']}")
        if body[start:end] != evidence['quote']:
            raise ValueError(f"Evidence mismatch: {candidate['candidate_id']}")


def browser(rows: list[dict], candidates: list[dict], translations: dict) -> str:
    css = (DATA / 'sample_browser.css').read_text(encoding='utf-8').strip()
    by_mail = defaultdict(list)
    for candidate in candidates:
        by_mail[candidate['sample_id']].append(candidate)
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
             'style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; connect-src \'none\'; img-src \'none\'">',
             '<title>Track 4 Mail Samples</title><style>', css, '</style></head><body><main>',
             '<header><h1>Track 4 Mail Samples</h1>',
             '<p class="lead">50 de-identified real-source messages for triage, task/date extraction, '
             'calendar edge cases and style development. Replay historical messages at receipt; '
             'this page creates no current tasks.</p>',
             '<div class="stats"><div class="stat"><strong>40</strong>Inbound samples</div>'
             '<div class="stat"><strong>10</strong>Style references</div>'
             '<div class="stat"><strong>32</strong>Time expressions</div></div>',
             '<p class="lead">dev 19 &middot; reserved holdout 21 &middot; style_reference 10. '
             'The data owner checked the 40 inbound labels on 10 November 2026. '
             'English annotations below are display translations; original reviewer notes remain in the JSONL. '
             'The reserved split was used during development and is not a blind final test.</p></header>',
             '<div class="tools"><input id="search" aria-label="Search samples" '
             'placeholder="Search subjects, tasks, dates, IDs or source text">',
             '<select id="split" aria-label="Filter by split"><option value="">All splits</option>'
             '<option>dev</option><option>holdout</option><option>style_reference</option></select>',
             '<button id="open">Expand visible samples</button><button id="close">Collapse all</button></div>',
             '<p id="count" class="meta">Showing 50 / 50</p>']
    for row in rows:
        sid = row['sample_id']
        ann = row.get('annotation') or {}
        style = row['direction'] == 'outbound'
        en = translations['style' if style else 'mail'][sid]
        labels = []
        if style:
            labels.append('Style reference')
        else:
            if ann.get('needs_reply'):
                labels.append('Needs reply')
            if ann.get('needs_action'):
                labels.append('Needs action')
            if not labels:
                labels.append('No required action')
        parts.extend([
            f'<article id="{sid}" data-split="{row["split"]}" data-direction="{row["direction"]}">',
            f'<details><summary><span class="id">{sid}</span><span>{escape(row["subject"])}</span>'
            f'<span class="pill">{escape(" + ".join(labels))}</span></summary><div class="inside">',
            f'<p class="meta">{row["direction"]} &middot; {row["split"]} &middot; '
            f'{escape(row["message_datetime_original"])}<br>Original MBOX ordinal '
            f'{row["original_mbox_ordinal_1based"]} &middot; {escape(row["from_redacted"])}</p>',
            '<h4>English reference annotation</h4>',
            f'<p><b>{escape(en.get("function" if style else "summary", ""))}</b><br>'
            f'{escape(en.get("observations" if style else "expected", ""))}</p>',
        ])
        if en.get('uncertainty'):
            parts.append(f'<p class="warning">Check: {escape(en["uncertainty"])}</p>')
        # Encode line-end spaces so the rendered source is exact without trailing
        # whitespace in the generated HTML's Git diff.
        body_html = escape(row['body_redacted']).replace(' \n', '&#32;\n')
        parts.extend(['<h4>Source body (de-identified; quoted history and footers removed)</h4>',
                      f'<pre>{body_html}</pre>'])
        attachments = ', '.join(row['attachments_present']) or 'No MIME attachments'
        scope = row.get('attachment_read_scope') or 'Attachment bodies not read'
        parts.append(f'<p class="meta">Attachment metadata: {escape(attachments)}. {escape(scope)}.</p>')
        if row.get('calendar_metadata'):
            parts.extend(['<h4>ICS scheduling metadata</h4>',
                          f'<pre>{escape(json.dumps(row["calendar_metadata"], ensure_ascii=False, indent=2))}</pre>'])
        if by_mail[sid]:
            parts.append('<h4>Time roles and candidates</h4><ul>')
            for c in by_mail[sid]:
                value = ' '.join(str(c.get(key) or 'not stated') for key in
                                 ('official_date_candidate', 'official_time_candidate', 'timezone'))
                parts.append(f'<li><b>{escape(c["entity_key"])}</b>: {escape(value)} '
                             f'<span class="status">{escape(c["status"])}</span><br>'
                             f'<q>{escape(c["evidence"]["quote"])}</q><br>'
                             f'{escape(c.get("interpretation_note", ""))}</li>')
            parts.append('</ul>')
        parts.append('<p class="meta">Reference annotations are not execution approval. '
                     'This viewer cannot send messages or write calendars.</p></div></details></article>')
    parts.extend(['<footer>Fully offline: no external resources, uploads or real-operation buttons. '
                  'Course content and dates may still identify someone indirectly; review before sharing.</footer></main>',
                  '<script>',
                  "const cards=[...document.querySelectorAll('article')];"
                  "function filter(){const q=document.querySelector('#search').value.toLowerCase(),"
                  "s=document.querySelector('#split').value;let n=0;cards.forEach(c=>{const show="
                  "(!q||c.textContent.toLowerCase().includes(q))&&(!s||c.dataset.split===s);"
                  "c.hidden=!show;if(show)n++});document.querySelector('#count').textContent=`Showing ${n} / 50`;}",
                  "document.querySelector('#search').addEventListener('input',filter);"
                  "document.querySelector('#split').addEventListener('change',filter);"
                  "document.querySelector('#open').onclick=()=>cards.filter(c=>!c.hidden)"
                  ".forEach(c=>c.querySelector('details').open=true);"
                  "document.querySelector('#close').onclick=()=>cards.forEach(c=>c.querySelector('details').open=false);",
                  '</script></body></html>'])
    return '\n'.join(parts) + '\n'


def canonical_bytes(path: Path) -> bytes:
    if path.suffix in TEXT_SUFFIXES:
        return path.read_text(encoding='utf-8').encode('utf-8')
    return path.read_bytes()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate without changing files')
    args = parser.parse_args()
    rows = read_jsonl('selected_50.jsonl')
    candidates = read_jsonl('date_candidates.jsonl')
    translations = json.loads((DATA / 'annotation_en.json').read_text(encoding='utf-8'))
    validate(rows, candidates, translations)
    generated = {'sample_browser.html': browser(rows, candidates, translations)}
    files = []
    for path in sorted(DATA.iterdir()):
        if not path.is_file() or path.name == 'AI_SOURCE_MANIFEST.json':
            continue
        content = generated[path.name].encode('utf-8') if path.name in generated else canonical_bytes(path)
        files.append({'name': path.name, 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
    manifest = {
        'package': 'Track4_deidentified_source_materials',
        'derived_from': 'Private user-provided MBOX and original selection package (not included)',
        'pseudonymised': True,
        'hash_format': 'UTF-8 text with LF line endings; exact bytes for binary files',
        'counts': {'real_email_samples': 50, 'inbound': 40, 'style_references': 10, 'time_expressions': 32},
        'annotation_status': '40 inbound labels checked by the data owner on 2026-11-10; style profile provisional',
        'language_policy': 'English documentation/display; preserve original source, reviewer notes and bilingual test inputs',
        'files': files,
    }
    generated['AI_SOURCE_MANIFEST.json'] = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    stale = []
    for name, content in generated.items():
        path = DATA / name
        if args.check:
            if not path.is_file() or path.read_text(encoding='utf-8') != content:
                stale.append(name)
        else:
            path.write_text(content, encoding='utf-8', newline='\n')
    if stale:
        print('Out of date: ' + ', '.join(stale) + '. Run without --check to rebuild.')
        return 1
    print(f'Package {"checked" if args.check else "rebuilt"}: 50 messages, 32 exact quotes; '
          f'{len(files)} files in the manifest.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
