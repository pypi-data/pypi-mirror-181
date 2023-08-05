# Installing Calliope from PyPI

The simplest way to get Calliope is:

    pip3 install calliope-music

Some Calliope modules have
[extra dependencies](https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html)
which you need to install before the command will work.

Here's what happens if you run `cpe spotify` without installing its extra
dependencies first:

```
> cpe spotify top-artists
ERROR: Command 'spotify' is not available.

You can install this module's dependencies using `pip`, for example:

    pip install calliope-music[spotify]

    Original error: No module named 'cachecontrol'
```

To solve this, run `pip3 install calliope-music[spotify]` and rerun
the command.

# Installing Calliope from a Git checkout

You can install from a local Git checkout using Pip:

    pip3 install .
