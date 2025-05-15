# project3_sanitycheck.py
from collections.abc import Sequence
import contextlib
import locale
from pathlib import Path
import platform
import queue
import subprocess
import sys
import tempfile
import threading
import time
import traceback
_REQUIRED_PYTHON_VERSION = ('3', '13')


class TextProcessReadTimeout(Exception):
    pass



class TextProcess:
    _READ_INTERVAL_IN_SECONDS = 0.025


    def __init__(self, args: [str], working_directory: str):
        self._process = subprocess.Popen(
            args, cwd = working_directory, bufsize = 0,
            stdin = subprocess.PIPE, stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)

        self._stdout_read_trigger = queue.Queue()
        self._stdout_buffer = queue.Queue()

        self._stdout_thread = threading.Thread(
            target = self._stdout_read_loop, daemon = True)

        self._stdout_thread.start()


    def __enter__(self):
        return self


    def __exit__(self, tr, exc, val):
        self.close()


    def close(self):
        self._stdout_read_trigger.put('stop')
        self._process.terminate()
        self._process.wait()
        self._process.stdout.close()
        self._process.stdin.close()


    def write_line(self, line: str) -> None:
        try:
            self._process.stdin.write((line + '\n').encode(locale.getpreferredencoding(False)))
            self._process.stdin.flush()
        except OSError:
            pass


    def read_line(self, timeout: float = None) -> tuple[str, bool] or None:
        self._stdout_read_trigger.put('read')

        sleep_time = 0

        while timeout is None or sleep_time < timeout:
            try:
                next_result = self._stdout_buffer.get_nowait()

                if next_result is None:
                    return None
                elif isinstance(next_result, Exception):
                    raise next_result
                else:
                    line = next_result.decode(locale.getpreferredencoding(False))
                    had_newline = False

                    if line.endswith('\r\n'):
                        line = line[:-2]
                        had_newline = True
                    elif line.endswith('\n'):
                        line = line[:-1]
                        had_newline = True

                    return line, had_newline
            except queue.Empty:
                time.sleep(TextProcess._READ_INTERVAL_IN_SECONDS)
                sleep_time += TextProcess._READ_INTERVAL_IN_SECONDS

        raise TextProcessReadTimeout()


    def _stdout_read_loop(self):
        try:
            while self._process.returncode is None:
                if self._stdout_read_trigger.get() == 'read':
                    line = self._process.stdout.readline()

                    if line == b'':
                        self._stdout_buffer.put(None)
                    else:
                        self._stdout_buffer.put(line)
                else:
                    break
        except Exception as e:
            self._stdout_buffer.put(e)



class TestFailure(Exception):
    pass



class TestInputLine:
    def __init__(self, text: str):
        self._text = text


    def execute(self, process: TextProcess) -> None:
        try:
            process.write_line(self._text)
        except Exception:
            print_labeled_output(
                'EXCEPTION',
                *[tb_line.rstrip() for tb_line in traceback.format_exc().split('\n')])

            raise TestFailure()

        print_labeled_output('INPUT', self._text)



class TestOutputLine:
    def __init__(self, text: str, timeout_in_seconds: float):
        self._text = text
        self._timeout_in_seconds = timeout_in_seconds


    def execute(self, process: TextProcess) -> None:
        try:
            output_line = process.read_line(self._timeout_in_seconds)
        except TextProcessReadTimeout:
            output_line = None
        except Exception:
            print_labeled_output(
                'EXCEPTION',
                [tb_line.rstrip() for tb_line in traceback.format_exc().split('\n')])

            raise TestFailure()

        if output_line is not None:
            output_text, had_newline = output_line

            print_labeled_output('OUTPUT', output_text)

            if output_text != self._text:
                print_labeled_output('EXPECTED', self._text)

                index = min(len(output_text), len(self._text))

                for i in range(min(len(output_text), len(self._text))):
                    if output_text[i] != self._text[i]:
                        index = i
                        break

                print_labeled_output('', (' ' * index) + '^')

                print_labeled_output(
                    'ERROR',
                    'This line of output did not match what was expected.  The first',
                    'incorrect character is marked with a ^ above.',
                    '(If you don\'t see a difference, perhaps your program printed',
                    'extra whitespace on the end of this line.)')

                raise TestFailure()
            elif not had_newline:
                print_labeled_output(
                    'ERROR',
                    'This line of output was required to have a newline',
                    'on the end of it, but it did not.')
        else:
            print_labeled_output('EXPECTED', self._text)

            print_labeled_output(
                'ERROR',
                'This line of output was expected, but the program did not generate',
                'any additional output after waiting for {} second(s).'.format(
                    self._timeout_in_seconds))

            raise TestFailure()


