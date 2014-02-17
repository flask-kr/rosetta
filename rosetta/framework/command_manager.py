# -*- coding:utf8 -*-
import os
import code
import argparse
import functools

from enum import Enum

class CommandManager(object):
    class ExitCode(Enum):
        EMPTY_ARGUMENTS = -1
        WRONG_PROCESS = -2

    class Error(Exception):
        pass

    class ArgumentError(Error):
        pass

    def __init__(self):
        self.main_parser = argparse.ArgumentParser()
        self.sub_parsers = self.main_parser.add_subparsers()

    def command(self, **option_table):
        def handler(func):
            option_names = func.func_code.co_varnames[:func.func_code.co_argcount]

            @functools.wraps(func)
            def wrapper(ns):
                return func(**dict((option_name, getattr(ns, option_name)) for option_name in option_names))

            sub_parser = self.sub_parsers.add_parser(func.func_name)
            for option_name in option_names:
                sub_parser.add_argument(option_name, **option_table[option_name])
            sub_parser.set_defaults(func=wrapper)
        return handler

    def add_common_argument(self, *args, **kwargs):
        self.main_parser.add_argument(*args, **kwargs) 
    
    def run_command(self, cmd_args):
        if cmd_args is None or len(cmd_args) == 0:
            self.main_parser.print_help()
            return self.ExitCode.EMPTY_ARGUMENTS

        ns = self.main_parser.parse_args(cmd_args)
        try:
            return ns.func(ns)
        except self.Error:
            return self.ExitCode.WRONG_PROCESS

    @staticmethod
    def run_program(exec_path, exec_args):
        cmd_line = '%s %s' % (exec_path, ' '.join(exec_args))
        print(cmd_line)
        return os.system(cmd_line)

    @staticmethod
    def run_python_shell(title, local_dict):
        code.interact(title, local=local_dict)

if __name__ == '__main__':
    command_manager = CommandManager()

    @command_manager.command(msg=dict(type=str, nargs='+'))
    def test(msg):
        print msg

    command_manager.run_command(['test', 'haha'])
