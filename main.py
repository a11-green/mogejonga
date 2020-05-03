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

# AWS
import boto3

# DF,Graph,etc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import re # 正規表現


# Instance
app = Flask(__name__)
fname = "test.txt" # データベース

n1 = 0
n2 = 0
n3 = 0
n4 = 0

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
aws_s3_bucket        = os.environ['AWS_BUCKET']
s3 = boto3.resource("s3")
bucket = s3.Bucket(aws_s3_bucket)
s3_client = boto3.client('s3')

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

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
        message = event.message.text.split("\n") 
        n = [0,0,0,0]
        for j,line in enumerate(message):
            if line.count("help") != 0:
                # ヘルプ
                message = "[ Apps help ]\n"
                
            elif line.count("-") == 3 : 
                # 着順を入力したときの動作
                global data
                data = line.split("-")
                for i in range(4):
                    n[i] += int(data[i])
                message = "Are you sure?\n"
                message += " 1着 : {}回\n 2着 : {}回\n 3着 : {}回\n 4着 : {}回\n".format(data[0],data[1],data[2],data[3])

            elif line.count("円") == 1:
                # "円"を含む行は収支として計算する
                # さらに "+" or "勝"　を含めばプラス収支，
                # "-" or "負" を含めばマイナス収支とする
                global money
                money = re.sub("\\D", "", line)
                bucket.download_file(fname, fname)
                if (line.count("+") == 1) or (line.count("勝")) == 1:
                    money = abs(int(money))
                if (line.count("-") == 1) or (line.count("負")) == 1:
                    money = abs(int(money))*(-1.0)
                message += "{} 円".format(int(money))
                
                
            elif line.count("show") != 0 :
                # データをみるときの動作
                # "show" とうつと起動する
                message = "data URL\n"
                message += s3_client.generate_presigned_url(
                    ClientMethod = 'get_object',
                    Params       = {'Bucket': aws_s3_bucket, 'Key': fname},
                    ExpiresIn    = 10,
                    HttpMethod   = 'GET' )

            elif line.count("del") != 0:
                message = "deleted all !"
                with open(fname,'w') as f:
                    f.write("date,1st,2nd,3rd,4th,money\n")
                bucket.upload_file(fname, fname)

            elif line.count("stat") != 0:
                # 成績の統計処理等を行う
                # 選択肢をQuickReplyボタンで表示する
                # Postback変数によって処理を変える
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="どれにする?",
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="着順分布",       # ボタンに表示する文字
                                        text="着順分布をみせて",  # テキストとして送信する文字
                                        data="request_pie"     # Postback
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="合計",
                                        text="合計をみせて",
                                        data="request_sum"
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="データ",
                                        text="データをみせて",
                                        data="request_data"
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="収支履歴",
                                        text="収支の履歴をみせて",
                                        data="request_history"
                                    )
                                )
                            ]
                        )
                    )
                )
            
            


            else :
                text += "備考 : {}\n".format(line)
            
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text=message,
                actions=[
                    PostbackAction(
                        label='yes',
                        display_text='yes :)',
                        data='action:yes'
                    ),
                    MessageAction(
                        label='no',
                        text='no XD'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, messages=confirm_template_message)
        
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=e))
        pass

@handler.add(PostbackEvent)
def handle_postback(event):
    '''
    PostBackアクションがあったときの動作
    '''
    postbackdata = event.postback.data
    if postbackdata == "action:yes":
        # 着順を入力
        bucket.download_file(fname, fname)
        date = datetime.date.today()
        with open(fname,'a') as f:
            f.write("{},{},{},{},{}\n".format(date,data[0],data[1],data[2],data[3]))
        # bucket.upload_file(fname, fname)
        # 収支を入力
        with open(fname) as f:
            lines = f.readlines()
            tmp = lines[-1].rstrip('\n') + ",{}\n".format(money)
            lines[-1] = tmp
        with open(fname,'w') as f:
            for line in lines:
                f.write(line)
        bucket.upload_file(fname, fname)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="done!")
        )

    elif postbackdata == "request_pie":
        # 円グラフを表示
        bucket.download_file(fname, fname)
        df = pd.read_csv(fname,header=0)
        plt.clf()
        x = np.array([df["1st"].sum(),df["2nd"].sum(),df["3rd"].sum(),df["4th"].sum()])
        plt.pie(x)
        plt.legend()
        plt.savefig("pie.png")
        bucket.upload_file("pie.png", "pie.png")
        s3_image_url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params       = {'Bucket': aws_s3_bucket, 'Key': "pie.png"},
            ExpiresIn    = 10,
            HttpMethod   = 'GET'
        )
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url = s3_image_url,
                preview_image_url    = s3_image_url,
            )
        )
    elif postbackdata == "request_sum":
        # 合計を表示
        bucket.download_file(fname, fname)
        df = pd.read_csv(fname,header=0)
        x = np.array([df["1st"].sum(),df["2nd"].sum(),df["3rd"].sum(),df["4th"].sum()])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "{}-{}-{}-{}".format(x[0],x[1],x[2],x[3]))
        )
    elif postbackdata == "request_data":
        # データURLを表示
        message = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params       = {'Bucket': aws_s3_bucket, 'Key': fname},
            ExpiresIn    = 10,
            HttpMethod   = 'GET' 
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))



if __name__ == "__main__":
    print("hello")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
   
