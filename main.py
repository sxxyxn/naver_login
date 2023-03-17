from flask import Flask, redirect, request, render_template, url_for
import requests
import urllib.parse

app = Flask(__name__)

client_id = 'R7W0PJBzq9oU3P6U5X0H'
client_secret = 'WXJ473DMdl'
redirect_uri = 'https://signup-sxxyxn.koyeb.app/callback'
authorize_url = 'https://nid.naver.com/oauth2.0/authorize'
token_url = 'https://nid.naver.com/oauth2.0/token'
user_info_url = 'https://openapi.naver.com/v1/nid/me'

@app.route('/')
def index():
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': 'STATE_STRING'
    }
    login_url = f'{authorize_url}?{urllib.parse.urlencode(params)}'
    return render_template('index.html', login_url=login_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'state': state,
        'code': code,
        'redirect_uri': redirect_uri
    }
    token_response = requests.post(token_url, data=payload)
    access_token = token_response.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
    birthyear = int(user_info['response']['birthyear'])
    gender = user_info['response']['gender']
    if birthyear < 1974:
        flash('1974년 이전 출생자는 가입할 수 없습니다.')
        return redirect(url_for('index'))
    if gender == 'M':
        flash('남성은 가입할 수 없습니다.')
        return redirect(url_for('index'))
    elif gender == 'F':
        return redirect('https://forms.gle/nc2Ctv3EyFKraUj38') #구글폼주소

if __name__ == '__main__':
    app.run(debug=True)