class TestEndOfOutput:
    def __init__(self, timeout_in_seconds: float):
        self._timeout_in_seconds = timeout_in_seconds


    def execute(self, process: TextProcess) -> None:
        output_line = process.read_line(self._timeout_in_seconds)

        if output_line is not None:
            print_labeled_output('OUTPUT', output_line)

            print_labeled_output(
                'ERROR',
                'Extra output was printed after the program should not have generated',
                'any additional output')

            raise TestFailure()


def run_test_first_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_first()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed First Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_second_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_second()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Second Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_third_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_third()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Third Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_fourth_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_third()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Fourth Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_fifth_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_fifth()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Fifth Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_sixth_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_sixth()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Sixth Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_seventh_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_seventh()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Seventh Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_eighth_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_eighth()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Eighth Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_nineth_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_nineth()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Nineth Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_tenth_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_tenth()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed Tenth Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_eleventh_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_eleventh()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Passed eleventh Case')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

def run_test_last_case() -> None:
    try:
        check_python_version()

        with contextlib.closing(start_process()) as process:
            test_lines = make_test_lines_last()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Congratulations! Your Project 3 implementation passed the sanity checker.  Note that',
                'there are many other tests you\'ll want to run on your own, because',
                'a number of other scenarios exist that are legal and interesting.')
    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')


def check_python_version() -> None:
    major, minor, _ = platform.python_version_tuple()
    req_major, req_minor = _REQUIRED_PYTHON_VERSION

    if (major, minor) != (req_major, req_minor):
        print_labeled_output(
            'ERROR',
            f'The version of Python in use is {platform.python_version()}.',
            f'This course requires the use of a {req_major}.{req_minor} version instead.')

        raise TestFailure()


def start_process() -> TextProcess:
    module_path = Path.cwd() / 'project3.py'

    if not module_path.exists() or not module_path.is_file():
        print_labeled_output(
            'ERROR',
            'Cannot find an executable "project3.py" file in this directory.',
            'Make sure that the sanity checker is in the same directory as the',
            'files that comprise your Project 3 solution.')

        raise TestFailure()
    else:
        return TextProcess(
            [sys.executable, str(module_path)],
            str(Path.cwd()))


def print_labeled_output(label: str, *msg_lines: Sequence[str]) -> None:
    showed_first = False

    for msg_line in msg_lines:
        if not showed_first:
            print('{:10}|{}'.format(label, msg_line))
            showed_first = True
        else:
            print('{:10}|{}'.format(' ', msg_line))

    if not showed_first:
        print(label)


