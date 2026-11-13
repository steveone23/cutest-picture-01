# Cutest Picture

An entry for the make.fun bounty "Make the cutest picture" (`cutest-picture-01`).

`main.py` copies `assets/entry.png` byte for byte to `/output/entry.png`. It checks that the picture is a PNG or JPEG of at most 1 MiB before writing, so every run produces the same bytes. It uses only the Python standard library and needs no network.

## Run

```sh
python main.py
```

For local testing, set `OUTPUT_DIR` to write somewhere other than `/output`:

```sh
OUTPUT_DIR=./out python main.py
```

## Picture

TODO: add the picture.

## License

MIT, see [LICENSE](LICENSE).
