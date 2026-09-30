# Contributing to OpenCode Prompt Forge

First-time contributors are welcome. Code, documentation, bug reports, and recorded evaluations all help.

## Find a useful task

Check the open issues. Comment on a task before starting to reduce duplicate work; a comment is not a requirement for small fixes. For a substantial feature, open a proposal before implementation.

Priority areas:
- Run the ten behavioral cases in a real OpenCode session and submit redacted evidence.
- Improve reproducible installation and troubleshooting examples.
- Add focused cases for ambiguity, prompt injection, or permission boundaries.
- Fix reproducible compatibility and installer bugs.

## Submit a pull request

1. Fork the repository and clone your fork.
2. Create a branch for one focused change.
3. Make the change and run:

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

4. For instruction changes, run relevant behavioral cases in OpenCode. Include exact inputs, redacted outputs, OpenCode version, provider/model, and rubric results. If you cannot run them, say so.
5. Push your branch and open a pull request against main. Explain the problem, resulting behavior, and validation.

The maintainer reviews contributions before merging. Contributors do not need direct write access. Do not submit credentials or private repository content.

## Quality expectations

Keep the core skill concise and provider-neutral. Preserve task scope and user authorization. Prefer durable guidance over model-specific claims. Do not claim improved quality or lower cost without reproducible measurements.

Behavioral fixtures are expectations, not successful model runs. Structural tests alone cannot establish instruction quality. Include appropriate attribution and license notices for reused material.

## Community conduct

Be respectful and constructive. Critique work rather than people; avoid harassment and discriminatory language. Use issues for project-related questions and report problematic content through GitHub's reporting tools.
