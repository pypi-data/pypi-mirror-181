import contextlib
import subprocess

import path
import autocommand
import jaraco.context
from more_itertools import consume

from . import git


@contextlib.contextmanager
def temp_checkout(project):
    with path.TempDir() as dir:
        repo = git.checkout(project, dir, depth=50)
        with repo:
            yield


@jaraco.context.suppress(FileNotFoundError)
def is_skeleton():
    return 'badge/skeleton' in path.Path('README.rst').read_text()


def update_project(name):
    if name == 'skeleton':
        return
    if 'fork' in name.tags:
        return
    print('\nupdating', name)
    with temp_checkout(name):
        if not is_skeleton():
            return
        proc = subprocess.Popen(['git', 'pull', 'gh://jaraco/skeleton', '--no-edit'])
        code = proc.wait()
        if code:
            try:
                subprocess.check_call(['git', 'mergetool', '-t', 'known-merge'])
            except subprocess.CalledProcessError:
                subprocess.check_call(['git', 'mergetool'])
            subprocess.check_call(['git', 'commit', '--no-edit'])
        subprocess.check_call(['git', 'push'])


class KeywordFilter(str):
    def __call__(self, other):
        return self in other


@autocommand.autocommand(__name__)
def main(keyword: KeywordFilter = None):  # type: ignore
    consume(map(update_project, filter(keyword, git.projects())))
