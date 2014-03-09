#!/usr/bin/env python
# -*- coding:utf8 -*-
import os

from framework import db
from application import app_factory

from urlparse import urlparse

from pypm import ProjectManager, FilterPattern

CONFIG_DIR_PATH = os.path.expandvars(
    '$PROJECT_DIR/etc/configs')

DEFAULT_CONFIG_FILE_PATH = os.path.expandvars(
    '$PROJECT_DIR/etc/configs/default_config.yml')

USER_CONFIG_FILE_PATH = os.path.expandvars(
    '$PROJECT_DIR/etc/configs/user_config.yml')

ALEMBIC_CONFIG_FILE_PATH = os.path.expandvars(
    '$PROJECT_DIR/alembic.ini')

ALEMBIC_REVISION_DIR_PATH = os.path.expandvars(
    '$PROJECT_DIR/alembic/versions')

EXAMPLE_DATA_LOCALE_DIR_PATH = os.path.expandvars(
    '$PROJECT_DIR/examples/data/locales')


def create_application(custom_config_file_path=USER_CONFIG_FILE_PATH):
    if os.access(custom_config_file_path, os.R_OK):
        return app_factory.create_application(
            DEFAULT_CONFIG_FILE_PATH,
            custom_config_file_path)
    else:
        print("NOT_FOUND_CUSTOM_CONFIG_FILE_PATH:%s" % custom_config_file_path)
        return app_factory.create_application(
            DEFAULT_CONFIG_FILE_PATH)


pm = ProjectManager()

@pm.command(package_names=dict(type=str, nargs='+', help='파이썬 패키지 이름'))
def install_package(package_names):
    """
    파이썬 패키지 설치 후 requirement.txt 를 갱신합니다.
    """

    if not package_names:
        raise pm.ArgumentError('NO_PACKAGE_NAME')

    for package_name in package_names:
        pm.run_system_command('pip', ['install', package_name])

    pm.run_system_command(
        'pip', ['freeze', '> ./requirements.txt'])


@pm.command(config_hint=dict(type=str, nargs=1, help='설정 파일 경로 혹은 접두어'))
def switch_config(config_hint):
    """
    유저 설정 파일을 교체합니다.
    """

    config_file_path = pm.smart_find_file_path(
        config_hint, base_dir_path=CONFIG_DIR_PATH)

    pm.run_system_command(
        'cp', [config_file_path, USER_CONFIG_FILE_PATH])


@pm.command(config_hint=dict(type=str, nargs=1, help='설정 파일 경로 혹은 접두어'))
def edit_config(config_hint):
    """
    설정 파일을 수정 합니다.
    """

    config_file_path = pm.smart_find_file_path(
        config_hint, base_dir_path=CONFIG_DIR_PATH)

    pm.run_system_command('$EDITOR', [config_file_path])


@pm.command(script_file_path=dict(type=str, nargs=1, help='스크립트 파일 경로'))
def run_script(script_file_path):
    """
    스크립트를 실행합니다.
    """
    script_dir_path, script_name = os.path.split(script_file_path) 

    import sys
    sys.path.append(script_dir_path)
    execfile(script_file_path, {'__name__': '__main__'})


@pm.command(config_hint=dict(type=str, flag='-c',
                             default=USER_CONFIG_FILE_PATH, help='설정 파일 경로'))
def run_shell(config_hint):
    """
    쉘을 실행합니다. app 과 db 에 접근할 수 있습니다.
    """

    config_file_path = pm.smart_find_file_path(
        config_hint, base_dir_path=CONFIG_DIR_PATH)

    app = create_application(config_file_path)
    pm.run_python_shell('Rosetta Shell', local_dict=dict(app=app, db=db))


@pm.command(config_hint=dict(type=str, flag='-c',
                             default=USER_CONFIG_FILE_PATH, help='설정 파일 경로'))
def reset_all_dbs(config_hint):
    """
    모든 데이터 베이스를 리셋합니다. 만약에 대비해 패스워드를 확인합니다.
    전체 리셋 패스워드를 지정하지 않았다면 사용할 수 없습니다.
    """

    config_file_path = pm.smart_find_file_path(
        config_hint, base_dir_path=CONFIG_DIR_PATH)

    app = create_application(config_file_path)

    print "#### reset all databases"
    print "* database uri: %s" % app.config['SQLALCHEMY_DATABASE_URI']
    for key, value in sorted(app.config['SQLALCHEMY_BINDS'].iteritems()):
        print " * bind_key: %s uri:%s" % (key, value)

    print "* reset_all_password:", 
    config_password = app.config['DB_RESET_ALL_PASSWORD']
    if not config_password:
        raise pm.Error(
            'NOT_FOUND_TO_DB_RESET_ALL_PASSWORD_IN_CONFIG_PATH:' +
            config_file_path)

    input_password = raw_input()
    if input_password != config_password:
        raise pm.Error('WRONG_DB_RESET_ALL_PASSWORD')

    db.drop_all()
    db.create_all()

    from alembic.config import Config
    alembic_config = Config(ALEMBIC_CONFIG_FILE_PATH)

    from alembic import command
    command.stamp(alembic_config, "head")


