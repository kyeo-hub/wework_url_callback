#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :企业微信API接收消息服务回调
@说明        :企业微信API接收消息服务回调，用于企业微信应用添加可信IP
@时间        :2024/01/31 10:40:15
@源码自      :https://zhuanlan.zhihu.com/p/466731552
@修改        :集家嘴的壳玛🐸
'''


from flask import Flask
from flask.globals import request
from Crypto.Cipher import AES
import base64,hashlib,os

app = Flask(__name__)

# 检查base64编码后数据位数是否正确
def check_base64_len(base64_str):
    len_remainder = 4 - (len(base64_str) % 4)
    if len_remainder == 0:
        return base64_str
    else:
        for temp in range(0,len_remainder):
            base64_str = base64_str + "="
        return base64_str
# 解密并提取消息正文
def msg_base64_decrypt(ciphertext_base64,key_base64):
    # 处理密文、密钥和iv
    ciphertext_bytes = base64.b64decode(check_base64_len(ciphertext_base64))
    key_bytes = base64.b64decode(check_base64_len(key_base64))
    iv_bytes = key_bytes[:16]

    # 解密
    decr = AES.new(key_bytes,AES.MODE_CBC,iv_bytes)
    plaintext_bytes = decr.decrypt(ciphertext_bytes)

    # 截取数据，判断消息正文字节数
    msg_len_bytes = plaintext_bytes[16:20]
    msg_len = int.from_bytes(msg_len_bytes,byteorder='big', signed=False)

    # 根据消息正文字节数截取消息正文，并转为字符串格式
    msg_bytes = plaintext_bytes[20:20+msg_len]
    msg = str(msg_bytes,encoding='utf-8')

    return msg

# 消息体签名校验
def check_msg_signature(msg_signature,token,timestamp,nonce,echostr):
    # 使用sort()从小到大排序[].sort()是在原地址改值的，所以如果使用li_s = li.sort()，li_s是空的，li的值变为排序后的值]
    li = [token,timestamp,nonce,echostr]
    li.sort()
    # 将排序结果拼接
    li_str = li[0]+li[1]+li[2]+li[3]

    # 计算SHA-1值
    sha1 = hashlib.sha1()
    # update()要指定加密字符串字符代码，不然要报错：
    # "Unicode-objects must be encoded before hashing"
    sha1.update(li_str.encode("utf8"))
    sha1_result = sha1.hexdigest()

    # 比较并返回比较结果
    if sha1_result == msg_signature:
        return True
    else:
        return False

@app.route("/",methods=["get"])
def wx_check_api():
    EncodingAESKey = os.getenv('QYWX_AESKEY')
    token = os.getenv('QYWX_TOKEN')
    # print(EncodingAESKey,token)
    if not request.args:
        return "错误：没有参数"
    else:
        msg_signature = request.args.to_dict().get("msg_signature")
        timestamp = request.args.to_dict().get("timestamp")
        nonce = request.args.to_dict().get("nonce")
        echostr = request.args.to_dict().get("echostr")
        print(msg_signature,timestamp,nonce,echostr)
        # 获取消息体签名校验结果        
        check_result = check_msg_signature(msg_signature,token,timestamp,nonce,echostr)
        if check_result:
            decrypt_result = msg_base64_decrypt(echostr,EncodingAESKey)
            print("通过")
            return decrypt_result
        else:
            return ""

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=5000)