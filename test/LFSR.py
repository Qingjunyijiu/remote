class LFSR:
    def __init__(self, degree, taps, initial_state):
        """
        初始化LFSR

        参数:
            degree (int): LFSR的级数(位数)
            taps (list): 抽头位置列表(从1开始计数)
            initial_state (list): 初始状态列表(0和1的序列)
        """
        self.degree = degree
        self.taps = taps
        self.state = initial_state.copy()

        # 验证参数
        if len(self.state) != self.degree:
            raise ValueError("初始状态长度必须与级数相同")
        if any(x not in {0, 1} for x in self.state):
            raise ValueError("初始状态只能包含0和1")
        if any(tap < 1 or tap > self.degree for tap in self.taps):
            raise ValueError("抽头位置必须在1到级数范围内")

    def next_bit(self):
        """生成下一个比特并更新状态"""
        # 计算反馈位(XOR所有抽头位置的位)
        feedback = 0
        for tap in self.taps:
            feedback ^= self.state[tap - 1]

        # 输出最低位(或最高位，取决于实现)
        output = self.state[-1]

        # 右移状态
        self.state = [feedback] + self.state[:-1]

        return output

    def generate_sequence(self, length):
        """生成指定长度的输出序列"""
        sequence = []
        for _ in range(length):
            sequence.append(self.next_bit())
        return sequence


def read_config_file(filename):
    """从配置文件中读取LFSR参数"""
    with open(filename, 'r') as f:
        lines = f.readlines()

    # 解析每行参数
    degree = int(lines[0].strip())
    taps = list(map(int, lines[1].strip().split()))
    initial_state = list(map(int, lines[2].strip().split()))
    output_length = int(lines[3].strip())

    return degree, taps, initial_state, output_length


def main():
    # 配置文件示例 (也可以从命令行参数获取)
    config_file = "LFSR"

    try:
        # 读取配置文件
        degree, taps, initial_state, output_length = read_config_file(config_file)

        # 初始化LFSR
        lfsr = LFSR(degree, taps, initial_state)

        # 生成序列
        sequence = lfsr.generate_sequence(output_length)

        # 打印结果
        print("LFSR参数:")
        print(f"级数: {degree}")
        print(f"抽头系数: {taps}")
        print(f"初态: {initial_state}")
        print(f"\n生成的序列 (长度={output_length}):")
        print(''.join(map(str, sequence)))

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()