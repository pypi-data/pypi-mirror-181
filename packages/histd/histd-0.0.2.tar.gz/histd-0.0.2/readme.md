# How I spent this day

A simple but useful personal diary application.

The sole purpose of this application is to quickly create a file
and open it in a text editor so that I can take a note before I lose my desire.
Notes can be found in the `~/.local/share/histd` directory.

```sh
tree ~/.local/share/histd
# /home/user/.local/share/histd
# └── 2022
#     └── 08
#         ├── 18.md
#         └── 19.md
```

## Installation
```bash
pip install histd
```

## Usage
```bash
python -m histd
```

## Backup
To create an archive of all notes, run the following command:
```bash
python -m histd backup
```

## Merge all notes
This command concatenates all files and prefixes each with the filename.
```bash
python -m histd merge
```
