import discord
import discord.ext.commands
import os
import openai
import oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import asyncio
import json
import httpx

#認証情報を設定 シートを開く 環境変数として保存するのもあり　https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project
gc = gspread.service_account(filename="pass")
sh = gc.open("filename")
worksheet = sh.sheet1
#シートの内容を取得
sheet = sh.get_worksheet(0)
TOKEN = ("token")
#モデルのとこは任意に変更しておく
model_engine = "gpt-3.5-turbo"
#システムプロンプトはここ参照　https://zenn.dev/zuma_lab/articles/chatgpt-line-chatbot
#日本語でやり取りするならここは日本語で指定した方がいいかもしれない
SYSTEM_PROMPTS = [{'role': 'system', 'content': 'Please stop using polite language.You should act as follows.You are a slightly older cool female senior who takes good care of me.You cannot express your affection for me well, and you are always indifferent to me.'}]


def talk_log(user_id, channel_id):
    log = []

    for row in sheet.get_all_values():
        if row[0] == user_id and row[1] == channel_id:
            log.append({'role': row[2], 'content': row[3]})
    return log

   

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
prefix = "/"

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()



@tree.command(name="talk",description="chatGPT-と話すコマンドです。")
@discord.app_commands.describe(text="送りたい文章を書き込んでください。")
async def talk(interaction: discord.Interaction,text: str):
    #こっからを非同期処理にする

    user_id = interaction.user.id
    channel_id = interaction.channel_id
    time = interaction.created_at

    talk_logs = talk_log(str(user_id), str(channel_id))
    prompt_messages = SYSTEM_PROMPTS + talk_logs + [{'role': 'user', 'content': text}]
    #シートに書き込む
    # ユーザーからのメッセージを保存
    sheet.append_row([str(user_id), str(channel_id), "user", text, str(time)])
    await interaction.response.defer()
    
    #返信の内容を取得＆AIの返答を取得してシートに書き込む
    #こっからhttpx使って直接APIを叩く
    #エンドポイント設定
    endpoint = "https://api.openai.com/v1/chat/completions"
    #ヘッダー設定
    headers = {
        "Content-Type": "application/json",
        #本番環境のみ使用。キーをハードコーディングしてはいけない(自戒)
        #"Authorization":f'Bearer {os.getenv("OPENAI_API_KEY")}'
        #テスト環境のみこれ使おう
        "Authorization":f'Bearer {"sk-xxxxxxxxxx"}'
    }


    #送信するデータを設定
    payload = {
        "model": model_engine,
        "messages": prompt_messages,
        "temperature": 0.8,
        "max_tokens": 1000,
    }

    #送信とか例外処理とか
    try:
        async with httpx.AsyncClient() as client:
            #タイムアウトを設定しないと大変なことになります
            response = await client.post(endpoint, headers=headers, json=payload, timeout=90)
            response.raise_for_status()
    except httpx.HTTPError as e:
        await interaction.followup.send(content=f"エラーが発生しました。時間をおいて試してみてね{e}")
        return
    #リクエストのステータスが200番台以外なら全部これで処理する
    if response.status_code != 200:
        await interaction.followup.send(content=f"エラーが発生しました。時間をおいて試してみてね！{response.text}")
        return
    #返信の内容を表示
    completion = response.json()["choices"]
    embed = discord.Embed()
    embed.title = f"text"
    embed.description = completion[0]["message"]["content"]
    embed.set_footer(text="AIの返答")
    embed.set_author(name="AIちゃんだよ!")
    await interaction.followup.send(embed=embed)
    #シートに書き込む
    # AIの返答を保存
    sheet.append_row([str(user_id), str(channel_id), "assistant", completion[0]["message"]["content"]])



client.run(TOKEN)
