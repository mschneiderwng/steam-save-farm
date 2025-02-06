# Steam Save Farm

Steam Save Farm (`ssf`) is a tool to link save file directories from various places under `~/.steam` to a central place like `~/games/saves`. For example running

```
ssf "~/.steam/steam/steamapps/compatdata/1245620/pfx/drive_c/users/steamuser/AppData/Roaming/EldenRing/76561198041267816/" "~/games/saves/elden ring"
```
moves the elden ring save folder `76561198041267816` to `~/games/saves/elden ring` and replaces it with a symlink. Running the same command a second time does nothing.

Run directly from github using nix:

```
nix run github:mschneiderwng/steam-save-farm
```

# uv2nix

This project, although useful, mainly servers as demonstration how to use `uv2nix`. There are 2 development environments, an impure `uv` and a pure `nix` environment:

- `nix develop .#impure`
- `nix develop .#uv2nix`

A development virtual environment for the use with e.g. pycharm can be created with `nix build .#venv -o .venv`.
