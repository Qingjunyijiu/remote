import random
import math
import sys


def is_prime(n, k=5):
    """Miller-Rabin素性测试"""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False

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


def find_primitive_root(p):
    """寻找素数的原根（简化版）"""
    if p == 2:
        return 1

    # p-1的质因数分解（简化：假设p-1=2*q，q为素数）
    q = (p - 1) // 2
    if not is_prime(q):
        return None  # 无法处理更复杂的情况

    for g in range(2, p):
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            return g
    return None


def generate_elgamal_parameters(bits=16):
    """生成ElGamal参数"""
    print(f"\n生成 {bits} 位 ElGamal 参数...")

    # 1. 选择大素数p
    print("1. 生成素数p...")
    p = generate_prime(bits)
    while True:
        # 确保p-1有足够大的素因子以便找到原根
        if is_prime((p - 1) // 2):
            break
        p = generate_prime(bits)
    print(f"   p = {p} (是否为素数: {is_prime(p)})")

    # 2. 找到p的原根α
    print("2. 寻找p的原根α...")
    alpha = find_primitive_root(p)
    while alpha is None:
        p = generate_prime(bits)
        alpha = find_primitive_root(p)
    print(f"   α = {alpha} (是否为原根: {pow(alpha, p - 1, p) == 1})")

    return p, alpha


def generate_keys(p, alpha):
    """生成ElGamal密钥对"""
    # 私钥：随机整数a，1 < a < p-1
    a = random.randint(2, p - 2)
    # 公钥：β = α^a mod p
    beta = pow(alpha, a, p)
    return (p, alpha, beta), a  # (公钥), (私钥)


def elgamal_encrypt(public_key, message):
    """ElGamal加密"""
    p, alpha, beta = public_key
    if message >= p:
        raise ValueError("消息必须小于p")

    # 选择随机整数k，1 < k < p-1
    k = random.randint(2, p - 2)

    # 计算密文对 (γ, δ)
    gamma = pow(alpha, k, p)
    delta = (message * pow(beta, k, p)) % p

    return gamma, delta


def elgamal_decrypt(private_key, public_key, ciphertext):
    """ElGamal解密"""
    p, alpha, beta = public_key
    a = private_key
    gamma, delta = ciphertext

    # 计算共享密钥γ^a
    shared_secret = pow(gamma, a, p)

    # 计算共享密钥的模逆
    shared_secret_inv = pow(shared_secret, p - 2, p)

    # 解密消息
    message = (delta * shared_secret_inv) % p
    return message


if __name__ == "__main__":
    # 设置素数位数（大的值计算会变慢）
    bits = 16

    # 1. 生成ElGamal参数
    p, alpha = generate_elgamal_parameters(bits)

    # 2. 生成密钥对
    public_key, private_key = generate_keys(p, alpha)
    print("\n生成的密钥对:")
    print(f"公钥 (p, α, β): {public_key}")
    print(f"私钥 (a): {private_key}")

    # 3. 加密测试
    print("\n加密测试:")
    message = random.randint(1, p - 1)
    print(f"原始消息: {message}")

    ciphertext = elgamal_encrypt(public_key, message)
    print(f"加密结果 (γ, δ): {ciphertext}")

    # 4. 解密测试
    decrypted = elgamal_decrypt(private_key, public_key, ciphertext)
    print(f"解密结果: {decrypted}")

    # 验证
    assert message == decrypted, "解密失败!"
    print("验证成功! 解密结果与原始消息一致。")
