import requests as reqs
import threading, webbrowser, random, logging, base64
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
s_host = "localhost"
s_port = 6969
count = 0
state = "on"

content_out = []
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def ngl_spam(username, msg, a):
    global content_out, state
    a = int(a)
    a-=1
    url = "https://ngl.link:443/api/submit"
    f = open('uheaderz.txt','r').read().splitlines()
    r_ua = ''.join(random.choices(f))
    headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": r_ua, "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://ngl.link", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://ngl.link/"+str(username), "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
    data = {"username": username, "question": msg, "deviceId": "381691f9-f6a2-7333-b132-618c51e2a34b", "gameSlug": '', "referrer": ''}
    r = reqs.post(url, headers=headers, data=data)

    if(r.status_code == 200):
        content_out.append(f'<h6 class="responze suc">[SUCCESS] ({a+1})| User: {username}</h6>')
    else:
        content_out.append(f'<h6 class="responze fai">[FAILED] ({a+1})| User: {username}</h6>')
    if(a > 0):
        ngl_spam(username, msg, a)
    else:
        content_out = ["".join(content_out)]
        state = "off"


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/status')
def status():
    content = bytes(''.join(content_out),encoding="utf-8")
    content = base64.b64encode(content)
    return f"{state}:{content.decode()}"

@app.route('/spam',methods=["POST","GET"])
def spam():
    if(request.method == "POST"):
        global state, content_out
        state = "on"
        content_out = []
        user = request.form['user']
        amnt = request.form['amount']
        message = request.form['msg']
        threading.Thread(target=ngl_spam, args=[user, message, amnt]).start()
        # ngl_spam(user, message, amnt)
    return render_template("spam.html")


if(__name__ == "__main__"):
    webbrowser.open('http://localhost:6969')
    app.run(host=s_host, port=s_port)

