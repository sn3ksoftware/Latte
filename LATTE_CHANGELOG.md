# Latte Changelog

## 2.0.0-alpha
- Joining file paths now uses `os.path.join()`.
- `ROOT` variable is now set as `os.path.expanduser("~/Documents")` on StaSh and `os.path.expanduser("~/Library")` on Libterm.
- Repos can now be removed with `latte del-repo nickname`.
- The `stansi` class for colours now has been split into two `ansi` colours, one for StaSh and another for LibTerm.
- New function, `onstash()`, to check if Latte is running in a StaSh instance.
- New function, `init()`, to create paths required by Latte.
- The code now (mostly) conforms to PEP8 (except in areas where it is not better to do so, obviously.)
- The "universe" (i.e, default) repository has been change to [this](https://github.com/sn3ksoftware/lattepkgs/master) repo.
- Better exception handling (Errors are prettier!)
- `latte list-repos nickname` now shows the URL of the repo under that nickname.
- To update Latte, you can just do `latte install latte`.
- Yellow colours for `WARNING` level alerts.

## 1.0.0-alpha
- Initial fork from the main Latte repo (Seanld/Latte).
