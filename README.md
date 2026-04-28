# booklet-generator

Rearranges pages of a PDF into booklet order for double-sided A3 printing. Input pages are scaled to A4 and paired onto A3 spreads so the printed sheets can be folded and stapled into a booklet.

A separate A4 PDF is produced for the middle sheet if the page count doesn't fit nicely on A3s.

## Installation

### uv

Latest Release:
```
uv tool install git+https://github.com/rezzubs/booklet-generator
```

Specific version:
```
uv tool install git+https://github.com/rezzubs/booklet-generator@v0.1.0
```

### pip

Latest Release:
```
pip install git+https://github.com/rezzubs/booklet-generator
```

Specific version:
```
pip install git+https://github.com/rezzubs/booklet-generator@v0.1.0
```

## Usage

```
booklet-generator [OPTIONS] SOURCE
```

`SOURCE` is the path to the input PDF.

**Options**

| Flag | Description |
|---|---|
| `-o`, `--output`, `-d`, `--destination` | Directory to write output files. Defaults to the source directory. |
| `-n`, `--name` | Base name for output files. Defaults to the source file name. |
| `-h`, `--help` | Show help and exit. |

**Output files**

- `<name>-a3.pdf` — booklet spreads for double-sided A3 printing, flipped on the short edge.
- `<name>-a4.pdf` — middle sheet (only produced when the page count requires it).
