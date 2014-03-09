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

#### 로컬 서버 실행

    (rosetta)$ ./manage.py switch_config etc/configs/local_sqlite_config.yml
    (rosetta)$ ./manage.py run_server


