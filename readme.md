# sloplint

A linter to detect AI-generated markdown prose

## Usage

```sh
sloplint myfile.md
```

If AI-generated text issues are identified, sloplint will exit with a failure code reporting each issue it discovered just like a linter would.

## Triggers

- em-dash
- emojis
- bold text
