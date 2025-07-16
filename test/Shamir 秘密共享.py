import random
from sympy import randprime  # 用于生成大素数

class ShamirSecretSharing:
    def __init__(self, threshold, total_shares, prime_bits=100):#是类的构造函数，用于初始化类的实例。
        """
        :param threshold: 门限值t（至少需要t个子秘密恢复密钥）
        :param total_shares: 总子秘密数n
        :param prime_bits: 素数p的比特长度（默认100比特）
        """
        self.threshold = threshold
        self.total_shares = total_shares
        self.p = randprime(2**(prime_bits-1), 2**prime_bits)  # 生成100比特素数

    def generate_polynomial(self, secret):
        """
        生成t-1次多项式，常数项为secret
        coefficients 是一个列表，用于存储多项式的系数。
        secret 作为第一个系数，即多项式在 x=0 处的值。
        random.randint(1, self.p-1) 生成一个在 1 到 self.p-1 之间的随机整数。self.p 是一个大素数，用于定义模运算的模数。
        for _ in range(self.threshold-1) 表示循环 threshold-1 次，每次生成一个随机整数。

        数学表示：f(x) = secret + a₁x + a₂x² + ... + aₜ₋₁xᵗ⁻¹ mod p
        """
        coefficients = [secret] + [random.randint(1, self.p-1) for _ in range(self.threshold-1)]
        return coefficients

    def evaluate_polynomial(self, coeffs, x):
        """
        计算多项式在x处的值（模p）
        enumerate 函数来遍历 coeffs 列表中的每一个系数及其对应的索引 i。
        enumerate 返回的是一个元组，其中第一个元素是索引，第二个元素是对应的系数。
        """
        y = 0
        for i, coeff in enumerate(coeffs):
            y += coeff * (x ** i)
        return y % self.p

    def generate_shares(self, secret):
        """
        生成n个子秘密（x_i, y_i）
        输出: [(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)]
        """
        if secret >= self.p:
            raise ValueError("Secret must be smaller than prime p.")
        coeffs = self.generate_polynomial(secret)
        shares = []
        for i in range(1, self.total_shares + 1):
            x = i  # 公开的x坐标（简单起见，设为1,2,...,n）
            y = self.evaluate_polynomial(coeffs, x)
            shares.append((x, y))
        return shares

    def reconstruct_secret(self, shares):
        """通过拉格朗日插值恢复秘密（k = h(0)）"""
        if len(shares) < self.threshold:
            raise ValueError(f"Need at least {self.threshold} shares to reconstruct.")

        def lagrange_basis(j, x=0):
            """
            计算拉格朗日基多项式在x处的值
            j 表示第j个子秘密的索引
            x 表示插值点
            """
            numerator, denominator = 1, 1
            x_j = shares[j][0]
            for i in range(len(shares)):
                if i != j:
                    x_i = shares[i][0]
                    numerator = (numerator * (x - x_i)) % self.p
                    denominator = (denominator * (x_j - x_i)) % self.p
            return (numerator * pow(denominator, -1, self.p)) % self.p

        secret = 0
        for j in range(len(shares)):
            y_j = shares[j][1]
            l_j = lagrange_basis(j)
            secret = (secret + y_j * l_j) % self.p
        return secret

#主程序入口
if __name__ == "__main__":
    # 参数设置
    threshold = 3  # 门限值t
    total_shares = 5  # 总子秘密数n
    secret = 123456789  # 要保护的秘密（需小于p）

    # 初始化Shamir方案
    sss = ShamirSecretSharing(threshold, total_shares, prime_bits=100)

    # 1. 秘密分发
    shares = sss.generate_shares(secret)
    print(f"生成的子秘密（{total_shares}个，至少需要{threshold}个恢复）：")
    for i, (x, y) in enumerate(shares):
        print(f"P_{x}: (x={x}, y={y})")

    # 2. 秘密重构（随机选择t个子秘密）
    selected_shares = random.sample(shares, threshold)
    print("\n用于恢复的子秘密：")
    for x, y in selected_shares:
        print(f"(x={x}, y={y})")

    reconstructed_secret = sss.reconstruct_secret(selected_shares)
    print(f"\n原始秘密: {secret}")
    print(f"恢复的秘密: {reconstructed_secret}")
    assert secret == reconstructed_secret, "恢复失败！"
    print("秘密恢复成功！")