def make_test_lines_first() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET MESSAGE "Hello Boo!"'),
        TestInputLine('PRINT MESSAGE'),
        TestInputLine('.'),
        TestOutputLine('Hello Boo!', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_second() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET NAME "Boo"'),
        TestInputLine('LET AGE 13.015625'),
        TestInputLine('PRINT NAME'),
        TestInputLine('PRINT AGE'),
        TestInputLine('.'),
        TestOutputLine('Boo', 10.0),
        TestOutputLine('13.015625', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_third() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET A 3'),
        TestInputLine('PRINT A'),
        TestInputLine('GOSUB "CHUNK"'),
        TestInputLine('PRINT A'),
        TestInputLine('PRINT B'),
        TestInputLine('GOTO "FINAL"'),
        TestInputLine('CHUNK: LET A 4'),
        TestInputLine('LET B 6'),
        TestInputLine('RETURN'),
        TestInputLine('FINAL: PRINT A'),
        TestInputLine('.'),
        TestOutputLine('3', 10.0),
        TestOutputLine('4', 10.0),
        TestOutputLine('6', 10.0),
        TestOutputLine('4', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_fourth() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('PRINT "Number:"'),
        TestInputLine('LET X 11'),
        TestInputLine('INNUM X'),
        TestInputLine('ADD X 7'),
        TestInputLinne('PRINT X'),
        TestInputLine('.'),
        TestOutputLine('Number:', 10.0),
        TestOutputLine('11', 10.0),
        TestOutputLine('18', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_fifth() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET A 1'),
        TestInputLine('GOTO 2'),
        TestInputLine('LET A 2'),
        TestInputLine('PRINT A'),
        TestInputLine('.'),
        TestOutputLine('1', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_sixth() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET Z 5'),
        TestInputLine('GOTO 5'),
        TestInputLine('LET C 4'),
        TestInputLine('PRINT C'),
        TestInputLine('PRINT Z'),
        TestInputLine('END'),
        TestInputLine('PRINT C'),
        TestInputLine('PRINT Z'),
        TestInputLine('GOTO -6'),
        TestInputLine('.'),
        TestOutputLine('0', 10.0),
        TestOutputLine('5', 10.0),
        TestOutputLine('4', 10.0),
        TestOutputLine('5', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_seventh() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET Z 5'),
        TestInputLine('GOTO "CZ"'),
        TestInputLine('CCZ: LET C 4'),
        TestInputLine('PRINT C'),
        TestInputLine('PRINT Z'),
        TestInputLine('END'),
        TestInputLine('CZ: PRINT C'),
        TestInputLine('PRINT Z'),
        TestInputLine('GOTO "CCZ"'),
        TestInputLine('.'),
        TestOutputLine('0', 10.0),
        TestOutputLine('5', 10.0),
        TestOutputLine('4', 10.0),
        TestOutputLine('5', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_eighth() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET A 4'),
        TestInputLine('ADD A 3'),
        TestInputLine('PRINT A'),
        TestInputLine('LET B 5'),
        TestInputLine('SUB B 3'),
        TestInputLine('PRINT B'),
        TestInputLine('LET C 6'),
        TestInputLine('MULT C B'),
        TestInputLine('PRINT C'),
        TestInputLine('LET D 8'),
        TestInputLine('DIV D 2'),
        TestInputLine('PRINT D'),
        TestInputLine('.'),
        TestOutputLine('7', 10.0),
        TestOutputLine('2', 10.0),
        TestOutputLine('12', 10.0),
        TestOutputLine('4', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_nineth() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET A 1'),
        TestInputLine('GOSUB 4'),
        TestInputLine('PRINT A'),
        TestInputLine('PRINT B'),
        TestInputLine('END'),
        TestInputLine('LET A 2'),
        TestInputLine('LET B 3'),
        TestInputLine('RETURN'),
        TestInputLine('.'),
        TestOutputLine('2', 10.0),
        TestOutputLine('3', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_tenth() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET A 3'),
        TestInputLine('GOSUB "PRINTABC"'),
        TestInputLine('LET B 4'),
        TestInputLine('GOSUB "PRINTABC"'),
        TestInputLine('LET C 5'),
        TestInputLine('GOSUB "PRINTABC"'),
        TestInputLine('LET A 1'),
        TestInputLine('GOSUB "PRINTABC"'),
        TestInputLine('END'),
        TestInputLine('PRINTABC: PRINT A'),
        TestInputLine('PRINT B'),
        TestInputLine('PRINT C'),
        TestInputLine('RETURN'),
        TestInputLine('.'),
        TestOutputLine('3', 10.0),
        TestOutputLine('0', 10.0),
        TestOutputLine('0', 10.0),
        TestOutputLine('3', 10.0),
        TestOutputLine('4', 10.0),
        TestOutputLine('0', 10.0),
        TestOutputLine('3', 10.0),
        TestOutputLine('4', 10.0),
        TestOutputLine('5', 10.0),
        TestOutputLine('1', 10.0),
        TestOutputLine('4', 10.0),
        TestOutputLine('5', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_eleventh() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET A 1'),
        TestInputLine('GOSUB 5'),
        TestInputLine('PRINT A'),
        TestInputLine('END'),
        TestInputLine('LET A 3'),
        TestInputLine('RETURN'),
        TestInputLine('PRINT A'),
        TestInputLine('LET A 2'),
        TestInputLine('GOSUB -4'),
        TestInputLine('PRINT A'),
        TestInputLine('RETURN'),
        TestInputLine('.'),
        TestOutputLine('1', 10.0),
        TestOutputLine('3', 10.0),
        TestOutputLine('3', 10.0),
        TestEndOfOutput(2.0)
    ]

def make_test_lines_last() -> list[TestInputLine | TestOutputLine]:
    return [
        TestInputLine('LET A 3'),
        TestInputLine('LET B 5'),
        TestInputLine('GOTO 2 IF A < 4'),
        TestInputLine('PRINT A'),
        TestInputLine('PRINT B'),
        TestInputLine('.'),
        TestOutputLine('5', 10.0),
    ]

def run_test_lines(process: TextProcess, test_lines: list[TestInputLine | TestOutputLine]) -> None:
    for line in test_lines:
        line.execute(process)


if __name__ == '__main__':
    test_cases = [
        run_test_first_case,
        run_test_second_case,
        run_test_third_case,
        run_test_fourth_case,
        run_test_fifth_case,
        run_test_sixth_case,
        run_test_seventh_case,
        run_test_eighth_case,
        run_test_nineth_case,
        run_test_tenth_case,
        run_test_eleventh_case,
        run_test_last_case
    ]
    for test_case in test_cases:
        test_case()
        print()
