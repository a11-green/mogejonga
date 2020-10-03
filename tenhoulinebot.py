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
from datetime import datetime, timedelta, timezone

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
import os
import pprint

# AWS
import boto3

# harukis module
import harukis.syukei as sy
tools = sy.Tools()


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

# AWS Instance
aws_s3_bucket = os.environ['AWS_BUCKET']
s3 = boto3.resource("s3")
bucket = s3.Bucket(aws_s3_bucket)
s3_client = boto3.client('s3')

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

#

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
        
        # Graph Plot
        elif message.count("ぐらふ") != 0:
            # import download4
            # import graph

            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="どれにする?",
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="点",       # ボタンに表示する文字
                                        text="点数推移を見せて",  # テキストとして送信する文字
                                        data="request_point"     # Postback
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="チップ",
                                        text="チップ推移をみせて",
                                        data="request_tip"
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="Rating",
                                        text="Ratingをみせて",
                                        data="request_rating"
                                    )
                                )
                            ]
                        )
                    )
                )


             

        # Summary
        elif message.count("しゅうけい") != 0:
            try:
                option = message.split("")[1]
            except:
                option = "4"
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="どれにする?",
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="収支",       # ボタンに表示する文字
                                        text="収支を見せて",  # テキストとして送信する文字
                                        data="request_sum"     # Postback
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="着順",
                                        text="着順をみせて",
                                        data="request_rank"
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="チーム",
                                        text="チーム成績をみせて",
                                        data="request_team"
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="Today",
                                        text="今日の結果をみせて",
                                        data="request_today"
                                    )
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label="Test",
                                        text="{} {}".format(message,option),
                                        data="request_test:{}".format(option)
                                    )
                                )
                            ]
                        )
                    )
                )

        # おまけ
        elif message.count("もげ") != 0:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "じょんが")
            )

        elif message.count("だーー") != 0:
           line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url = "https://amd.c.yimg.jp/im_siggaxoZr2KCiBiG_WuqdyfQwg---x900-y863-q90-exp3h-pril/amd/20200619-06190063-sph-000-2-view.jpg",
                    preview_image_url    = "https://amd.c.yimg.jp/im_siggaxoZr2KCiBiG_WuqdyfQwg---x900-y863-q90-exp3h-pril/amd/20200619-06190063-sph-000-2-view.jpg"
                )
            )
        elif message.count("ブリテン") != 0:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "イギリスかよ")
            )

    


    except:
        import traceback
        print("errrrrrrrrrror")
        traceback.print_exc()
        


@handler.add(PostbackEvent)
def handle_postback(event):
    '''
    PostBackアクションがあったときの動作
    '''
    import download4
    import summary
    import graph
    import rating.calc_rating as cr

    postbackdata = event.postback.data
    if postbackdata == "request_point":
        tools.plot_summary(season="4")
        bucket.upload_file("scores.png", "scores.png")
        s3_image_url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params       = {'Bucket': aws_s3_bucket, 'Key': "scores.png"},
            ExpiresIn    = 600,
            HttpMethod   = 'GET'
        )

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url = s3_image_url,
                preview_image_url    = s3_image_url,
            )
        )
        # download4.upload("test.png","/graph.png")  

    if postbackdata == "request_tip":
        download4.download("/logvol4.txt","log.txt")
        graph.graph_plot(tip=True)
        bucket.upload_file("test2.png", "test2.png")
        s3_image_url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params       = {'Bucket': aws_s3_bucket, 'Key': "test2.png"},
            ExpiresIn    = 600,
            HttpMethod   = 'GET'
        )

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url = s3_image_url,
                preview_image_url    = s3_image_url,
            )
        )
        download4.upload("test2.png","/graph2.png")    

    elif postbackdata == "request_rating":

        download4.download("/logvol1.txt","rating/logvol1.txt")
        download4.download("/logvol2.txt","rating/logvol2.txt")
        download4.download("/logvol3.txt","rating/logvol2.txt")
        download4.download("/logvol4.txt","rating/logvol4.txt")
        
        initial_rating,initial_games,initial_rating_history = cr.initialize_rating("rating/rating.txt")
        r,g,h = cr.calc_rating(initial_rating,initial_games,initial_rating_history,"rating/logvol1.txt",tip=False)
        r,g,h = cr.calc_rating(r,g,h,"rating/logvol2.txt",tip=True)
        r,g,h = cr.calc_rating(r,g,h,"rating/logvol3.txt",tip=True)
        r,g,h = cr.calc_rating(r,g,h,"rating/logvol4.txt",tip=True)
        cr.rating_plot(h)

        bucket.upload_file("rating.png", "rating.png")
        s3_image_url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params       = {'Bucket': aws_s3_bucket, 'Key': "rating.png"},
            ExpiresIn    = 600,
            HttpMethod   = 'GET'
        )

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url = s3_image_url,
                preview_image_url    = s3_image_url,
            )
        )
        download4.upload("rating.png","/rating.png")    


    elif postbackdata == "request_sum":
        text = tools.summary(season="5")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = text))
    
    elif postbackdata == "request_today":
        text = tools.today(season="5")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = text)) 

    elif postbackdata == "request_rank":
        text = tools.rank(season="5")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = text))

    elif postbackdata == "request_team":
        text = tools.team(season="5")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = text))

    elif postbackdata.count("request_test") != 0:
        option = postbackdata.split(":")[1]
        text = tools.summary(season=option)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = postbackdata))
        
         
    


if __name__ == "__main__":
    print("hello")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
   










