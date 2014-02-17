#!/usr/bin/env python
# -*- coding:utf8 -*-
from rosetta import CommandManager

command_manager = CommandManager()

@command_manager.command(package_names=dict(type=str, nargs='+', help='python package names'))
def install_package(package_names):
    if not package_names:
        raise CommandArgumentError('NO_PACKAGE_NAME')

    for package_name in package_names:
        command_manager.run_program('pip', ['install', package_name])

    command_manager.run_program('pip', ['freeze', '> requirements.txt'])

@command_manager.command(config_path=dict(type=str, nargs=1, help='active config path'))
def switch_config(config_path):
    command_manager.run_program('cp', [config_path[0], 'active_config.yml'])

@command_manager.command()
def run_shell():
    server_manager = command_manager.server_manager
    command_manager.run_python_shell('Rosetta Shell', local_dict=dict(app=server_manager.app, db=server_manager.db))

@command_manager.command()
def reset_all_databases():
    server_manager = command_manager.server_manager

    print "#### reset all databases"
    print "* database uri: %s" % server_manager.app.config['SQLALCHEMY_DATABASE_URI']
    for key, value in sorted(server_manager.app.config['SQLALCHEMY_BINDS'].iteritems()):
        print " * bind_key: %s uri:%s" % (key, value)

    print "* reset_all_password:", 
    password = raw_input()
    if password != server_manager.app.config['RESET_ALL_PASSWORD']:
        raise server_manager.Error('WRONG_DROP_ALL_PASSWORD')

    server_manager.reset_all_databases()

@command_manager.command(port=dict(type=int, default=5000, help="server port"))
def run_server(port):
    command_manager.server_manager.run_server()

if __name__ == '__main__':
    import sys
    command_manager.run_command(sys.argv[1:])
