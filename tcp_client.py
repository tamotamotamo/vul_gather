#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

target_host = "192.168.11.201"
target_port = 9999

# ソケットオブジェクトの作成
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# サーバーへ接続
client.connect((target_host,target_port))

# データの送信
client.send("GET / HTTP/1.1\r\nHi! from MacBook.\r\n\r\n")

# データの受信
response = client.recv(4096)

print response
