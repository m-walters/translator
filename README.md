# translator
Simple language translator script for files. Very scrappy.

### Setup & Usage

Install dependencies with `poetry`
```bash
poetry install
```

Call signature is `python translate.py <source_lang> <target_lang> [files]`.

- `[files]` can be a list of names in `docs/in/`
- It can also be a directory, to process all files within
- If `[files]` is null, the script automatically process all files within `docs/in/`.

Processed files are output to `docs/out/` with the `<target_lan>` code affixed.
