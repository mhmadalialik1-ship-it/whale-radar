import requests,time,json,os
BOT_TOKEN=os.environ.get('BOT_TOKEN')
ADMIN_ID=int(os.environ.get('ADMIN_ID',0))
DATA_FILE="whale_data.json"

def load_data():
 try:return json.load(open(DATA_FILE))
 except:return {"wallets":{},"last":{}}

def save_data(d):json.dump(d,open(DATA_FILE,"w"))
DATA=load_data()
STATE={}

def send(c,t,m=None):
 d={"chat_id":c,"text":t,"parse_mode":"HTML"}
 if m:d["reply_markup"]=json.dumps(m)
 try:requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",data=d,timeout=10)
 except:pass

def menu():
 return{"inline_keyboard":[
 [{"text":"🎒 اضف TON","callback_data":"add_TON"},{"text":"🎒 اضف ETH","callback_data":"add_ETH"}],
 [{"text":"📋 محافظي","callback_data":"list"}]
 ]}

send(ADMIN_ID,"✅ <b>شغال من المجلد الرئيسي</b>",menu())
print("شغال...")
