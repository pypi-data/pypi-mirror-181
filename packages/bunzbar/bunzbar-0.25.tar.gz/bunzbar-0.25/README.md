# Bunzbar

## System requirements
- Linux system with dwm and a fresh status monitor
- pip

## Installing

### Using pip:
```bash
pip install bunzbar
```

### From source:
```bash
git clone git@gitlab.com:02742/bunzbar.git
cd bunzbar
pip install build twine
make build
pip install dist/*.whl
```


## Post installation

### Add `~/.local/bin` to your `$PATH`:
```bash
export PATH=~/.local/bin:$PATH
```

### Make it persistant
```bash
echo "export PATH=~/.local/bin:$PATH" >> .bashrc
```

## Usage

### Start service in subshell
```bash
bunzbar -s &
```

## Links

- [gitlab](https://gitlab.com/02742/bunzbar/)
- [pypi](https://pypi.org/project/bunzbar/)
