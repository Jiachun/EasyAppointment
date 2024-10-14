# -*- coding: utf-8 -*-
"""
# 文件名称: utils/crypto_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-27
# 版本: 1.0
# 描述: 实现了数据的加密解密功能。
"""
import base64
import os

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes

from app.config import Config


def generate_rsa_key_pair():
    """生成 RSA 密钥对"""
    # 检查目录是否存在，不存在则创建
    keys_directory = Config.KEYS_DIR
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
    """从文件加载 RSA 公钥"""
    public_key_path = Config.PUBLIC_KEY_PATH
    try:
        with open(public_key_path, 'rb') as f:
            return RSA.import_key(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到公钥文件: {public_key_path}")
    except ValueError:
        raise ValueError(f"公钥文件内容无效: {public_key_path}")


def load_private_key_from_file():
    """从文件加载 RSA 私钥"""
    private_key_path = Config.PRIVATE_KEY_PATH
    try:
        with open(private_key_path, 'rb') as f:
            return RSA.import_key(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到私钥文件: {private_key_path}")
    except ValueError:
        raise ValueError(f"私钥文件内容无效: {private_key_path}")


def load_public_key_from_env():
    """从环境变量加载 RSA 公钥"""
    public_key_data = Config.PUBLIC_KEY
    if public_key_data:
        return RSA.import_key(public_key_data)
    else:
        raise EnvironmentError(f"环境变量 PUBLIC_KEY 中未找到公钥数据")


def load_private_key_from_env():
    """从环境变量加载 RSA 私钥"""
    private_key_data = Config.PRIVATE_KEY
    if private_key_data:
        return RSA.import_key(private_key_data)
    else:
        raise EnvironmentError(f"环境变量 PRIVATE_KEY 中未找到私钥数据")


def rsa_encrypt_bytes_to_str(public_key: RsaKey, data: bytes) -> str:
    """使用 RSA 公钥加密数据 bytes to str"""
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data)  # 加密后的字节数据
    return base64.b64encode(encrypted_data).decode('utf-8')  # 编码为 base64 字符串


def rsa_decrypt_str_to_bytes(private_key: RsaKey, encrypted_data: str) -> bytes:
    """ 使用 RSA 私钥解密数据 str to bytes"""
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_data_bytes = base64.b64decode(encrypted_data.encode('utf-8'))  # base64 解码为字节数据
    decrypted_data = cipher.decrypt(encrypted_data_bytes)  # 解密为字节数据
    return decrypted_data


def rsa_encrypt_str_to_bytes(public_key: RsaKey, data: str) -> bytes:
    """使用 RSA 公钥加密数据 str to bytes"""
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))  # 加密后的字节数据
    return encrypted_data


def rsa_decrypt_bytes_to_str(private_key: RsaKey, encrypted_data: bytes) -> str:
    """ 使用 RSA 私钥解密数据 bytes to str"""
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher.decrypt(encrypted_data)  # 解密为字节数据
    return decrypted_data.decode('utf-8')  # 解码为字符串


def rsa_encrypt_str_to_str(public_key: RsaKey, data: str) -> str:
    """使用 RSA 公钥加密数据 str to str"""
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))  # 加密后的字节数据
    return base64.b64encode(encrypted_data).decode('utf-8')  # 编码为 base64 字符串


def rsa_decrypt_str_to_str(private_key: RsaKey, encrypted_data: str) -> str:
    """ 使用 RSA 私钥解密数据 str to str"""
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_data_bytes = base64.b64decode(encrypted_data.encode('utf-8'))  # base64 解码为字节数据
    decrypted_data = cipher.decrypt(encrypted_data_bytes)  # 解密为字节数据
    return decrypted_data.decode('utf-8')  # 解码为字符串


def rsa_encrypt_aes_key(aes_key):
    """加载 RSA 公钥对 AES 密钥进行加密"""
    if Config.PUBLIC_KEY:
        return rsa_encrypt_bytes_to_str(load_public_key_from_env(), aes_key)
    return rsa_encrypt_bytes_to_str(load_public_key_from_file(), aes_key)


def rsa_decrypt_aes_key(aes_key):
    """加载 RSA 私钥对 AES 密钥进行解密"""
    if Config.PRIVATE_KEY:
        return rsa_decrypt_str_to_bytes(load_private_key_from_env(), aes_key)
    return rsa_decrypt_str_to_bytes(load_private_key_from_file(), aes_key)


def pad(data: bytes) -> bytes:
    """使用 PKCS7 填充数据"""
    block_size = AES.block_size
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length]) * padding_length
    return data + padding


def unpad(data: bytes) -> bytes:
    """去掉 PKCS7 填充"""
    padding_length = data[-1]
    return data[:-padding_length]


def aes256_encrypt(data: str, key: bytes) -> str:
    """使用 AES-256 加密数据"""
    # 生成随机的初始化向量 (IV)
    cipher = AES.new(key, AES.MODE_CBC)

    # 填充数据
    padded_data = pad(data.encode('utf-8'))
    ciphertext = cipher.encrypt(padded_data)

    # 返回 IV 和密文的组合，进行 Base64 编码
    return base64.b64encode(cipher.iv + ciphertext).decode('utf-8')


def aes256_decrypt(encrypted_data: str, key: bytes) -> str:
    """使用 AES-256 解密数据"""
    # 解码 Base64 编码的数据
    encrypted_data = base64.b64decode(encrypted_data)

    # 提取 IV 和密文
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密并去掉填充
    decrypted_data = unpad(cipher.decrypt(ciphertext))
    return decrypted_data.decode('utf-8')


def aes256_encrypt_data(data):
    """随机生成 AES-256 密钥对数据进行加密"""
    try:
        key = get_random_bytes(32)  # 生成 AES 密钥
        encrypted_data = aes256_encrypt(data, key)  # 加密数据

        return {
            'encrypted_key': rsa_encrypt_aes_key(key),  # 使用 RSA 加密 AES 密钥
            'encrypted_data': encrypted_data,  # 加密后的数据
        }
    except Exception as e:
        return {'error': str(e)}, 400  # 错误处理


def aes256_decrypt_data(data):
    """使用 AES-256 密钥对数据进行解密"""
    try:
        # 解码密钥和加密数据
        key = rsa_decrypt_aes_key(data['encrypted_key'])  # 使用 RSA 解密 AES 密钥
        encrypted_data = data['encrypted_data']  # 加密后的数据
        decrypted_data = aes256_decrypt(encrypted_data, key)  # 解密数据

        return decrypted_data
    except Exception as e:
        return {'error': str(e)}, 400  # 错误处理


def aes256_encrypt_sensitive(data):
    """使用 AES-256 密钥对敏感数据进行加密"""
    key = base64.b64decode(Config.AES_KEY.encode('utf-8'))  # 加载密钥
    encrypted_data = aes256_encrypt(data, key)  # 加密数据
    return encrypted_data


def aes256_decrypt_sensitive(encrypted_data):
    """使用 AES-256 密钥对敏感数据进行解密"""
    key = base64.b64decode(Config.AES_KEY.encode('utf-8'))  # 加载密钥
    decrypted_data = aes256_decrypt(encrypted_data, key)  # 解密数据
    return decrypted_data
