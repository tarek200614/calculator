# assets/

This folder is for optional application assets.

If you want a custom window/taskbar icon, add one of the following files
here (the app will pick it up automatically, no code changes needed):

- `icon.ico` — used on Windows (recommended, since `.ico` is the native
  Windows icon format).
- `icon.png` — used as a fallback if `icon.ico` is not present (works on
  Windows, macOS, and Linux).

If neither file is present, the application simply runs with the default
Tk window icon — this is not an error.
