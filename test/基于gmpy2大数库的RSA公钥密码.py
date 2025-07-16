import gmpy2
from gmpy2 import mpz, random_state
import binascii
import sys


class RSA:
    def __init__(self, key_size=1024):
        self.key_size = key_size
        self.rs = random_state()

    def generate_keys(self):
        # 生成两个大素数p和q
        p = gmpy2.next_prime(gmpy2.mpz_urandomb(self.rs, self.key_size // 2))
        q = gmpy2.next_prime(gmpy2.mpz_urandomb(self.rs, self.key_size // 2))
        """
        gmpy2.mpz_urandomb(self.rs, self.key_size // 2):
        生成一个均匀随机的大整数，其比特长度最多为 self.key_size / 2, 当key_size=1024时，生成的比特长度为512
        
        gmpy2.next_prime()：
        找到比该随机数大的下一个素数。
        """

        # 计算n = p * q
        n = p * q

        # 计算欧拉函数φ(n) = (p-1)*(q-1)
        phi = (p - 1) * (q - 1)

        # 选择公钥e，通常为65537
        e = mpz(65537)
        while gmpy2.gcd(e, phi) != 1:
            e = gmpy2.next_prime(e)
        """
        65537（即 2^16 + 1） 是最常用的 RSA 公钥指数，因为：
        它是素数（满足 RSA 的要求）。
        它的二进制形式 10000000000000001 只有两个 1，使得模幂运算（pow(m, e, n)）非常高效。
        它足够大，可以避免一些低指数攻击（如 e=3 可能面临的攻击）。
        
        gmpy2.gcd(e, phi) != 1:
        如果 gcd(e, phi) != 1，说明 e 和 phi 有公因子，此时需要重新选择 e。
        
        gmpy2.next_prime(e)：
        如果 e 和 phi 不互质，就选择比当前 e 大的下一个素数作为新的 e
        """

        # 计算私钥d，满足 e*d ≡ 1 mod φ(n)
        d = gmpy2.invert(e, phi)
        """gmpy2.invert(e, phi) 是 模逆元（Modular Inverse） 的计算函数"""

        # 返回公钥(n, e)和私钥(n, d)
        return (n, e), (n, d)

    def encrypt(self, public_key, plaintext):
        n, e = public_key
        # 将明文转换为整数
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        m = mpz(int.from_bytes(plaintext, byteorder='big'))
        """
        先通过 .encode('utf-8') 将其转换为 UTF-8 编码的字节流
        int.from_bytes(plaintext, byteorder='big') 将字节流解释为一个大整数。
        byteorder='big' 表示高位字节在前（类似大端序），这是密码学中的常见约定。
        例如，b'AB' 会转换为 0x4142（因为 A 的 ASCII 是 0x41，B 是 0x42）。
        mpz(...) 将 Python 的整数转换为 gmpy2 的高效大整数类型，支持后续的大数运算。
        """

        # 验证明文长度是否超过n的长度
        # 加密: c = m^e mod n
        c = gmpy2.powmod(m, e, n)
        return c

    def decrypt(self, private_key, ciphertext):
        n, d = private_key
        # 解密: m = c^d mod n
        m = gmpy2.powmod(ciphertext, d, n)
        """gmpy2.powmod(c, d, n)：高效计算 c^d mod n，即用私钥 d 解密密文 c。"""

        # 将整数转换回字节
        """
        plaintext = "Hello"
        byte_data = plaintext.encode('utf-8')           # 字符串 → 字节流
        m = int.from_bytes(byte_data, byteorder='big')  # 字节流 → 大整数
        c = pow(m, e, n)                                # 大整数 → 加密得到密文
        
        明文:人类可读的数据
        字节流	二进制数据（b'\x41\x42'）
        大整数	数学上的整数（如 16706）
        """
        plaintext = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
        try:
            return plaintext.decode('utf-8')
        except:
            return plaintext


def main():
    # 初始化RSA实例，使用2048位密钥
    rsa = RSA(2048)

    # 生成密钥对
    public_key, private_key = rsa.generate_keys()
    print(f"公钥 (n, e): {public_key}")
    print(f"私钥 (n, d): {private_key}")

    # 要加密的消息
    message = "这是一条使用RSA加密的测试消息。Hello RSA!"
    print(f"\n原始消息: {message}")

    # 加密
    ciphertext = rsa.encrypt(public_key, message)
    print(f"\n加密后的密文(整数形式): {ciphertext}")

    # 解密
    decrypted = rsa.decrypt(private_key, ciphertext)
    print(f"\n解密后的消息: {decrypted}")

    # 验证
    if isinstance(decrypted, str) and decrypted == message:
        print("\n验证成功: 解密后的消息与原始消息一致!")
    else:
        print("\n验证失败!")


if __name__ == "__main__":
    main()