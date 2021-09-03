# Python AWS REST API

This is a working backbone for a new REST API written in Python and deployed to Amazon AWS with TerraForm. The intent is to accelerate
while starting a new project.


## Configuration



## Building

TODO

## Deploying

TODO

## Testing

### Unittests

All the unittests are located inside ``api/tests/unittests`` directory and are written inside the files that coresponds to the files with
source code - ``tests/unittests/test_main.py`` to ``src/main.py``, ``tests/unittests/test_utils.py`` to ``src/utils.py``, etc.

Tests are triggered via ``make tests-unittests`` command that is more or less equivalent to:

```bash
$> cd api
$> PYTHONPATH=src pipenv run pytest -ra -v --cov --cov-report=term-missing:skip-covered tests/unittests
```

Pytest configuration is located inside ``api/pytest.ini`` file, where one can also modify ENVs for test execution. There is also
``api/.coveragerc`` where one can modify the success threshold for tests' coverage. Adding any new tools (libs, packages) to testing
environment should be added inside to the ``Pipfile``:

```
[[source]]
...

[packages]
...

[dev-packages]
...
            <--- HERE
```

