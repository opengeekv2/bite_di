from inspect import signature
from io import StringIO
from bite_di import container
from mypy.api import run
import sys

def debug():
    stubs = StringIO()
    for f in container().decorated:
        stubs.write('def ' + f.__name__ + str(signature(f)) + ':\n')
        stubs.write('  pass\n')
        stubs.write('\n')

        stubs.write(container().generate_test_call(f))
        stubs.write('\n')
        stubs.write('\n')

    result = run(['-c', stubs.getvalue()])

    if result[0]:
        print('\nType checking report:\n')
        print(result[0])  # stdout

    if result[1]:
        print('\nError report:\n')
        print(result[1], file=sys.stderr)  # stderr

    print('\nExit status:', result[2])


