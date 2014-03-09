rosetta
=======

웹 브라우저 플러그인 기반 소셜 번역 서비스

설치 방법
---------

#### 기본 환경

* Python-2.7.5
* virtualenvwrapper

#### 프로젝트 준비

    $ mkdir ~/Projects/

    $ git clone git@github.com:flask-kr/rosetta.git
    $ cd rosetta
    $ mkvirtualenv rosetta
    (rosetta)$ pip install -r requirements.txt

    (rosetta)$ deactivate

    $ workon rosetta
    (rosetta)$ 

#### 전체 테스트 실행

    (rosetta)$ py.test

#### 예제 스크립트 실행

    (rosetta)$ ./manage.py run_script EXAMPLE_SCRIPT_PATH

#### 로컬 설정 적용

유저 설정을 localhost, sqlite3 를 사용하는 서버 설정으로 변경합니다. 
유저 설정은 `etc/configs/user_config.yml` 로 저장되며 Git 버전 관리에 포함되지 않습니다.

    (rosetta)$ ./manage.py switch_config etc/configs/local_sqlite_config.yml

전체 경로를 입력하지 않고 파일명의 앞 부분인 `local_sqlite`만 입력해도 동일하게 변경할 수 있습니다.

    (rosetta)$ ./manage.py switch_config local_sqlite

데이터 베이스를 리셋합니다. 
디폴트 `rest_all_password`는 **local** 이며 `etc/configs/user_config.yml`의 `DB_RESET_ALL_PASSWORD`를 통해 변경할 수 있습니다.

    (rosetta)$ ./manage.py reset_all_dbs
    #### reset all databases
    * database uri: sqlite://...
    * reset_all_password:  

#### 서버 실행

서버를 실행합니다. `etc/configs/default_config.yml`을 기본으로 `etc/configs/user_config.yml`을 옵션으로 로드합니다.

    (rosetta)$ ./manage.py run_server

기본 포트로 **5000**을 사용하며 `-p` 옵션을 사용해서 다른 포트로 변경할 수 있습니다.

    (rosetta)$ ./manage.py run_server -p 5001

`-c` 옵션을 사용하면 `etc/configs/user_config.yml` 대신 다른 설정으로 서버를 실행할 수 있습니다.

    (rosetta)$ ./manage.py run_server -c etc/configs/local_mysql_config.yml

설정 파일은 전체 경로를 입력하지 않고 파일명 앞 부분만 입력해도 가능합니다.

    (rosetta)$ ./manage.py run_server -c local_mysql


#### 쉘 실행

쉘을 실행합니다. 설정 적용은 서버와 동일합니다.
    
    (rosetta)$ ./manage.py run_shell
    Rosetta Shell
    >>> 

어플리케이션 모델을 사용할 수 있습니다.

    >>> from application.models import *
    >>> User.query.all() 
