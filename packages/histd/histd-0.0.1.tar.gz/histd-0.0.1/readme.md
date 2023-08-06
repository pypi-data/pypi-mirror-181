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

## Usage
```sh
python3 histd.py
```

## Installation
Recommended method
```sh
sudo cp histd.py /usr/local/bin/histd
```

Risky way (without cloning the repository)
```sh
sudo curl -o /usr/local/bin/histd "https://raw.githubusercontent.com/ordinary-dev/histd/master/histd.py"
```

To create a new note, you can simply type `histd` in the terminal.

## Backup
To create an archive of all notes, run the following command:
```bash
histd backup
```

## Merge all notes
This command concatenates all files and prefixes each with the filename.
```bash
histd merge
```
