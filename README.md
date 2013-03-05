pip launcher for Windows
==========

If you installed multiple versions of pip globally in order to manage global 
packages for different versions of Python, this is for you.

Install
-------

1. `git clone git://github.com/cpylua/pip-launcher.git`
2. Copy `pips.cmd` to a place so that it's in your `PATH`
3. Edit the path of `pips.py` in `pips.cmd`, make sure it's correct


Usage
------

    usage: pips [launcher arguments] [pip arguments]

    Launcher arguments:

    -2    Launch the latest pip 2.x version
    -3    Launch the latest pip 3.x version(default)
    -X.Y  Launch the specified pip version