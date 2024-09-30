# shed-pi

## Introduction

A package to run a Raspberry Pi in an outbuilding such as a garden shed, for the internet of sheds.

Automated use cases:

- Weather station
- Garden lighting
- Security

## Design Principles

The Hub contains a Protocol, and can utilise modules
A device contains a protocol, and can utilise modules

## TODO:

1. Fix: Bug: The script startup gets an incorrect time (Hasn't yet got the internet time)
2. Instructions on pinout
3. Tests for the utils and base protocol
4. Extend Baseprotocol with a reusable run method
5. General Integration test for the logger using a fake module
6. Test default endpoint address settings work in theory, because the test above overrides them
7. Device startup and shutdown needs a unit test
8. Temp probe should be a fixture
9. CPU temp probe should be a fixture

### Wish list:

- Poetry (Not started)
- Native webcomponent FE with Bootstrap
- pip install raspberry pi

## Development

### Precommit

Install pre-commit: https://pre-commit.com/

Configure precommit on your local git for the project by running the following at the root of the project:

```shell
pre-commit install
```

Pre-commit will then automatically run for your changes at commit time.

To run the pre-commit config manually, run:

```shell
pre-commit run --all-files
```

## Release

Generate the release

```shell
pip install -q build
python -m build
twine upload dist/*
```
