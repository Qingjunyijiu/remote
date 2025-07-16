import random
import math
from typing import Tuple


class ElGamalParameterGenerator:
    """ElGamal算法参数生成套件"""

    @staticmethod
    def generate_random_odd(bits: int) -> int:
        """生成指定位数的随机奇数"""
        min_val = 2 ** (bits - 1)
        max_val = 2 ** bits - 1
        n = random.randint(min_val, max_val)
        return n | 1  # 确保返回奇数

    @staticmethod
    def miller_rabin_test(n: int, k: int = 5) -> bool:
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

    @staticmethod
    def generate_prime(bits: int = 16, k: int = 5) -> int:
        """生成指定位数的素数"""
        while True:
            candidate = ElGamalParameterGenerator.generate_random_odd(bits)
            if ElGamalParameterGenerator.miller_rabin_test(candidate, k):
                return candidate

    @staticmethod
    def factorize(n: int) -> list:
        """试除法质因数分解（简化版）"""
        factors = []
        while n % 2 == 0:
            factors.append(2)
            n //= 2
        i = 3
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 2
        if n > 1:
            factors.append(n)
        return factors

    @staticmethod
    def is_primitive_root(g: int, p: int) -> bool:
        """判断g是否是模p的原根"""
        if math.gcd(g, p) != 1:
            return False

        phi = p - 1
        factors = set(ElGamalParameterGenerator.factorize(phi))

        for q in factors:
            if pow(g, phi // q, p) == 1:
                return False
        return True

    @staticmethod
    def find_primitive_root(p: int) -> int:
        """寻找模p的最小原根"""
        if p == 2:
            return 1

        for g in range(2, p):
            if ElGamalParameterGenerator.is_primitive_root(g, p):
                return g
        raise ValueError(f"未找到{p}的原根")

    @staticmethod
    def generate_elgamal_parameters(bits: int = 16) -> Tuple[int, int]:
        """生成ElGamal参数(p, α)"""
        print(f"\n生成 {bits} 位 ElGamal 参数...")

        # 1. 生成安全素数p（使得(p-1)/2也是素数）
        print("1. 生成安全素数p...")
        while True:
            p = ElGamalParameterGenerator.generate_prime(bits)
            q = (p - 1) // 2
            if ElGamalParameterGenerator.miller_rabin_test(q):
                break
        print(f"   p = {p} (是否为素数: {ElGamalParameterGenerator.miller_rabin_test(p)})")
        print(f"   (p-1)/2 = {q} (是否为素数: {ElGamalParameterGenerator.miller_rabin_test(q)})")

        # 2. 寻找p的原根α
        print("2. 寻找p的原根α...")
        alpha = ElGamalParameterGenerator.find_primitive_root(p)
        print(f"   α = {alpha} (是否为原根: {ElGamalParameterGenerator.is_primitive_root(alpha, p)})")
        print(f"   验证: α^(p-1) mod p = {pow(alpha, p - 1, p)} (应为1)")

        return p, alpha

    @staticmethod
    def generate_key_pair(p: int, alpha: int) -> Tuple[Tuple[int, int, int], int]:
        """生成ElGamal密钥对"""
        print("\n生成密钥对...")

        # 私钥：随机整数a，1 < a < p-1
        a = random.randint(2, p - 2)
        print(f"1. 生成私钥a: {a} (1 < a < {p - 1})")

        # 公钥：β = α^a mod p
        beta = pow(alpha, a, p)
        print(f"2. 计算公钥β = α^a mod p = {alpha}^{a} mod {p} = {beta}")

        return (p, alpha, beta), a


class ElGamalCryptoSystem:
    """ElGamal加密系统实现"""

    @staticmethod
    def encrypt(public_key: Tuple[int, int, int], message: int) -> Tuple[int, int]:
        """ElGamal加密"""
        p, alpha, beta = public_key
        if message >= p:
            raise ValueError(f"消息必须小于p ({message} >= {p})")

        print(f"\n加密消息: {message}")

        # 选择随机整数k，1 < k < p-1
        k = random.randint(2, p - 2)
        print(f"1. 选择临时密钥k: {k} (1 < k < {p - 1})")

        # 计算γ = α^k mod p
        gamma = pow(alpha, k, p)
        print(f"2. 计算γ = α^k mod p = {alpha}^{k} mod {p} = {gamma}")

        # 计算δ = (消息 * β^k) mod p
        beta_k = pow(beta, k, p)
        delta = (message * beta_k) % p
        print(f"3. 计算δ = (m * β^k) mod p = ({message} * {beta}^{k}) mod {p} = {delta}")

        print(f"加密结果: (γ, δ) = ({gamma}, {delta})")
        return gamma, delta

    @staticmethod
    def decrypt(private_key: int, public_key: Tuple[int, int, int], ciphertext: Tuple[int, int]) -> int:
        """ElGamal解密"""
        p, alpha, beta = public_key
        a = private_key
        gamma, delta = ciphertext

        print(f"\n解密密文: (γ, δ) = ({gamma}, {delta})")

        # 计算共享密钥γ^a mod p
        shared_secret = pow(gamma, a, p)
        print(f"1. 计算共享密钥γ^a mod p = {gamma}^{a} mod {p} = {shared_secret}")

        # 计算共享密钥的模逆（使用费马小定理，p是素数）
        shared_secret_inv = pow(shared_secret, p - 2, p)
        print(f"2. 计算共享密钥的逆: {shared_secret}^-1 mod {p} = {shared_secret_inv}")

        # 解密消息 = (δ * 共享密钥逆) mod p
        message = (delta * shared_secret_inv) % p
        print(f"3. 解密消息 = (δ * s^-1) mod p = ({delta} * {shared_secret_inv}) mod {p} = {message}")

        return message


if __name__ == "__main__":

    # 参数设置
    bits = 16  # 素数位数（建议8-16位，更大的值计算会变慢）
    message = 1234  # 要加密的消息

    try:
        # 1. 生成ElGamal参数
        p, alpha = ElGamalParameterGenerator.generate_elgamal_parameters(bits)

        # 2. 生成密钥对
        public_key, private_key = ElGamalParameterGenerator.generate_key_pair(p, alpha)
        print(f"\n公钥 (p, α, β): {public_key}")
        print(f"私钥 a: {private_key}")

        # 3. 加密消息
        ciphertext = ElGamalCryptoSystem.encrypt(public_key, message)

        # 4. 解密密文
        decrypted = ElGamalCryptoSystem.decrypt(private_key, public_key, ciphertext)

        # 验证
        print(f"\n原始消息: {message}")
        print(f"解密结果: {decrypted}")
        assert message == decrypted, "解密失败!"
        print("验证成功! 解密结果与原始消息一致。")

    except ValueError as e:
        print(f"错误: {e}")

    print("\n注意: 此实现使用小参数仅用于教学目的。")
    print("实际ElGamal应用应使用至少1024位的素数以保证安全性。")