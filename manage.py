#!/usr/bin/env python
# -*- coding:utf8 -*-
import os

from rosetta import db, app_factory
from rosetta import Environment

from pypm import ProjectManager


pm = ProjectManager()


def create_app():
    try:
        return app_factory.create_main_app()
    except Environment.Error:
        print "#### no active config"
        print "\t./mange.py switch_config "\
              "rosetta/data/$(TARGET)_config.yml"
        raise pm.Error('NO_ACTIVE_CONFIG')

@pm.command(package_names=dict(type=str, nargs='+', help='파이썬 패키지 이름'))
def install_package(package_names):
    """
    파이썬 패키지 설치 후 requirement.txt 를 갱신합니다.
    """

    if not package_names:
        raise pm.ArgumentError('NO_PACKAGE_NAME')

    for package_name in package_names:
        pm.run_system_command('pip', ['install', package_name])

    pm.run_system_command('pip', ['freeze', '> requirements.txt'])

@pm.command(config_file_path=dict(type=str, nargs=1, help='활성화 설정 파일 경로'))
def switch_config(config_file_path):
    """
    active_config.yml 설정 파일을 교체합니다.
    """

    pm.run_system_command('cp', [config_file_path, 'active_config.yml'])

@pm.command(script_file_path=dict(type=str, nargs=1, help='실행 스크립트 파일 경로'))
def run_script(script_file_path):
    """
    스크립트를 실행합니다.
    """
    script_dir_path, script_name = os.path.split(script_file_path) 

    import sys
    sys.path.append(script_dir_path)
    execfile(script_file_path, {'__name__': '__main__'})

@pm.command()
def run_shell():
    """
    쉘을 실행합니다. app 과 db 에 접근할 수 있습니다.
    """

    app = create_app()
    pm.run_python_shell('Rosetta Shell', local_dict=dict(app=app, db=db))

@pm.command()
def reset_all_databases():
    """
    모든 데이터 베이스를 리셋합니다. 만약에 대비해 패스워드를 확인합니다.
    전체 리셋 패스워드를 지정하지 않았다면 사용할 수 없습니다.
    """

    app = create_app()

    print "#### reset all databases"
    print "* database uri: %s" % app.config['SQLALCHEMY_DATABASE_URI']
    for key, value in sorted(app.config['SQLALCHEMY_BINDS'].iteritems()):
        print " * bind_key: %s uri:%s" % (key, value)

    print "* reset_all_password:", 
    config_password = app.config['RESET_ALL_PASSWORD']
    if not config_password:
        raise pm.Error('NO_PERMISSION_TO_RESET_ALL_PASSWORD')

    input_password = raw_input()
    if input_password != config_password:
        raise pm.Error('WRONG_RESET_ALL_PASSWORD')

    db.drop_all()
    db.create_all()

@pm.command(port=dict(type=int, default=5000, help="포트 번호"))
def run_server(port):
    """
    서버를 실행합니다. 기본 포트는 5000번입니다.
    """

    app = create_app()
    app.run_server(port=port)


if __name__ == '__main__':
    import sys
    pm.run_command(sys.argv[1:])
