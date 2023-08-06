# forge-python

forge-python enables you to create, change, and develop industrial process simulations. It is an open source tool that codifies APIs into declarative configuration files that can be shared amongst team members, treated as code, edited, reviewed, and versioned.

# how to publish

## build distribution archives

- python3 -m pip install --upgrade build
- python3 -m build

## upload to PyPi

- python3 -m twine upload dist/\*
