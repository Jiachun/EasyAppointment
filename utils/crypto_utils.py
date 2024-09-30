# -*- coding: utf-8 -*-
"""
# 文件名称: utils/crypto_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-27
# 版本: 1.0
# 描述: 实现了数据的非对称加密解密功能。
"""


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def generate_key(dir_path):
    # 生成 RSA 密钥对
    key = RSA.generate(2048)

    # 保存私钥
    with open(dir_path + 'private_key.pem', 'wb') as f:
        f.write(key.export_key())

    # 保存公钥
    with open(dir_path + 'public_key.pem', 'wb') as f:
        f.write(key.publickey().export_key())


def load_public_key(file_path):
    # 从文件加载公钥
    with open(file_path, 'rb') as f:
        return RSA.import_key(f.read())


def load_private_key(file_path):
    # 从文件加载私钥
    with open(file_path, 'rb') as f:
        return RSA.import_key(f.read())


def encrypt_message(public_key, message):
    # 使用公钥加密消息
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(message)


def decrypt_message(private_key, encrypted_message):
    # 使用私钥解密消息
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(encrypted_message)


def encrypt_content(content):
    # 加载公钥对数据进行加密
    pub_key = load_public_key('public_key.pem')
    return encrypt_message(pub_key, content.encode('utf-8'))


def decrypt_content(content):
    # 加载私钥对数据进行解密
    priv_key = load_private_key('private_key.pem')
    return decrypt_message(priv_key, content).decode('utf-8')

