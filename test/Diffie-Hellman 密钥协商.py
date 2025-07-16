import random
import sympy

def generate_prime(bits=100):
    """生成一个指定位数的随机素数(sympy.randprime 生成一个位于指定范围内的随机素数)"""
    return sympy.randprime(2**(bits-1), 2**bits)

def find_primitive_root(p):
    """查找原根,sympy.primitive_root(p) 返回一个指定素数的原根"""
    if p == 2:
        return 1
    return sympy.primitive_root(p)

def diffie_hellman_example(bits=100):
    # 1. 协商公共参数（p 和 α）
    p = generate_prime(bits)
    alpha = find_primitive_root(p)
    print(f"公共参数: p = {p}\n原根 α = {alpha}")

    # 2. Alice 和 Bob 选择私钥（范围：2 ≤ 私钥 ≤ p-2）
    a_private = random.randint(2, p-2)
    b_private = random.randint(2, p-2)
    print(f"\nAlice 的私钥: a = {a_private}")
    print(f"Bob 的私钥: b = {b_private}")

    # 3. 计算公钥并交换
    A_public = pow(alpha, a_private, p)  # A = α^a mod p
    B_public = pow(alpha, b_private, p)  # B = α^b mod p
    print(f"\nAlice 发送给 Bob 的公钥: A = {A_public}")
    print(f"Bob 发送给 Alice 的公钥: B = {B_public}")

    # 4. 计算共享密钥
    K_alice = pow(B_public, a_private, p)  # K = B^a mod p
    K_bob = pow(A_public, b_private, p)    # K = A^b mod p
    print(f"\nAlice 计算的共享密钥: K = {K_alice}")
    print(f"Bob 计算的共享密钥: K = {K_bob}")

    # 5. 验证一致性(assert用于测试一个条件是否为真)
    assert K_alice == K_bob, "错误：共享密钥不匹配！"
    print("\n密钥协商成功！共享密钥一致。")

if __name__ == "__main__":
    diffie_hellman_example(bits=100)