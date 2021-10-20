# VSDeeP 客户设备接口说明文档


为了方便客户管理和操作平台和设备，VSDeeP为客户提供了若干接口，以达到从平台获取信息和直接管理平台上的设备的功能。方便客户将VSDeeP的产品通过VSAIS平台的api接口对接到自有平台。

一般来讲，通过接口操作设备可以分为如下步骤：通过VSAIS平台登录鉴权；通过VSAIS平台获取设备信息；通过设备接口获取相关设备操作功能。

## 通用信息

### VSAIS平台 api 基础接口: base_url

https://api.vsais.com

## 鉴权

### 请求地址: 

${base_url}/api/oauth2/token

### 调用方式

POST / FORM

### FORM 参数

|字段名称 |字段说明 |类型 |必填 |备注 |
| -------------|:--------------|:--------------|:--------------|:------|
|grant_type|固定字段|string|Y|固定字符串: password|
|password|密码|string|Y|sha1(password) 后转换为十六进制字符串|
|username|用户名|string|Y|+86 手机号，注意+86后面有一个空格|
|scope|固定字段|string|Y|固定字符串: USER

### 返回值
```json
{
    "data": {
        "access_token": "***************************",
        "expires_in": 3600,
        "refresh_token": "***************************",
        "scope": "USER",
        "token_type": "bearer"
    },
    "err_code": null,
    "execution_time": 0.017519474029541016,
    "is_successful": true,
    "msg": "Operation_successful",
    "status_code": 200
}
```
#### 返回值说明： .data
|字段名称 |字段说明 |类型|备注 |
| -------------|:--------------|:--------------|:--------------|
|access_token|用于访问的Token|string|后续需要使用|
|expires_in|过期期限|int|单位: 秒|
|refresh_token|用于刷新的Token|string|一般不使用|
|scope|登录范围|string|一般不使用|
|token_type|Token种类|string|Y|

## 获取设备信息

### 请求地址: 

${base_url}/api/client/device

### 调用方式

GET

### Headers
Authorization:Bearer ${access_token}
注意 Bearer 后面有一个空格，${access_token}为鉴权获得的未过期的Token

### URL 参数

|字段名称 |字段说明 |类型 |必填 |备注 |
| -------------|:--------------|:--------------|:--------------|:------|
|search|设备VSN|string|Y|可以搜索设备VSN或者设备名称|

### 返回值
```json
{
    "data": {
        "items": [
            {
                "access_token": {
                    "rw": "*********************"
                },
                "creation_time": 1631936272,
                "enabled": true,
                "locked": false,
                "meta": {
                    "address": "*********************",
                    "addressOld": "*********************",
                    "company": "*********************",
                    "constructionCompany": "*********************",
                    "constructionName": "*********************",
                    "coordinate": "120.742058,31.260366",
                    "deviceName": "*********************",
                    "userName": "*********************",
                    "userPhone": "13333333333"
                },
                "meta_alt": null,
                "model": "VSDeeP WS",
                "serial_number": "X6132AF6DCE********",
                "status": {
                    "access_url": {
                        "WEB": "/device/****"
                    },
                    "online": true
                },
                "uuid": "*****-*****-****-****-********"
            }
        ],
        "page_index": 1,
        "page_size": 100,
        "total_item": 1
    },
    "err_code": null,
    "execution_time": 0.91302490234375,
    "is_successful": true,
    "msg": "Operation_successful",
    "status_code": 200
}
```
#### 重要返回值说明： 

.data.items: array

|字段名称 |字段说明 |类型|备注 |
| -------------|:--------------|:--------------|:--------------|
|serial_number|设备VSN编码|string|-|
|access_token.rw|访问设备的TOKEN|string|后续需要使用|
|status.access_url.WEB|访问设备的API接口地址|string|后续需要使用|
|status.online|设备的在线状态|boolean|-|

## 获取设备接口基础地址

将VSAIS平台基础地址与上述接口获得的 ${status.access_url.WEB} 中的地址进行拼接，即可获得设备接口的基础地址。

### 设备接口地址: device_base_url

${base_url}${status.access_url.WEB}

由于${status.access_url.WEB} 带有"/"，所不需要另加。其一般形式为：

https://api.vsais.com/device/****

(****一般为7开头的四位数字)

## 获取设备相机信息

### 请求地址: 

${device_base_url}/status/camera

### 调用方式

GET

### Headers
TOKEN:${access_token.rw}

### 返回值

```json
{
    "is_successful":true,
    "data":{
        "相机测试":{
            "type":"camera",
            "available":true,
            "color":false,
            "width":1920,
            "height":1080,
            "process_time":0.09310030937194824,
            "ping_rtt":0.683,
            "ping_large_rtt":12.665,
            "detail":165,
            "camera_brand":"HIKVISION",
            "camera_sn":"DS-IPC-B12HV2-IA20210701AACHG29443469",
            "camera_model":"DS-IPC-B12HV2-IA",
            "time":1634655797
        }
    },
    "type":"camera"
}
```

#### 结果说明 .data

键值名称为相机别名，其中包含的相机参数有：

|字段名称 |字段说明 |类型|备注 |
| -------------|:--------------|:--------------|:--------------|
|type|相机类型|string|camera(单相机) 或 group(相机序列)|
|available|相机可用性|boolean|相机是否可以获取正常图片|
|color|是否为彩色图片|boolean|-|
|width|宽|int|-|
|height|高|int|-|
|process_time|获取图片耗时|float|-|
|ping_rtt|ping相机IP地址（1450bytes）的返回时间|float|以小包ping相机，检查一遍连通性|
|ping_large_rtt|ping相机IP地址（1450bytes）的返回时间|float|以大包ping相机，检查大流量连通性|
|detail|图像细节|int|越大内容越丰富，如果过小（小于2），则画面可能起雾或者看向不正确的方向|
|camera_brand|相机品牌|string|通过Onvif获取的相机品牌|
|camera_sn|相机序列号|string|通过Onvif获取的相机序列号，可后期任意修改|
|camera_model|相机型号|string|通过Onvif获取的相机型号|
|time|彼时的时间戳|string|处理该相机时的Unix时间戳，精确到秒|


## 修订记录

* 2021-10-19 Feimax 初次修订