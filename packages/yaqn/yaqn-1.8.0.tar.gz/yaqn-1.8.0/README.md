# YAQN - Yet Another Quick Note
> A fast, easy and OOTB app for taking your notes made in Python.

<img src="https://raw.githubusercontent.com/kutu-dev/yaqn/master/assets/screenshots/app.png" alt="Screenshot of the app" width=542>

## Installation
```
> pip install yaqn  # Install from pypi
> yaqn --check # Run the app and generate the config file
```

## How to use
Run the `yaqn` command, it will open the app. To save the note and close the app itself just press `Ctrl + Enter`.

### Open with a keyboard shortcut
This can't be done automatically by `pip`, please use the correct for your OS:
- MacOS: Use [Karabiner Elements](https://karabiner-elements.pqrs.org/) and import [this rule](https://github.com/kutu-dev/yaqn/tree/master/assets/karabiner-rules/open-yaqn.json). This should work in any standard python installation, if you a using `pyenv` or similar this rule should be modified manually.
- Windows: _Too complex too configure unfortunately..._
- Linux, FreeBSD and others depend of the window manager you're using.

## Configuration
Your configuration file is saved by default in:
- Unix-like: `~/.config/yaqn/config.toml`
- Windows: `%AppData%\yaqn\config.toml`

### Custom config path
You can use your custom path for the config using `--config`:
```
> yaqn ---config /path/to/config/directory
```
### Check the config file integrity
The argument `--check` allows you to create, check and repair the config file, just run the command and it will analyze the config:
```
> yaqn --check
[ INFO ] Check mode -> Config checked and operative
```

### Configuration structure
An ordinary config file looks like this:
```
notes_path = '/path/to/notes/directory'
extension = 'md'
```
And this is its structure:

| Parameter | Description |
| --- | --- |
| `notes_path` | Define the path to the directory the notes will be saved. You can use the word `default` to point to the generic notes path. |
| `extension` | Define the extension the notes will be saves. _Remember to **not** put `.` before the extension itself._ |
| `no_whitespaces` | Define if YAQN should convert all whitespaces to hyphens `-` in the file name. |
| `no_uppercase` | Define if YAQN should convert all uppercase letters to lowercase. |
| `no_firstline` | Define if YAQN should remove the first line of the note before save it (useful with apps like [ObsidianMD](https://obsidian.md/)). |

### Restore configuration to default
Use the command `yaqn --restore` to regenerate the configuration with its defaults values.

## Author

Created with :heart: by [Kutu](https://kutu-dev.github.io/).
> - GitHub - [kutu-dev](https://github.com/kutu-dev)
> - Twitter - [@kutu_dev](https://twitter.com/kutu_dev)

Logo of the app created by [vladlucha](https://macosicons.com/#/u/vladlucha) (account deleted unfortunately) in [MacOS Icons](https://macosicons.com/#/).
