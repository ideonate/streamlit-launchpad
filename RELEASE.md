- To release a new version of streamlit-launchpad on PyPI:

Update setup.py to the new version

delete dist folder

`python setup.py sdist`

`twine upload dist/*`

git add and git commit

`git tag -a X.X.X -m 'comment'`

`git push`

`git push --tags`

