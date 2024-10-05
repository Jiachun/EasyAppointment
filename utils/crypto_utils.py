# -*- coding: utf-8 -*-
"""
# 文件名称: utils/crypto_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-27
# 版本: 1.0
# 描述: 实现了数据的非对称加密解密功能。
"""


import os
from dotenv import load_dotenv
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


load_dotenv()


def generate_key_pair(keys_directory):
    # 检查目录是否存在，不存在则创建
    if not os.path.exists(keys_directory):
        os.makedirs(keys_directory)
        print(f"创建目录: {keys_directory}")

        # 生成 RSA 密钥对
        key = RSA.generate(2048)

        # 保存私钥
        with open(os.path.join(keys_directory, 'private_key.pem'), 'wb') as f:
            f.write(key.export_key())
        print("私钥已生成并保存为 private_key.pem")

        # 保存公钥
        with open(os.path.join(keys_directory, 'public_key.pem'), 'wb') as f:
            f.write(key.publickey().export_key())
        print("公钥已生成并保存为 public_key.pem")
    else:
        print(f"目录 {keys_directory} 已存在")


def load_public_key_from_file():
    # 从文件加载公钥
    public_key_path = os.getenv('PUBLIC_KEY_PATH')
    try:
        with open(public_key_path, 'rb') as f:
            return RSA.import_key(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到公钥文件: {public_key_path}")
    except ValueError:
        raise ValueError(f"公钥文件内容无效: {public_key_path}")


def load_private_key_from_file():
    # 从文件加载私钥
    private_key_path = os.getenv('PRIVATE_KEY_PATH')
    try:
        with open(private_key_path, 'rb') as f:
            return RSA.import_key(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到私钥文件: {private_key_path}")
    except ValueError:
        raise ValueError(f"私钥文件内容无效: {private_key_path}")


def load_public_key_from_env():
    # 从环境变量加载公钥
    public_key_data = os.getenv('PUBLIC_KEY')
    if public_key_data:
        return RSA.import_key(public_key_data)
    else:
        raise EnvironmentError(f"环境变量 PUBLIC_KEY 中未找到公钥数据")


def load_private_key_from_env():
    # 从环境变量加载私钥
    private_key_data = os.getenv('PRIVATE_KEY')
    if private_key_data:
        return RSA.import_key(private_key_data)
    else:
        raise EnvironmentError(f"环境变量 PRIVATE_KEY 中未找到私钥数据")


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
    if os.getenv('PUBLIC_KEY'):
        return encrypt_message(load_public_key_from_env(), content.encode('utf-8'))
    else:
        return encrypt_message(load_public_key_from_file(), content.encode('utf-8'))


def decrypt_content(content):
    # 加载私钥对数据进行解密
    if os.getenv('PRIVATE_KEY'):
        return decrypt_message(load_private_key_from_env(), content).decode('utf-8')
    else:
        return decrypt_message(load_private_key_from_file(), content).decode('utf-8')

