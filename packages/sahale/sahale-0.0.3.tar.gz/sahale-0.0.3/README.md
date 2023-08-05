# sdk-python

# TODO add instructions for testing package locally
To install locally: note: this isn't currently working
Q: is setup.py being used by anyone?
`pip install .` (in root of package, where pyproject.toml is located)

Running the example to create a new activity
```
cd test
python sahale.py
```

Python SDK for Sahale

Make sure to bump up the version number in setup.py

Building and publishing to Test PyPi repo: 
Activate virtual env
```
python3 -m build
python3 -m twine upload --repository testpypi dist/*
````

Installing package:
`python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps sahale`

Note: need to first create a test PyPi account and create an API key and put it in the `$HOME/.pypirc` file as per https://packaging.python.org/en/latest/tutorials/packaging-projects/

Can then view the package on Test PyPi i.e. https://test.pypi.org/project/sahale


Building and publishing to PyPi repo:
```
python3 -m build
python3 -m twine upload --skip-existing dist/*
```
And we can install normally using
`pip install sahale`


----------------------
TODOS
Q: if we do pip install update will that be faster? 
