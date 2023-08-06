# mkdirpy

Like `mkdir` but with `__init__.py` inside

## Installation

```
pip install mkdirpy
```

## Usage

The syntax is identical to `mkdir`:

```
mkdirpy foo
```

Will create `foo` directory and `foo/__init__.py`

Use `-p` flag to generate parent directories recursively:

```
mkdirpy -p foo/bar
```

Will create `foo`, `foo/__init__.py`, `foo/bar`, `foo/bar/__init__.py`

Add `-v` flag for verbose output:

```
mkdirpy -pv foo/bar
```

Output:

```
foo
foo/__init__.py
foo/bar
foo/bar/__init__.py
```