@pm.command(config_hint=dict(type=str, flag='-c',
                             default=USER_CONFIG_FILE_PATH, help='설정 파일 경로'))
def connect_db(config_hint):
    config_file_path = pm.smart_find_file_path(
        config_hint, base_dir_path=CONFIG_DIR_PATH)

    app = create_application(config_file_path)
    db_uri = urlparse(app.config['SQLALCHEMY_DATABASE_URI'])
    if db_uri.scheme == 'sqlite':
        pm.run_system_command('sqlite3', [db_uri.path])
    else:
        print 'NOT_SUPPORT_DB_SCHEME:', db_uri.scheme


@pm.command(title=dict(type=str, nargs=1, help='DB 리비전 제목'))
def make_db_rev(title):
    pm.run_system_command('alembic', ['revision', '--autogenerate', '-m', title])


@pm.command()
def list_db_revs():
    pm.run_system_command('ls', [ALEMBIC_REVISION_DIR_PATH])


@pm.command(db_rev_hint=dict(type=str, nargs=1, help='DB 리비전 파일 이름 접두어'))
def edit_db_rev(db_rev_hint):
    db_rev_file_path = pm.smart_find_file_path(
        db_rev_hint, base_dir_path=ALEMBIC_REVISION_DIR_PATH)

    pm.run_system_command('$EDITOR', [db_rev_file_path])


@pm.command(db_rev_hint=dict(type=str, nargs=1, help='DB 리비전 파일 이름 접두어'))
def remove_db_rev(db_rev_hint):
    db_rev_file_path = pm.smart_find_file_path(
        db_rev_hint, base_dir_path=ALEMBIC_REVISION_DIR_PATH)

    pm.remove_file(db_rev_file_path, is_testing=False)


@pm.command(db_rev_hint=dict(type=str, nargs=1, help='DB 리비전 파일 이름 접두어'))
def apply_db_rev(db_rev_hint):
    db_rev_file_path = pm.smart_find_file_path(
        db_rev_hint, base_dir_path=ALEMBIC_REVISION_DIR_PATH)

    db_rev_file_name = os.path.basename(db_rev_file_path).split('_')[0]
    pm.run_system_command('alembic', ['upgrade', db_rev_file_name])


@pm.command(config_hint=dict(type=str, flag='-c',
                             default=USER_CONFIG_FILE_PATH,
                             help='설정 파일 경로'),
            port=dict(type=int, flag='-p', default=5000, help="포트 번호"))
def run_server(config_hint, port):
    """
    서버를 실행합니다. 기본 포트는 5000번입니다.
    """

    config_file_path = pm.smart_find_file_path(
        config_hint, base_dir_path=CONFIG_DIR_PATH)

    app = create_application(config_file_path)
    app.run(port=port)


@pm.command(config_hint=dict(type=str, flag='-c',
                             default=USER_CONFIG_FILE_PATH,
                             help='설정 파일 경로'),
            locale_dir_path=dict(type=str, flag='-l',
                                 default=EXAMPLE_DATA_LOCALE_DIR_PATH,
                                 help='로케일 디렉토리 경로'),
            po_hints=dict(type=str, nargs='+', help='번역 파일 경로들'))
def insert_po(config_hint, locale_dir_path, po_hints):
    """
    po 번역 파일을 데이터 베이스에 추가합니다.
    """
    config_file_path = pm.smart_find_file_path(
        config_hint, base_dir_path=CONFIG_DIR_PATH)

    create_application(config_file_path)

    import polib
    import email.utils
    from urlparse import urlparse, urlunsplit

    po_file_paths = list(pm.find_file_path_iter(
        base_dir_path=locale_dir_path,
        filter_file_name=FilterPattern(po_hints)))

    from application.models import Site, Page, Sentence
    from application.models import User, Translation, Selection
    for po_file_path in po_file_paths:
        print "insert_database_from_po_file:", po_file_path

        po = polib.pofile(po_file_path)
        site_url = urlparse(po.metadata['Project-Id-Version'])
        site, is_site_created = Site.query\
            .get_or_create(url=urlunsplit(
            (site_url.scheme, site_url.netloc, '', '', '')))

        page, is_page_created = Page.query\
            .get_or_create(path=site_url.path, site=site)

        user_name, user_email = email.utils\
            .parseaddr(po.metadata['Last-Translator'])
        user, is_user_created = User.query\
            .get_or_create(uid=user_email, name=user_name)

        for entry in po:
            sentence, is_sentence_created = Sentence.query\
                .get_or_create(text=entry.msgid, page=page)

            translation, is_translation_created = Translation.query\
                .get_or_create(text=entry.msgstr,
                               sentence=sentence,
                               user=user)

            selection, is_selection_created = Selection.query\
                .get_or_create(translation=translation,
                               sentence=sentence,
                               user=user)

        db.session.commit()

if __name__ == '__main__':
    if 0:
        pm.run_command(['insert_po', '*liks*.po'])
    else:
        import sys
        pm.run_command(sys.argv[1:])
