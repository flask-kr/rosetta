# -*- coding:utf8 -*-
import os
import yaml
import logging

from logging.handlers import RotatingFileHandler


class Environment(object):
    SQLITE_SCHEMA = 'sqlite:///'
    SQLITE_URI_MEMORY = 'sqlite:///:memory:'

    class Error(Exception):
        pass

    def __init__(self, app=None):
        self.log_formatter = None

        if app:
            self.init_app(app)

    def __repr__(self):
        return '#### environments\n%s' % '\n'.join(sorted('* %s: %s' % (key, value) for key, value in self.app.config.items()))

    def __create_builtin_config_dict(self):
        config_dict = {}
        config_dict['DEBUG'] = True

        config_dict['LOG_DEBUG_FILE_PATH'] = os.path.expandvars("$PWD/var/logs/debug.log")
        config_dict['LOG_DEBUG_FILE_MAX_MB_SIZE'] = 100
        config_dict['LOG_DEBUG_BACKUP_COUNT'] = 2

        config_dict['LOG_INFO_FILE_PATH'] = os.path.expandvars("$PWD/var/logs/info.log")
        config_dict['LOG_INFO_FILE_MAX_MB_SIZE'] = 100
        config_dict['LOG_INFO_BACKUP_COUNT'] = 2

        config_dict['LOG_ERROR_FILE_PATH'] = os.path.expandvars("$PWD/var/logs/error.log")
        config_dict['LOG_ERROR_FILE_MAX_MB_SIZE'] = 100
        config_dict['LOG_ERROR_BACKUP_COUNT'] = 2

        config_dict['LOG_FORMAT'] = "%(asctime)-15s %(message)s"

        config_dict['SQLALCHEMY_DATABASE_URI'] = self.SQLITE_URI_MEMORY
        config_dict['SQLALCHEMY_BINDS'] = {} 
        config_dict['SQLALCHEMY_ECHO'] = True
        return config_dict

    def init_app(self, app):
        self.app = app
        self.app.config.update(self.__create_builtin_config_dict())

    def load_config_file(self, config_path):
        """
        설정 파일을 불러온다
        """

        expanded_config_path = os.path.expandvars(config_path)

        try:
            with open(expanded_config_path) as config_file:
                self.load_config_dict(yaml.load(config_file))
        except IOError as e:
            raise self.Error(
                'NOT_FOUND_CONFIG_FILE_PATH:%s' % expanded_config_path)

    def load_config_dict(self, config_dict):
        "설정 사전을 불러온다"
        if config_dict:
            for config_key, config_value in config_dict.iteritems():
                if config_key.endswith('_PATH'):
                    config_value = os.path.expandvars(config_value)
                elif config_key == 'SQLALCHEMY_DATABASE_URI':
                    config_value = os.path.expandvars(config_value)
                elif config_key == 'SQLALCHEMY_BINDS':
                    config_value = dict((key, os.path.expandvars(value)) for key, value in config_value.iteritems())

                self.app.config[config_key] = config_value

    def create_all(self):
        "모든 환경을 준비한다"

        self._create_log_formatter()
        self._create_debug_log()
        self._create_error_log()
        self._create_info_log()

        self._create_sqlalchemy_database(self.app.config['SQLALCHEMY_DATABASE_URI'])

        for bind_uri in self.app.config['SQLALCHEMY_BINDS'].values():
            self._create_sqlalchemy_database(bind_uri)

    def _create_log_formatter(self):
        self.log_formatter = logging.Formatter(self.app.config['LOG_FORMAT'])

    def _create_debug_log(self):
        if self.app.config['DEBUG']:
            self.__create_log_file(
                logging.DEBUG,
                self.app.config['LOG_DEBUG_FILE_PATH'],
                log_max_mb_size=self.app.config['LOG_DEBUG_FILE_MAX_MB_SIZE'],
                log_bak_count=self.app.config['LOG_DEBUG_BACKUP_COUNT'])

    def _create_info_log(self):
        self.__create_log_file(
            logging.INFO,
            self.app.config['LOG_INFO_FILE_PATH'],
            log_max_mb_size=self.app.config['LOG_INFO_FILE_MAX_MB_SIZE'],
            log_bak_count=self.app.config['LOG_INFO_BACKUP_COUNT'])

    def _create_error_log(self):
        self.__create_log_file(
            logging.ERROR,
            self.app.config['LOG_ERROR_FILE_PATH'],
            log_max_mb_size=self.app.config['LOG_ERROR_FILE_MAX_MB_SIZE'],
            log_bak_count=self.app.config['LOG_ERROR_BACKUP_COUNT'])

    def __create_log_file(
            self, log_level, log_file_path, log_max_mb_size, log_bak_count):

        log_dir_path, log_file_name = os.path.split(log_file_path)
        if not os.access(log_dir_path, os.R_OK):
            os.makedirs(log_dir_path)

        log_file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=log_max_mb_size * 1024 * 1024,
            backupCount=log_bak_count)

        log_file_handler.setLevel(log_level)

        if self.log_formatter:
            log_file_handler.setFormatter(self.log_formatter)

        self.app.logger.addHandler(log_file_handler)

    def _create_sqlalchemy_database(self, db_uri):
        if db_uri.startswith(self.SQLITE_SCHEMA):
            sqlite_dir_path, sqlite_file_path = os.path.split(db_uri[len(self.SQLITE_SCHEMA):])
            if sqlite_file_path == ':memory:':
                return
    
            # SQLite 상대 경로는 애매한 위치에 저장되므로 절대 경로 강제
            if not os.path.isabs(sqlite_dir_path):
                raise self.Error('NOT_ABSOLUTE_SQLITE_PATH:%s' % sqlite_dir_path)

            if not os.access(sqlite_dir_path, os.R_OK):
                os.makedirs(sqlite_dir_path)
            


