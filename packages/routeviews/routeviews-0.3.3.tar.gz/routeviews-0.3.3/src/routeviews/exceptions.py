"""Route Views Custom Exceptions.

Raising a custom exception instead of using [Python's Built-in
Exceptions](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
can add extra context to errors that future developers might encounter.
"""


class ParseError(Exception):
    pass


class EmptyError(ParseError):
    pass


class MissingTemplateError(ParseError):
    pass


class ExecError(Exception):
    pass


class ExecRuntimeError(ExecError):
    def __init__(self, ret_code, stdout, stderr):
        super().__init__(
            f'''There was unexpected output on STDERR!
Return Code: {ret_code}
STDOUT:
{stdout}

STDERR:
{stderr}
''')

class ExecMissingError(ExecError):
    def __init__(self, executable):
        super().__init__(f"Executable not found: '{ executable }'")
