# ep-algorithm-wrapper package

Algorithm wrapper for the ep project

## Create new distro version

1. Cd into correct directory
`cd python-ep-algorithm-wrapper/`

2. Update wheel packages on local machine
`python -m pip install --upgrade build`

3. Generate distribution files
`python -m build`

4. To test locally, install the package on your local machine
`python -m pip install -e .`

## Upload new version

1. `python -m pip install --upgrade twine`

2. `python -m twine upload dist/*`
