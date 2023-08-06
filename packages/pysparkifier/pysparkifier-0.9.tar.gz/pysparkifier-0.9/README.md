## pysparkifier
Incorporate pyspark easily into pandas/numpy workflows

### Installation

### Fresh pyspark installation / Including dependencies

If you're starting fresh the following will include installation of `pyspark`:

```
pip3 install [--force-reinstall] --no-dependencies 
```

### For an existing pyspark environment / not including dependencies

If you're installing into an existing python/pyspark environment:

```
pip3 install [--force-reinstall] --no-dependencies 
```



### releases

Update the setup.py for the version: needs to be changed in two places:

  - the version
  - the download url

Apply following in the root dir

```
rm -rf dist
rm -rf  pysparkifier.egg-info/
python -m setup sdist
twine upload -r  pypi dist/*
```
For _twine_ username:  use the first part of email (_javadba_ in my case) without the _@provider.com_ 