# HowIGotHere

A package containing a single function `howigothere` that returns a condensed
stack preview. Useful for debugging to easily trace how some call was made,
even through a jungle of calls made by frameworks and other packages.

To see it in action, you can run
[`example.py`](https://github.com/vsego/howigothere/blob/master/example.py) or, if
you didn't install the package but you only downloaded this repository,
[`example.sh`](https://github.com/vsego/howigothere/blob/master/example.sh). Both
approaches require that
[`settings-collector`](https://pypi.org/project/settings-collector/) is
installed. The result should look like this:

![Screenshot](https://raw.githubusercontent.com/vsego/howigothere/master/images/example.png)

## Content

1. [The name](#the-name)
2. [Usage](#usage)
3. [Global setup](#global-setup)
4. [Local setup](#local-setup)

## The name

The name of the package is "How I Got Here?". If your question is "How I Go
There?", wherever "there" might be, you'll need to ask some other package.

## Usage

Make an import:
```python
from howigothere import howigothere
```
and then call
```python
print(howigothere())  # or logger.debug(howigothere())
```
somewhere in your code.

## Global setup

This package relies on
[`settings-collector`](https://pypi.org/project/settings-collector/) to collect
settings from various frameworks. This means that you can set it up through
standard mechanisms of the framework used by your project.

For example, if you are using Django, you can set the separator colour by
defining `HOWIGOTHERE__COLOR_SEP` (note two underscores before `COLOR`, but
only one after it) in your Django settings. The frameworks' settings character
casing is respected, so - for example - in TurboGears this will be
`howigothere__color_sep`

If you don't use a framework (or, at least, not one supported by
`settings-collector`), you can also use `sc_settings` (`settings-collector`'s
`dict`-like equivalent of frameworks' configs) and do something this:
```python
from settings_collector import sc_settings

sc_settings["howigothere__color_sep"] = colorama.Fore.RED
```

For more details, please see the documentation of `settings-collector`.

If the setup (either in `sc_settings` or in framework's settings) contains
`settings-collector`'s scopes, you can specify the scope to use like this:
```python
howigothere(namespace="some_scope")
```

## Local setup

Lastly, you can also configure values when calling the function. For example,
```python
howigothere(color_sep=colorama.Fore.RED)
```

Here is the list of all arguments accepted by the function. All but `namespace`
are also available in `sc_settings` and frameworks' settings. The default
values are as shown, unless overridden in `sc_settings` or framework's setup.

* `namespace` [default: `None`]: If set, it is used as scope identifier in
  `settings_collector`.
* `keep_dirs` [default: 1]: The number of directories to keep in output (`None`
  to keep them all). For example, if set to `2`, path `/a/b/c/d/e/f.py` will be
  displayed as `d/e/f.py`. This is to reduce the output while still being able
  to distinguish between files with the same name.
* `sep` [default: `" > "`]: Separator between calls.
* `call_format` [default: `"{function} ({path}:{lineno})"`]: The format of each
  call.
* `no_color` [default: `False`]: If set to `True`, colours won't be used even
  if they are properly defined. This is useful if you want to have properly
  coloured printouts most of the times, but you sometimes want to add these to
  some logging system that doesn't support your preferred way of colouring
  text.
* `start_from_dir` [default: `None`]: If set, output is suppressed until the
  first file having `start_from_dir` as its parent. This can also be a tuple of
  strings, in which case encountering any of them starts the output.

To add to those, colours can also be redefined. Their defaults depend on the
presence of `colorama` package (if it's not there, these are all empty strings
by default). The displayed defaults assume that `colorama` is installed and
that its `Fore` and `Style` constants are imported.

* `color_reset` [default: `Style.RESET_ALL`]: This is added to the end of each
  colourisable chunk (separator, function name, etc.).
* `color_sep` [default: `""`, i.e., no colouring]: Colour used for the
  separators between calls.
* `color_func`[ default: `Style.BRIGHT + Fore.GREEN`]: Colour used for
  functions' names in each call.
* `color_path` [default: `Style.BRIGHT + Fore.CYAN`]: Colour used for path of
  the each file containing called functions.
* `color_lineno` [default: `Fore.CYAN`]: Colour used for the line numbers where
  calls were made.
