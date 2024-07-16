from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent,TextMessage,LocationMessage
import dotenv
import os
dotenv.load_dotenv()

line_bot_api=LineBotApi(os.getenv('TOKEN'))
app=Flask(__name__)
handler=WebhookHandler(os.getenv('SECRET'))
@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/callback',methods=['POST'])
def callback():
    signature=request.headers['X-Line-Signature']
    print(signature)
    body=request.get_data(as_text=True)
    handler.handle(body, signature)
    print(body)
    return ''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '20':
        line_bot_api.reply_message(event.reply_token,TextMessage(text=('他是閱!')))
    else:
        line_bot_api.reply_message(event.reply_token,TextMessage(text=('你是閱吧?')))
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    user_lat =event.message.latitude
    user_lon =event.message.longitude
    user_id =event.source.user_id
    s=f'{user_lat}:{user_lon}'
    line_bot_api.reply_message(event.reply_token,TextMessage(text=(s)))
if __name__ == '__main__':  
    app.run(port=1234)