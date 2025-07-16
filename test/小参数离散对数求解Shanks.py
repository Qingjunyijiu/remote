import math
from typing import Optional


def shanks_algorithm(g: int, h: int, p: int) -> Optional[int]:
    """
    Shanks' Baby-step Giant-step算法求解离散对数 g^x ≡ h mod p
    返回满足条件的最小非负整数x，若不存在则返回None
    """
    if g == 1:
        return 0 if h == 1 else None

    # 计算步长m = ⌈√p⌉
    m = math.isqrt(p) + 1

    print(f"\n求解 {g}^x ≡ {h} mod {p}")
    print(f"步长 m = ⌈√{p}⌉ = {m}")

    # Baby-step阶段：预计算g^j mod p (0 ≤ j < m)
    baby_steps = {}
    print("\nBaby-step阶段：计算g^j mod p (0 ≤ j < m)")
    current = 1
    for j in range(m):
        baby_steps[current] = j
        print(f"  j={j}: {g}^{j} mod {p} = {current}")
        current = (current * g) % p

    # 计算g^(-m) mod p
    gm_inv = pow(g, p - 1 - m, p)
    print(f"\n计算g^(-m) mod p = {g}^(-{m}) mod {p} = {gm_inv}")

    # Giant-step阶段：查找h*(g^(-m))^i mod p
    print("\nGiant-step阶段：查找h*(g^-m)^i mod p")
    current = h
    for i in range(m):
        print(f"  i={i}: 检查 {h}*({gm_inv})^{i} mod {p} = {current}")
        if current in baby_steps:
            j = baby_steps[current]
            x = i * m + j
            print(f"\n找到匹配：i={i}, j={j}")
            print(f"解 x = i*m + j = {i}*{m} + {j} = {x}")
            print(f"验证 {g}^{x} mod {p} = {pow(g, x, p)} (期望值 {h})")
            return x
        current = (current * gm_inv) % p

    print("\n未找到解，离散对数不存在")
    return None


def test_discrete_log():
    """测试Shanks算法"""
    # 示例1：小参数测试
    g, h, p = 2, 9, 11
    print(f"\n=== 测试1：求解 {g}^x ≡ {h} mod {p} ===")
    x = shanks_algorithm(g, h, p)
    print(f"解：x = {x}")

    # 示例2：无解情况
    g, h, p = 2, 7, 11
    print(f"\n=== 测试2：求解 {g}^x ≡ {h} mod {p} ===")
    x = shanks_algorithm(g, h, p)
    print(f"解：x = {x}")

    # 示例3：稍大参数
    g, h, p = 3, 13, 17
    print(f"\n=== 测试3：求解 {g}^x ≡ {h} mod {p} ===")
    x = shanks_algorithm(g, h, p)
    print(f"解：x = {x}")


if __name__ == "__main__":
    test_discrete_log()
 