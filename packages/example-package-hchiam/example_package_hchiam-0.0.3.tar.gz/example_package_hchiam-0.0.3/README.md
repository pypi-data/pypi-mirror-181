# My notes:

Register for an account on test.pypi, and get an API token.

https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives

```sh
# update the pyproject.toml [project] name (to be the package name)
python3 -m pip install --upgrade build
# go to folder that contains pyproject.toml and run this:
python3 -m build
```

https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives

```sh
python3 -m pip install --upgrade twine
# go folder containing dist and run this:
python3 -m twine upload --repository testpypi dist/*
# for username, literally enter username as __token__
# for password, use your API key from your test.pypi account, including pypi- prefix
# https://test.pypi.org/search/?q=example_package_hchiam
# https://test.pypi.org/project/example-package-hchiam/
```

(more steps if you want to test the test-only version of your package: https://test.pypi.org/project/example-package-hchiam/)

To upload the production-ready version of your package: (pypi requires a separate registration and API key set up from the test.pypi site)

```sh
python3 -m twine upload dist/*
# for username, still literaly enter __token__
# for password, use your other API key from your pypi account, including pypi- prefix
# https://pypi.org/search/?q=example_package_hchiam
# https://pypi.org/project/example-package-hchiam/
```

https://pypi.org/project/example-package-hchiam/

```sh
# python3 -m pip install [your-package]
python3 -m pip install example_package_hchiam
```

`/tests/test_example.py` shows a good example of how the package will be used by users, where you can see a method from an inner/non-`__init__` file, e.g.:

```py
from example_package_hchiam.example import add_one
```

## Streamlined thereafter:

```sh
# update code
# update pyproject.toml version number
# remove the old .whl and .gz files
rm -rf dist
python3 -m build
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*

python3 -m pip install example_package_hchiam
```
