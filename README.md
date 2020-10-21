# Django/PostgreSQL/Docker/TravisCI/HEROKU
## DjangoとPostgreSQLをdocker-composeで起動(local開発)

### 1,Dockerfile、docker-compose.yml、Pipfile、Pipfile.lock、runtime.txt、Procfileを作業フォルダ配下に設置

### 2,pipenvで仮想環境を構築
```
$pip install pipenv
$pipenv install
```

### 3,Djangoプロジェクト作成
```
$pipenv shell
django-admin startproject プロジェクト名 .
exit
```

### 4,プロジェクト内のsettings.pyを変更
```
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

WSGI_APPLICATION = 'project.wsgi.application'

#STATIC_URLの上に追加
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#STATIC_URLの下に追加
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

#DEBUG = Trueにすると
DEBUG = False

try:
    from config.local_settings import *
except ImportError:
    pass

if not DEBUG:
    import django_heroku
    django_heroku.settings(locals())
```
### 5,プロジェクトのルートディレクトリにstaticディレクトリを作成し、その中に.gitkeepファイルを作成
- herokuで静的ファイルを配信するのにstaticディレクトリを作成しなければならないが、<br>
　空のディレクトリはgitで管理できないため、.gitkeepという空のファイルを作成
 
### 6,開発環境用の設定ファイルを作成
- settiongs.pyと同じディレクトリにlocal_settings.pyを作成
プロジェクトフォルダ/local_settings.py
```
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

ALLOWED_HOSTS = []

DEBUG = True

```

### (ローカル開発)docker-composeでコンテナ起動
```
$docker-compose up --build -d　#コンテナ起動
$docker-compose exec web python manage.py migrate #DBの初期化
$docker-compose exec web python manage.py createsuperuser #スーパーユーザーの作成
$docker-compose ecec web python manage.py runserver 0.0.0.0:8000 #サーバーの起動
```
※いちいちdocker-compose exec web　を打つのがめんどくさい場合は下記コマンドでコンテナ内へ入ると
以降python manage.py ~~~　からでOKになる
```
$docker-compose exec web bash
```
### (ローカル開発)localhostにアクセス
http://localhost:8000 にアクセスし、welcome画面が出ればOK
http://localhost:8000/admin にアクセスし、必要事項を入力

### CD/CIの設定
## heroku clを自分の環境にインストール
## TravisCIとHEROKUの設定
＜TravisCI＞
Environment Variablesに以下項目を追加
・HEROKU_API_KEY 
・HEROKU_APP_NAME →heroku app名
・HEROKU_USERNAME　→_(アンダースコア)

＜heroku＞
Config Varsに以下項目を追加
・DATABASE_PASSWORD →docker-compose.ymlで設定したもの
・SECRET_KEY　→settiongs.pyにあるSECRET_KEYをcopy

## デプロイ
$ git add .
$ git commit -m 'コメント'
$ git push origin master

## TravisCIのサイトでlogを確認し、デプロイが完了していればherokuでOpen appする


＊ディレクトリ構造、settings.pyの設定はこのgitリポジトリで確認してください



