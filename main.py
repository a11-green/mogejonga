# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

'''
## references
1. Line Bot API
* [公式-python](https://github.com/line/line-bot-sdk-python/blob/master/README.rst_)
* https://keinumata.hatenablog.com/entry/2018/05/08/122348
* [bottun](https://qiita.com/shimayu22/items/c599a94dfa39c6466dfa)
* [](https://dev.classmethod.jp/etc/line-messaging-api-action-object/)
* [避難場所LINE bot](https://qiita.com/lovemysoul/items/5ad818220d65b74351a5)
  このサイトまじでわかりやすい．神．

2. DB,SQL
* https://baku1101.hatenablog.com/entry/2019/04/15/185003
* https://qiita.com/jacob_327/items/ec7d2223010ad4a0dd38

3. Python x S3(AWS)
* https://www.casleyconsulting.co.jp/blog/engineer/2861/

4. Heroku
* [環境変数の設定](https://qiita.com/colorrabbit/items/18db3c97734f32ebdfde)
* [Heroku x Linebot API](https://miyabi-lab.space/blog/21)


'''

# system
import os
import sys
import datetime
from argparse import ArgumentParser

# Web FlameWork
from flask import Flask, request, abort

# Line API
from linebot import (
    LineBotApi, WebhookHandler
    )
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    PostbackEvent, 
    TextMessage, 
    TextSendMessage,
    ButtonsTemplate,
    URIAction,
    PostbackAction,
    MessageAction,
    ImageSendMessage,
    ConfirmTemplate,
    TemplateSendMessage,
    QuickReply,
    QuickReplyButton
)



# DF,Graph,etc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import re # 正規表現

import pprint

# Google Drive API
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# Flask Web App Instance
app = Flask(__name__)


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


# PREPARE LINE messaging API Instance
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

'''
以下アクション時の応答処理
'''

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    '''
    テキストメッセージが送られてきたときの処理
    '''
    try:
        message = event.message.text
        if message.count("新垣結衣") != 0:   
            text = "plotting...\n"
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url = "https://orionfdn.org/wp-content/uploads/2018/12/WS000011-69.jpg",
                    preview_image_url    = "https://orionfdn.org/wp-content/uploads/2018/12/WS000011-69.jpg"
                )
            )
        elif message.count("グラフ") != 0:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text="graph")
                )
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            file_id = drive.ListFile({'q': 'title = "log.txt"'}).GetList()[0]['id']
            f = drive.CreateFile({'id': file_id})
            f.GetContentFile('download.txt')
    except:
        print("errrrrrrrrrror")
    


if __name__ == "__main__":
    print("hello")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
   
