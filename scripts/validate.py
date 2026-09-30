"""Validate this package's narrow frontmatter format without dependencies."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def metadata(path):
    text = path.read_text(encoding='utf-8')
    assert text.startswith('---\n'), f'{path}: missing frontmatter'
    header, body = text[4:].split('\n---\n', 1)
    pairs = [line.split(':', 1) for line in header.splitlines()]
    assert all(len(pair) == 2 for pair in pairs), f'{path}: invalid field'
    fields = {key.strip(): value.strip() for key, value in pairs}
    assert len(fields) == len(pairs), f'{path}: duplicate fields'
    assert all(fields.values()), f'{path}: empty field'
    return fields, body


def main():
    skill = ROOT / '.opencode/skills/prompt-forge/SKILL.md'
    fields, body = metadata(skill)
    assert fields['name'] == skill.parent.name
    assert re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', fields['name'])
    assert 1 <= len(fields['name']) <= 64
    assert 1 <= len(fields['description']) <= 1024
    assert fields['license'] == 'MIT' and fields['compatibility'] == 'opencode'
    assert len(body.splitlines()) < 500
    expected = {'forge', 'forge-review', 'forge-debug'}
    commands = list((ROOT / '.opencode/commands').glob('*.md'))
    assert {p.stem for p in commands} == expected
    for path in commands:
        fields, body = metadata(path)
        assert fields['agent'] == 'plan'
        assert '$ARGUMENTS' in body and 'prompt-forge' in body
    cases = json.loads((ROOT / 'evals/cases.json').read_text())
    assert len(cases) == 10 and len({c['id'] for c in cases}) == 10
    assert all(c['command'] in expected and c['input'] and c['expectation'] for c in cases)
    for file in ('README.md', 'LICENSE', 'CONTRIBUTING.md'):
        assert (ROOT / file).is_file()
    print('Package validation passed: skill, three commands, ten evaluation cases.')


if __name__ == '__main__':
    main()
