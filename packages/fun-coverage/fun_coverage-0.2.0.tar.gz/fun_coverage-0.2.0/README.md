# fun-coverage

fun-coverage is a tool to extract *function coverage* from the *statement (= line) coverage* of [coverage.py](https://github.com/nedbat/coveragepy).

## Installation
The simplest way to install fun-coverage is with pip:
```shell
pip install fun-coverage
```

## Getting started
After installing the package, a `fun-coverage` command will be available.

You need to run coverage.py first. For example, if you're using it through [pytest-cov](https://github.com/pytest-dev/pytest-cov/):
```shell
pytest --cov=<my_module> <my_module_tests>
```

Once this is done, simply run:
```shell
fun-coverage
```

This will print a text report similar to the one of coverage.py, but for functions. The report will include the line numbers of the missed functions.

For example, this is the output of `fun-coverage` run on its example test suite (as a preliminary step of its actual test suite):
```
Name                                                                            Funcs   Miss   Cover   Missing
--------------------------------------------------------------------------------------------------------------
tests/example_test_suite/src/__init__.py                                            0      0    100%
tests/example_test_suite/src/async_function.py                                      1      0    100%
tests/example_test_suite/src/covered_function_with_partially_covered_lines.py       1      0    100%
tests/example_test_suite/src/docstring_only_function.py                             1      0    100%
tests/example_test_suite/src/excluded_function.py                                   0      0    100%
tests/example_test_suite/src/methods.py                                             2      2      0%   6, 9
tests/example_test_suite/src/non_covered_function.py                                1      1      0%   1
--------------------------------------------------------------------------------------------------------------
TOTAL                                                                               6      3     50%
```

## How it works
fun-coverage looks for functions and methods in the source code files concerned by a previous round of statement coverage measurement, then marks them as hit if and only if their first statement has been hit.

Specifically, this starts from the `.coverage` file left by coverage.py. This is configurable with the `--cov-file` flag.

## Command-line options
```
usage: fun-coverage [--cov-file COV_FILE] [--cov-fail-under MIN]

  --cov-file COV_FILE   Which coverage file to analyze (default .coverage in the current directory)
  --cov-fail-under MIN  Fail if the total coverage is strictly less than MIN (a percentage between 0 and 100)
```

## Excluding code from fun-coverage
If the line containing the `def` or `async def` statement for a function is [excluded](https://coverage.readthedocs.io/en/latest/excluding.html) from coverage.py, then fun-coverage ignores that entire function.

## Compatibility
fun-coverage has been tested with `coverage==6.4`, and `pytest-cov==3.0.0`.

## Development
This section only applies if you wish to contribute to the project.

### pre-commit
This project uses [pre-commit](https://pre-commit.com/). Please [install it](https://pre-commit.com/#install), then activate it to run automatically on `git commit`:
```shell
pre-commit install
```
### Tests
Run the test suite with:
```shell
make test
```
