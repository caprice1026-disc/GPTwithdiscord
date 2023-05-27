# ~~個人的なメモみたいな感じなのであまり参考にしない方がいい。~~
gspreadを使用して過去の文脈を参照しつつdiscordでchatGPTと会話できます。メモ書きが多いです。可読性が悪すぎて読みづらいです。そのうちコメントとかも書き換える予定。今の状態だと~~多分discordpyとopenAIAPIとspreadsheetAPIを理解している人でないと分かりません。~~

## だいじなこと
OpenAI APIへリクエストを送る文字数もトークン量にカウントされます。今の状態だと過去の文脈全部をAPIにリクエストを送っちゃうのでそのうちエラーを吐きます。スプレッドシートから参照する際に同じチャンネル、同じユーザーを参照するので参照の限界を設定してください。やる気があるときに修正する予定

## 使い方
・依存関係をインストールします

・discordAPIとopenAIAPIとspreadsheetAPIを用意します。分からない？これを参考にしてください。
　https://qiita.com/wataru86/items/12958c36d010733b00be

・SYSTEM PROMPTSを自分の必要としているように書き換えます。キャラクターなりきりとかもここで設定します。分からないならこれを参考:
https://zenn.dev/zuma_lab/articles/chatgpt-line-chatbot

・APIとか認証情報をつっこみます。参考:
https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project

## 全部わかる人へのtips
discordAPIのタイムアウトは死ぬほど短いです。こんにちはくらいの内容の返信くらいならなんとかなりますが非同期処理にしないと確実にタイムアウトしてエラーを起こします。asyncでsleepさせてようと思いましたがうまくいきませんでした。
なのでhttpxを使用して直接APIを叩いています。LINEチャットbotとはちょっと違うAPIの叩き方になっているので注意が必要です。

参考:https://zenn.dev/quojama/articles/730b9901769053

無課金構成です。replit＋uptimerobot＋スプレッドシートに展開しています。金があるならスプレッドシートなんか使わずlambdaとdynamoDB使いましょう。その方が選択肢が増えます。





