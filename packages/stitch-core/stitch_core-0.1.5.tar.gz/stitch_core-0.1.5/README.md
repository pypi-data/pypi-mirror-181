# Stitch Bindings

This repo provides Python bindings to [stitch](https://github.com/mlb2251/stitch).

## Installing the bindings
```bash
pip install stitch-core
```

Opening a new `python` session and running `import stitch_core` should succeed.

## Using the bindings

**TODO give tutorial**

For more usage examples, see `tests/test.py` in this repo.

## Using a specific version of `stitch`
To build the bindings for a specific commit, modify the line beginning with `stitch_core =` in `Cargo.toml` to have the SHA of the desired commit, for example:


## Locally building the bindings
Adjust the `rev` value in `Cargo.toml` to the desired commit SHA:
```toml
stitch_core = { git = "https://github.com/mlb2251/stitch", rev = "058890ecc3c3137c5105d673979304edfb0ab333"}
```

To build, install, and test the bindings run:
```bash
make
```
which install the bindings for `python3` by default. To use a specific interpreter pass it in like so:
```bash
make PYTHON=python3.10
```

Note on testing bindings: simply executing `python3 tests/test.py` may fail for strange PYTHONPATH-related reasons so use `make test` or `cd tests && python3 test.py` instead.

## Publishing the bindings to PYPI
`maturin publish`