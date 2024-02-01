# WheelChairBreakeSpeedController


## 目次

1. [概要](#概要)
2. [使用技術一覧](#使用技術一覧)
3. [詳細](#詳細)
4. [環境](#環境)
5. [実行方法](#実行方法)
6. [設定項目の一覧](#設定項目の一覧)
7. [コマンド一覧](#コマンド一覧)
8. [トラブルシューティング](#トラブルシューティング)
9. [諸注意](#諸注意)
10. [更新履歴](#更新履歴)


## 概要

このプログラムはLinux版Python3系向けです

Arduino2台とシリアル通信を行い、片方に接続しておいたホール素子(あるいは他のセンサー)からの電圧が変動する間隔から物体の回転速度を検出し、その速度に応じてもう一台のArduinoに接続したサーボモーターを動かすプログラムです。

<div id="top"></div>


## 使用技術一覧
<p style="display: inline">
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Arduino-00979D.svg?logo=arduino&style=for-the-badge">
</p>


## プロジェクト名

ホール素子を用いた介助式車椅子の自動速度制御装置の開発(奈良高等学校 2024)

<!-- プロジェクトについて -->

## プロジェクトについて

  <p align="left">
    <br />
    <!-- プロジェクト詳細にBacklogのWikiのリンク -->
    <a href="Backlogのwikiリンク"><strong>プロジェクト詳細 »</strong></a>
    <br />
    <br />

<p align="right">(<a href="#top">トップへ</a>)</p>


## 詳細


お使いの環境にpyserialをインストールして、config.iniのarduino1,arduino2をお使いのArduinoそれぞれ(1はホール素子側、2はモーター側)のシリアルポート番号に設定します(ls /dev/tty*)

その後実行したら何とかなるはずです

多分...


## 動作環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->
| OS　　　　　　　　　  | バージョン |
| --------------------- | ---------- |
| Ubuntu                | 22.04.3    |

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.10.12    |
| pyserial              | 3.5        |
| Arduino IDE           | 1.8.18     |
| servo                 | 1.2.1      |


## 必須ライブラリ
pyserial (Python)
servo (Arduino)


## 開発環境構築

あらかじめお使いのPCにPythonとArduino IDEをインストール、その後、各モジュールの最新版をpip等でインストールしてください。
なお、servoライブラリはArduino IDE側の「ライブラリの管理」からインストールしてください。

<p align="right">(<a href="#top">トップへ</a>)</p>

## 実行方法


※実行時にエラーが出る場合が多いですが、シリアル通信関連で例外が発生していることがほとんどなので、何度かCtrl+Zで強制終了して再実行を繰り返していると動作するはずです（V1.1.0で修正予定）


## 設定項目の一覧

### ・config.ini
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

### ・holeRead_MTOnly.ino
| 変数名                 | 役割                                      | デフォルト値                       | DEV 環境での値                           |
| ---------------------- | ----------------------------------------- | ---------------------------------- | ---------------------------------------- |
| MYSQL_ROOT_PASSWORD    | MySQL のルートパスワード（Docker で使用） | root                               |                                          |
| MYSQL_DATABASE         | MySQL のデータベース名（Docker で使用）   | django-db                          |                                          |
### ・holeRead_HlOnly.ino
| 変数名                 | 役割                                      | デフォルト値                       | DEV 環境での値                           |
| ---------------------- | ----------------------------------------- | ---------------------------------- | ---------------------------------------- |
| MYSQL_ROOT_PASSWORD    | MySQL のルートパスワード（Docker で使用） | root                               |                                          |
| MYSQL_DATABASE         | MySQL のデータベース名（Docker で使用）   | django-db                          |                                          |


### コマンド一覧

| Make                | 実行する処理                                                            | 元のコマンド                                                                               |
| ------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| make prepare        | node_modules のインストール、イメージのビルド、コンテナの起動を順に行う | docker-compose run --rm front npm install<br>docker-compose up -d --build                  |

## トラブルシューティング

### AttributeError: module 'serial' has no attribute 'Serial'

pyserialではなくserialをインストールしている可能性があります。
serialをインストールしている、あるいは両方をインストールしている場合、serialをアンインストールしてください。

### No such file or directory: '/dev/tty****'

指定しているシリアルポートが間違っている可能性があります。
Arduinoを抜き差ししつつ" ls /dev/tty* "を実行して特定を行ったうえで、config.iniに記述してください。

### 2.2.41がfloatに直せない等のエラーが出ている

わかりません。
なぜなのか聞きたいです。
シリアル通信中にいらないものを受け取っているようです。
まぁこのエラーはそのまま進んだはずですが...

### 実行した直後に〇等のエラーが出て停止する

わかりません。
上のエラーと同様、シリアル通信関連で何か間違ってるみたいです。
何度か実行すれば通るので Ctrl+Z で強制終了させ、もう一度実行してください。

## 諸注意
当プログラムを利用した事によるいかなる損害も一切の責任を負いません。  
自己の責任の上で使用して下さい。  

<p align="right">(<a href="#top">トップへ</a>)</p>

## 更新履歴
・v1.0.0 : リリース
