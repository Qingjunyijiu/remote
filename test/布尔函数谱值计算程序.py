import numpy as np


def read_boolean_function_config(config_file):
    """读取布尔函数配置文件"""
    with open(config_file, 'r') as f:
        lines = f.readlines()

    # 解析变元个数
    n = int(lines[0].strip())

    # 解析真值向量（允许有空格或没有空格）
    truth_vector_str = lines[1].strip().replace(" ", "")
    truth_vector = [int(c) for c in truth_vector_str]

    return n, truth_vector


def compute_walsh_spectrum(n, truth_vector):
    """计算布尔函数的Walsh谱"""
    N = 2 ** n
    spectrum = np.zeros(N, dtype=int)

    # 将布尔函数值从{0,1}转换为{-1,1}
    f = np.array([1 if x == 1 else -1 for x in truth_vector])

    # 计算所有可能的输入x和所有可能的w
    for w in range(N):
        total = 0
        for x in range(N):
            # 计算x与w的点积(mod 2)
            dot_product = 0
            for k in range(n):
                dot_product ^= ((x >> k) & 1) & ((w >> k) & 1)
            # 累加(-1)^(x·w) * f(x)
            total += (-1) ** dot_product * f[x]
        spectrum[w] = total

    return spectrum


def main():
    config_file = input("请输入配置文件路径: ")
    n, truth_vector = read_boolean_function_config(config_file)

    # 验证真值向量长度是否正确
    if len(truth_vector) != 2 ** n:
        print(f"错误: 变元个数为{n}, 真值向量长度应为{2 ** n}, 但得到的是{len(truth_vector)}")
        return

    spectrum = compute_walsh_spectrum(n, truth_vector)

    print("\n布尔函数信息:")
    print(f"变元个数: {n}")
    print(f"真值向量: {' '.join(map(str, truth_vector))}")

    print("\nWalsh谱值:")
    for w in range(len(spectrum)):
        # 将w表示为二进制形式，方便查看
        binary_str = format(w, f'0{n}b')
        print(f"w = {binary_str}: {spectrum[w]}")


if __name__ == "__main__":
    main()