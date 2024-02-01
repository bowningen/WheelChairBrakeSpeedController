# WheelChairBreakeSpeedController
## Usage
使い方  

##詳細

お使いの環境にpyserialをインストールして、config.iniのarduino1,arduino2をお使いのArduinoそれぞれ(1はホール素子側、2はモーター側)のシリアルポート番号に設定します(ls /dev/tty*)

その後実行したら何とかなるはずです

多分...

<div id="top"></div>

## 使用技術一覧

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- フロントエンドのフレームワーク一覧 -->
  <!-- バックエンドのフレームワーク一覧 -->
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Arduino-00979D.svg?logo=arduino&style=for-the-badge">
  <!-- ミドルウェア一覧 -->
  <!-- インフラ一覧 -->
</p>

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [開発環境構築](#開発環境構築)
5. [トラブルシューティング](#トラブルシューティング)

<!-- プロジェクト名を記載 -->

## プロジェクト名

React、DRF、Terraform のテンプレートリポジトリ

<!-- プロジェクトについて -->

## プロジェクトについて


このプログラムはLinux版Python3系向けです

Arduino2台とシリアル通信を行い、片方に接続しておいたホール素子(あるいは他のセンサー)からの電圧が変動する間隔から物体の回転速度を検出し、その速度に応じてもう一台のArduinoに接続したサーボモーターを動かすプログラムです。

<!-- プロジェクトの概要を記載 -->

  <p align="left">
    <br />
    <!-- プロジェクト詳細にBacklogのWikiのリンク -->
    <a href="Backlogのwikiリンク"><strong>プロジェクト詳細 »</strong></a>
    <br />
    <br />

<p align="right">(<a href="#top">トップへ</a>)</p>

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.11.4     |
| pyserial              | 4.2.1      |
| time                  | 1.3.6      |
| os                    | 3.14.0     |
| logging               | 8.0        |
| configparser          | 16.17.0    |
| multiprocessing       | 18.2.0     |
| Arduino SDK           | 13.4.6     |
| servo                 | 1.3.6      |

<p align="right">(<a href="#top">トップへ</a>)</p>


## 開発環境構築

<!-- コンテナの作成方法、パッケージのインストール方法など、開発環境構築に必要な情報を記載 -->

### コンテナの作成と起動

.env ファイルを以下の環境変数例と[環境変数の一覧](#環境変数の一覧)を元に作成

.env
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=django-db
MYSQL_USER=django
MYSQL_PASSWORD=django
MYSQL_HOST=db
MYSQL_PORT=3306
SECRET_KEY=django
DJANGO_SETTINGS_MODULE=project.settings.local


.env ファイルを作成後、以下のコマンドで開発環境を構築

make prepare

### 動作確認

http://127.0.0.1:8000 にアクセスできるか確認
アクセスできたら成功

### コンテナの停止

以下のコマンドでコンテナを停止することができます

make down

## 設定項目の一覧

### setting.ini
| 変数名                 | 役割                                      | デフォルト値                       | DEV 環境での値                           |
| ---------------------- | ----------------------------------------- | ---------------------------------- | ---------------------------------------- |
| MYSQL_ROOT_PASSWORD    | MySQL のルートパスワード（Docker で使用） | root                               |                                          |
| MYSQL_DATABASE         | MySQL のデータベース名（Docker で使用）   | django-db                          |                                          |
| MYSQL_USER             | MySQL のユーザ名（Docker で使用）         | django                             |                                          |
| MYSQL_PASSWORD         | MySQL のパスワード（Docker で使用）       | django                             |                                          |
| MYSQL_HOST             | MySQL のホスト名（Docker で使用）         | db                                 |                                          |
| MYSQL_PORT             | MySQL のポート番号（Docker で使用）       | 3306                               |                                          |
| SECRET_KEY             | Django のシークレットキー                 | secretkey                          | 他者に推測されないランダムな値にすること |
| ALLOWED_HOSTS          | リクエストを許可するホスト名              | localhost 127.0.0.1 [::1] back web | フロントのホスト名                       |
| DEBUG                  | デバッグモードの切り替え                  | True                               | False                                    |
| TRUSTED_ORIGINS        | CORS で許可するオリジン                   | http://localhost                   |                                          |
| DJANGO_SETTINGS_MODULE | Django アプリケーションの設定モジュール   | project.settings.local             | project.settings.dev                     |

### holeRead_MTOnly.ino
| 変数名                 | 役割                                      | デフォルト値                       | DEV 環境での値                           |
| ---------------------- | ----------------------------------------- | ---------------------------------- | ---------------------------------------- |
| MYSQL_ROOT_PASSWORD    | MySQL のルートパスワード（Docker で使用） | root                               |                                          |
| MYSQL_DATABASE         | MySQL のデータベース名（Docker で使用）   | django-db                          |                                          |
### holeRead_HlOnly.ino
| 変数名                 | 役割                                      | デフォルト値                       | DEV 環境での値                           |
| ---------------------- | ----------------------------------------- | ---------------------------------- | ---------------------------------------- |
| MYSQL_ROOT_PASSWORD    | MySQL のルートパスワード（Docker で使用） | root                               |                                          |
| MYSQL_DATABASE         | MySQL のデータベース名（Docker で使用）   | django-db                          |                                          |


### コマンド一覧

| Make                | 実行する処理                                                            | 元のコマンド                                                                               |
| ------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| make prepare        | node_modules のインストール、イメージのビルド、コンテナの起動を順に行う | docker-compose run --rm front npm install<br>docker-compose up -d --build                  |

## トラブルシューティング

### .env: no such file or directory

pyserialではなくserialをインストールしている可能性があります。
serialをインストールしている、あるいは両方をインストールしている場合、serialをアンインストールしてください。

###

指定しているシリアルポートが間違っている可能性があります。
Arduinoを抜き差ししつつ" ls /dev/tty* "を実行して特定を行ったうえで、setting.iniに記述してください。

### 2.2.41がfloatに直せない等のエラーが出ている。

わかりません。
なぜなのか聞きたいです。
そのまま進んだはずですが...

### 実行した直後に〇等のエラーが出て停止する

わかりません。
この上のエラーと同様、シリアル通信関連で何か間違ってるみたいです。
何度か実行すれば通るので Ctrl+Z で強制終了させ、もう一度実行してください。

## 諸注意
当プログラムを利用した事によるいかなる損害も一切の責任を負いません。  
自己の責任の上で使用して下さい。  

<p align="right">(<a href="#top">トップへ</a>)</p>
