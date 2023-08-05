Want to add a new CLI tool to the 'Route Views CLI package?'
This is a short guide to help anyone add tools to this `routeviews` package.

# Prerequisites

We've provides instructions for setting up a simple 'local development environment' in our [Developer Guide](./development.md).

# Adding a Tool (Script)

If you already have a script created, you'll still likely want to start from the template suggested below if you'd like to use standard solutions.

1. Make a copy of the "src/routeviews/scripts/template.py" file.
2. Rename the new module/file, per PEP8 (underscores are fully acceptable in the `scripts` package).
3. Fill in any 'TODO' statements in the new script.

Finally, now that the script is ready to go, it is just time to do a bit of Python package wiring. 

4. Add the new script to the list of `console_scripts` in "setup.py"

Assuming you choose the name 'routeviews-tinker' for your tool (and used the template provided), you would add the following line to `console_scripts`:
```python
            'routeviews-tinker=routeviews.scripts.tinker:run_main',
```

5. Finally, reinstall the package using `pip install -e`. This will enable the new tool to run from the CLI!

```bash
$ pip install -e .
```

## Test the new tool

The tool can be tested directly at the command line:

```
$ routeviews-tinker
```

> ℹ Tip: Since the package is installed in editable mode, any changes you make to the code will effect this command!

## Automated Tests

In addition to manual testing, we use Pytest for automated testing.

> ℹ Tip: Please do consider adding automated tests!
> Adding some automated test coverage helps ensure future changes don't break the tool just added!

1. Add a new test module/file in the "tests" directory. Ex. `test_tinker.py`

2. Write your first **test function**! A toy example test function is below, following the "Arrange, Act, Assert" structure:

> A **test function** is any function that starts with the word `test` in this workspace.
>
> ℹ Test functions should contain some **self-check**, generally via assertions (or assertion libraries).
>
> The "Arrange, Act, Assert" structure helps ensure that test functions contain only one action, and that it is self-checked via assertions.

> ℹ Tip: Consider using the `assertpy` library for assertions!
>  
> ℹ Tip: Consider writing `doctest` test cases! 

```
def test_assignment_operator():
    # Arrange
    y = 2

    # Act
    x = y

    # Assert
    assert x == 2
```

