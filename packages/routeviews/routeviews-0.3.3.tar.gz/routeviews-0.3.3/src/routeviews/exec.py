import subprocess
from typing import List, Tuple, Union

from routeviews import exceptions


def run(command: List[str], expect_stderr=False, expect_rc=False, stdout_encoding='utf-8',**kwargs) -> Union[str,Tuple[str,int]]:
    """Run an arbitrary shell command.

    > Implemented using Python's builtin subprocess package. 

    Args:
        command (List[str]): The command to be run, along with any arguments.
        expect_stderr (bool, optional): Is STDERR output expected? Defaults to False.
        expect_rc (bool, optional): Is some return code other than 0 expected? Defaults to False.
        stdout_encoding (str, optional): How to decode stdout. Defaults to 'utf-8'. 
        **kwagrs: Additional keyword arguments are passed on to `subprocess.run`.

    Raises:
        ChildProcessError: If any output goes to STDERR, or if any other issue occurs.
        FileNotFoundError: If the command is not found.

    Returns:
        str: The output from running "command".

    Examples:

    It is easy to run simple commands leveraging `split`.

    >>> run('cat /dev/null'.split())
    ''

    If you'd like to use full shell semantics, put the command into a
    single string, and provide `shell=True` keyword arg.

    >>> run(['cat /dev/null | wc'], shell=True)
    '      0       0       0\\n'

    The next example greps over this file to find itself:

    >>> run(['cat src/routeviews/exec.py | grep "LOOKING FOR ME?"'], shell=True)
    '...grep "LOOKING FOR ME?"...'

    """
    # Prepare arguments for running the command
    if expect_stderr:
        kwargs.update({
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT,
        })
    else:
        kwargs.update({
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
        })
    # Actually run the subprocess!
    try:
        result = subprocess.run(command, **kwargs)
    # Error handling
    except FileNotFoundError:
        raise exceptions.ExecMissingError(command[0])

    if type(result.stdout) is bytes:
        result.stdout = result.stdout.decode(stdout_encoding)
    if type(result.stderr) is bytes:
        result.stderr = result.stderr.decode(stdout_encoding)

    if result.stderr and not expect_stderr:
        raise exceptions.ExecRuntimeError(result.returncode, result.stdout, result.stderr)

    if expect_rc:
        return result.stdout, result.returncode
    else:
        if result.returncode > 0:
            raise exceptions.ExecRuntimeError(result.returncode, result.stdout, result.stderr)
        return result.stdout
