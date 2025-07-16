import random
import math
import sys


def generate_random_odd(bits):
    """生成指定位数的随机奇数"""
    min_val = 2 ** (bits - 1)
    max_val = 2 ** bits - 1
    n = random.randint(min_val, max_val)
    return n | 1  # 确保返回奇数


def miller_rabin_test(n, k=5):
    """Miller-Rabin素性测试"""
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


def generate_probable_prime(bits, k=5):
    """生成指定位数的可能素数"""
    while True:
        candidate = generate_random_odd(bits)
        if miller_rabin_test(candidate, k):
            return candidate


def gcd(a, b):
    """欧几里得算法求最大公约数"""
    while b != 0:
        a, b = b, a % b
    return a


def are_coprime(a, b):
    """判断两个数是否互质"""
    return gcd(a, b) == 1


def extended_gcd(a, b):
    """扩展欧几里得算法"""
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


def generate_rsa_parameters(bits=16):
    """生成RSA参数"""
    print(f"\n生成 {bits} 位 RSA 参数...")

    # 生成两个不同的素数
    print("1. 生成素数p...")
    p = generate_probable_prime(bits)
    print(f"   p = {p} (是否为素数: {miller_rabin_test(p)})")

    print("2. 生成素数q...")
    q = generate_probable_prime(bits)
    while q == p:
        q = generate_probable_prime(bits)
    print(f"   q = {q} (是否为素数: {miller_rabin_test(q)})")

    # 计算n和φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)
    print(f"3. 计算模数n和欧拉函数φ(n):")
    print(f"   n = p * q = {p} * {q} = {n}")
    print(f"   φ(n) = (p-1)*(q-1) = {p - 1} * {q - 1} = {phi}")

    # 选择公钥e
    print("4. 选择公钥e (与φ(n)互质)...")
    e_candidates = [3, 5, 17, 257, 65537]  # 常用的小素数
    e = None
    for candidate in e_candidates:
        if candidate < phi and are_coprime(candidate, phi):
            e = candidate
            break
    if e is None:
        e = random.randint(2, phi - 1)
        while not are_coprime(e, phi):
            e = random.randint(2, phi - 1)
    print(f"   选择 e = {e} (与φ(n)是否互质: {are_coprime(e, phi)})")

    # 计算私钥d
    print("5. 计算私钥d (e的模逆元)...")
    d = modinv(e, phi)
    print(f"   d ≡ e⁻¹ mod φ(n) => {e}⁻¹ mod {phi} = {d}")

    # 验证
    print("6. 验证参数:")
    print(f"   e*d mod φ(n) = {e}*{d} mod {phi} = {(e * d) % phi} (应为1)")

    return (e, n), (d, n), (p, q)


def rsa_encrypt(message, public_key):
    """RSA加密"""
    e, n = public_key
    if message >= n:
        raise ValueError("消息必须小于n")
    return pow(message, e, n)


def rsa_decrypt(ciphertext, private_key):
    """RSA解密"""
    d, n = private_key
    return pow(ciphertext, d, n)


if __name__ == "__main__":
    print("=" * 50)
    print("小参数RSA算法参数建立程序套件")
    print("=" * 50)

    # 设置素数位数
    bits = 16  # 可以调整为8-32之间的值，更大的值计算会变慢

    # 生成RSA参数
    public_key, private_key, primes = generate_rsa_parameters(bits)

    print("\n生成的RSA参数:")
    print(f"公钥 (e, n): {public_key}")
    print(f"私钥 (d, n): {private_key}")
    print(f"素数 (p, q): {primes}")

    # 测试加密解密
    print("\n测试加密解密:")
    message = random.randint(2, public_key[1] - 1)
    print(f"原始消息: {message}")

    ciphertext = rsa_encrypt(message, public_key)
    print(f"加密结果: {ciphertext}")

    decrypted = rsa_decrypt(ciphertext, private_key)
    print(f"解密结果: {decrypted}")

    # 验证
    assert message == decrypted, "解密失败!"
    print("验证成功! 解密结果与原始消息一致。")
