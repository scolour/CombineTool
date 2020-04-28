# CombineTool
Traktorのbroadcastingからアーティスト名と楽曲名を取得してテキストファイルに出力する時の、テキスト出力する側のツール

## これは何
Traktorで再生中の曲情報ってbroadcastingの機能を使って出力することができます。  
出力された曲情報はIcecastサーバ(ストリーミング)を使って受信することができます。  
Icecastサーバは楽曲情報を受信するとXSLファイルに出力しているので、そのXSLファイルから楽曲情報を取得、テキストファイルに出力するツールがこれです。  
ちなみにIcecastサーバはローカルのwindowsやmacの環境上にも建てることができるので、必ずしもネットワークを必要とはしません。  

## ツールを使うにあたっての前提
Traktorを使用していること  
同じLAN内にIcecastサーバを立てていること  
Traktorのbroadcastingの設定ができていてIcecastサーバで受信できていること

参考：KAI-YOU 開発者ブログ 様
https://kai-you-tech.hatenablog.com/entry/2019/11/19/190107

## その他
pythonの勉強がてらに作ったので不具合については許してください。
要望とかは気が向いたときに対応できれば…
