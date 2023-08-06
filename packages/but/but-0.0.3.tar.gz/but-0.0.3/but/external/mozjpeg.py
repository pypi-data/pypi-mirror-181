import os
import re
from shutil import copyfile
from subprocess import check_call, check_output, STDOUT
from tempfile import NamedTemporaryFile

from ..utils import init_log

_log = init_log(__name__)


def mozjpeg_check_available():
    try:
        result = check_output(['jpegtran', '-version'], encoding='utf-8', stderr=STDOUT)
    except FileNotFoundError:
        raise RuntimeError('Cannot run `jpegtran` (FileNotFoundError)')

    version = re.match(r'mozjpeg version (.+?)$', result, re.MULTILINE)
    if version is None:
        raise RuntimeError(f'Cannot understand `jpegtran -version`, got {result!r}')

    version_tuple = tuple(version.group(1).split('.'))
    if version_tuple[0] != '4':
        raise RuntimeError(f'Expected mozjpeg version 4, got {version.group(1)!r}')

    return version_tuple


def mozjpeg_optimize(infile, outfile):
    try:
        check_call(['jpegtran', '-copy', 'none', '-optimize', '-outfile', outfile, '-strict', infile])
    except FileNotFoundError:
        raise RuntimeError('Cannot run `jpegtran` (FileNotFoundError)')


def mozjpeg_optimize_replace(infile):
    with NamedTemporaryFile(suffix='.jpeg') as f:
        outfile = f.name

        mozjpeg_optimize(infile, outfile)

        infile_size = os.stat(infile, follow_symlinks=False).st_size
        outfile_size = os.stat(outfile, follow_symlinks=False).st_size

        bytes_saved = infile_size - outfile_size
        if bytes_saved < 1:
            _log.info(f'MozJPEG could not reduce {infile}')
            return

        _log.info(f'MozJPEG reduced {infile} by {bytes_saved} bytes')

        copyfile(outfile, infile)
