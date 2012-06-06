import os

import setuptools

from pyflakes import checker

import sys
import _ast
import re

def check(codeString, filename, outfile=None):
    try:
        tree = compile(codeString, filename, "exec", _ast.PyCF_ONLY_AST)
    except (SyntaxError, IndentationError):
        value = sys.exc_info()[1]
        try:
            (lineno, offset, line) = value[1][1:]
        except IndexError:
            print >> sys.stderr, 'could not compile %r' % (filename,)
            return 1
        if line.endswith("\n"):
            line = line[:-1]
        print >> sys.stderr, '%s:%d: could not compile' % (filename, lineno)
        print >> sys.stderr, line
        print >> sys.stderr, " " * (offset-2), "^"
        return 1
    else:
        w = checker.Checker(tree, filename)
        w.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
        for warning in w.messages:
            if outfile:
                outfile.write(str(warning) + '\n')
            else:
                print warning
        return len(w.messages)

def checkPath(filename, outfile=None):
    if os.path.exists(filename):
        return check(file(filename, 'U').read() + '\n', filename, outfile)

class PyflakesCommand(setuptools.Command):
    description = "run pyflakes on all your modules"
    user_options = [
        ('flakes-exclude-packages=', None, "omit these packages, modules"),
        ('flakes-file=', None, "write into this file"),
    ]

    def initialize_options(self):
        self.flakes_exclude_packages = 'tests test'
        self.flakes_file = None

    def finalize_options(self):
        self.flakes_exclude_packages = [module.strip() for module in re.split('[\s,]+', self.flakes_exclude_packages)]
        if self.flakes_file:
            self.flakes_file = open(self.flakes_file, 'w')

    def run(self):
        warnings = False
        base = self.get_finalized_command('build_py')
        for (package, module, file) in base.find_all_modules():
            if package in self.flakes_exclude_packages:
                continue

            if checkPath(file, self.flakes_file):
                warnings=True
        if warnings:
            sys.exit(1) # FAIL


