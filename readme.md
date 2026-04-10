# sloplint

[![Lint](https://github.com/jncraton/sloplint/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/sloplint/actions/workflows/lint.yml)
[![Test](https://github.com/jncraton/sloplint/actions/workflows/test.yml/badge.svg)](https://github.com/jncraton/sloplint/actions/workflows/test.yml)
[![Deploy](https://github.com/jncraton/sloplint/actions/workflows/deploy.yml/badge.svg)](https://github.com/jncraton/sloplint/actions/workflows/deploy.yml)
[![Release](https://github.com/jncraton/sloplint/actions/workflows/release.yml/badge.svg)](https://github.com/jncraton/sloplint/actions/workflows/release.yml)
[![PyPI](https://github.com/jncraton/sloplint/actions/workflows/pypi.yml/badge.svg)](https://github.com/jncraton/sloplint/actions/workflows/pypi.yml)

A linter to detect AI-generated markdown prose

## Installation

```sh
pip install sloplint
```

## Usage

```sh
sloplint myfile.md
```


If AI-generated text issues are identified, sloplint will exit with a failure code reporting each issue it discovered just like a linter would.

If you want to modify files in place to address issues, use the `--fix` flag.

```sh
sloplint --fix myfile.md
```

## Why?

The intent behind this package is not to "humanize" AI generations so that they can be accepted as human output. The intent of this tool is to flag AI-isms in human writing to avoid having folks think that you might be an AI. This may be especially helpful for humans who have been trained on a large corpus of Wikipedia and other open web texts.

## Resources

- [WP:AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
