import sys
import requests
from hashlib import sha1
import json
# 设置设备的VSN

base_url = 'https://api.vsais.com'

header_form = {'Content-Type': 'application/x-www-form-urlencoded'}


def header_json(token):
    return {'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'}


def header_device_json(token):
    return {'TOKEN': token,
            'Content-Type': 'application/json'}


# 鉴权
username = input('请输入手机号，不需要带+86：')
psw = input('请输入密码：')
# device_vsn = 'X6132AF6DCE6A53172B'
device_vsn = input('请输入设备VSN：')

data_body = {'grant_type': 'password',
             'password': sha1(psw.encode()).hexdigest(),
             'username': f'+86 {username}',
             'scope': 'USER'}

rval = requests.post(base_url + '/api/oauth2/token', data=data_body, headers=header_form).json()

access_token = rval['data']['access_token']  # 获取到 token


# 获取对设备的访问接口和权限
rval = requests.get(base_url + f'/api/client/device?search={device_vsn}', headers=header_json(access_token)).json()

if not rval['is_successful']:
    sys.exit(0)

if len(rval['data']['items']) != 1:
    sys.exit(0)

online_status = rval['data']['items'][0]['status']['online']

if online_status is False:
    sys.exit(0)

device_api = rval['data']['items'][0]['status']['access_url']['WEB']
device_token = rval['data']['items'][0]['access_token']['rw']

rval = requests.get(base_url + device_api + f'/status/camera', headers=header_device_json(device_token)).json()
print(json.dumps(rval, indent=4, ensure_ascii=False))
