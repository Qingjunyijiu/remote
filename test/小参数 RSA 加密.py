import random
import math


def is_prime(n, k=5):
    """Miller-Rabin素数测试"""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False

    # 将n-1表示为d*2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits=16):
    """生成指定位数的素数"""
    while True:
        p = random.randint(2 ** (bits - 1), 2 ** bits)
        if is_prime(p):
            return p


def extended_gcd(a, b):
    """扩展欧几里得算法求模逆元"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    """计算模逆元"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None  # 不存在逆元
    else:
        return x % m


def generate_rsa_keys(bits=16):
    """生成RSA密钥对"""
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    # 选择e，通常为65537或较小的与phi互质的数
    e = 65537
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = modinv(e, phi)
    return (e, n), (d, n)


def rsa_encrypt(message, public_key):
    """RSA加密"""
    e, n = public_key
    # 平方乘法实现模幂运算
    return pow(message, e, n)


def rsa_decrypt(ciphertext, private_key):
    """RSA解密"""
    d, n = private_key
    # 平方乘法实现模幂运算
    return pow(ciphertext, d, n)



if __name__ == "__main__":
    # 生成RSA密钥对（16位素数，适合演示）
    public_key, private_key = generate_rsa_keys(16)
    print(f"公钥(e,n): {public_key}")
    print(f"私钥(d,n): {private_key}")

    # 加密示例
    message = 12345  # 要加密的消息（必须小于n）
    if message >= public_key[1]:
        raise ValueError("消息必须小于n")

    ciphertext = rsa_encrypt(message, public_key)
    print(f"加密后的密文: {ciphertext}")

    # 解密示例
    decrypted = rsa_decrypt(ciphertext, private_key)
    print(f"解密后的消息: {decrypted}")

    # 验证
    assert message == decrypted, "解密失败!"
    print("RSA加密解密验证成功!")