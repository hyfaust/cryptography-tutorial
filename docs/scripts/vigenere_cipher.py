#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
维吉尼亚密码加解密演示脚本

功能：
  1. 维吉尼亚密码加密
  2. 维吉尼亚密码解密
  3. 维吉尼亚方阵展示
  4. Kasiski 测试（确定密钥长度）
  5. 重合指数法（Index of Coincidence）

使用方法：
  python vigenere_cipher.py                              # 运行完整演示
  python vigenere_cipher.py --encrypt "TEXT" -k "KEY"    # 指定加密
  python vigenere_cipher.py --decrypt "TEXT" -k "KEY"    # 指定解密
  python vigenere_cipher.py --kasiski "CIPHERTEXT"       # Kasiski 测试
"""

from collections import Counter
from math import gcd
from functools import reduce


# 英语字母的标准频率（用于频率分析）
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074,
}


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    维吉尼亚密码加密

    数学公式: C_i = (P_i + K_{i mod m}) mod 26

    Args:
        plaintext: 明文字符串
        key: 密钥字符串（纯字母）

    Returns:
        加密后的密文字符串
    """
    # 预处理密钥：转大写，只保留字母
    key = [k for k in key.upper() if k.isalpha()]
    if not key:
        raise ValueError("密钥不能为空或全为非字母字符")

    result = []
    key_index = 0  # 密钥位置索引

    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # 获取当前密钥字母的偏移量
            k = ord(key[key_index % len(key)]) - ord('A')
            # 加密: (明文字母 + 密钥字母) mod 26
            encrypted = chr((ord(char.upper()) - ord('A') + k) % 26 + base)
            result.append(encrypted)
            key_index += 1
        else:
            # 非字母字符保持不变（不推进密钥位置）
            result.append(char)

    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    维吉尼亚密码解密

    数学公式: P_i = (C_i - K_{i mod m}) mod 26

    Args:
        ciphertext: 密文字符串
        key: 密钥字符串

    Returns:
        解密后的明文字符串
    """
    # 预处理密钥
    key = [k for k in key.upper() if k.isalpha()]
    if not key:
        raise ValueError("密钥不能为空或全为非字母字符")

    result = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            k = ord(key[key_index % len(key)]) - ord('A')
            # 解密: (密文字母 - 密钥字母) mod 26
            decrypted = chr((ord(char.upper()) - ord('A') - k) % 26 + base)
            result.append(decrypted)
            key_index += 1
        else:
            result.append(char)

    return ''.join(result)


def print_vigenere_table(rows: int = 6):
    """
    打印维吉尼亚方阵（前 N 行）

    维吉尼亚方阵是一个 26x26 的表格，
    第 i 行第 j 列的字母表示用第 i 个密钥加密第 j 个明文字母的结果。
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(f"\n    {' '.join(alphabet)}")
    print(f"    {'-' * 51}")
    for i in range(rows):
        row = alphabet[i:] + alphabet[:i]
        print(f"{alphabet[i]} | {' '.join(row)}")
    if rows < 26:
        print(f"... (共 26 行)")


def index_of_coincidence(text: str) -> float:
    """
    计算文本的重合指数（Index of Coincidence）

    重合指数 IC 的定义：随机选择两个字母，它们相同的概率。
    - 英语随机文本的 IC ≈ 0.065
    - 完全随机文本的 IC ≈ 0.038 (1/26)

    对于维吉尼亚密码：
    - 如果按正确的密钥长度分组，每组的 IC 应该接近 0.065
    - 如果分组不正确，IC 会接近 0.038

    Args:
        text: 只包含字母的文本

    Returns:
        重合指数值
    """
    text = [c for c in text.upper() if c.isalpha()]
    n = len(text)
    if n <= 1:
        return 0.0

    freq = Counter(text)
    # IC = sum(ni * (ni - 1)) / (n * (n - 1))
    # 其中 ni 是第 i 个字母的出现次数
    numerator = sum(count * (count - 1) for count in freq.values())
    denominator = n * (n - 1)
    return numerator / denominator if denominator > 0 else 0.0


def get_nth_chars(text: str, n: int, start: int = 0) -> str:
    """从文本中每隔 n 个字符提取一个字符"""
    letters = [c for c in text if c.isalpha()]
    return ''.join(letters[i] for i in range(start, len(letters), n))


def estimate_key_length(ciphertext: str, max_length: int = 20) -> list:
    """
    使用重合指数法估算密钥长度

    原理：对不同的假设密钥长度，将密文分组并计算每组的平均 IC。
    当假设的密钥长度正确时，平均 IC 最接近英语的 0.065。

    Args:
        ciphertext: 密文
        max_length: 最大尝试的密钥长度

    Returns:
        按 IC 与 0.065 的接近程度排序的 (密钥长度, 平均IC) 列表
    """
    # 只保留字母
    letters_only = ''.join(c for c in ciphertext.upper() if c.isalpha())
    results = []

    for key_len in range(1, min(max_length + 1, len(letters_only))):
        # 按假设的密钥长度分组
        groups = []
        for i in range(key_len):
            group = get_nth_chars(letters_only, key_len, i)
            groups.append(group)

        # 计算每组的 IC 并取平均值
        ic_values = [index_of_coincidence(g) for g in groups if len(g) > 1]
        avg_ic = sum(ic_values) / len(ic_values) if ic_values else 0
        results.append((key_len, avg_ic))

    # 按与英语 IC (0.065) 的接近程度排序
    results.sort(key=lambda x: abs(x[1] - 0.065))
    return results


def kasiski_test(ciphertext: str) -> dict:
    """
    Kasiski 测试

    原理：在密文中寻找重复的片段（长度 >= 3），
    计算重复片段之间的距离，这些距离的最大公约数很可能是密钥长度。

    Args:
        ciphertext: 密文

    Returns:
        字典，包含重复片段及其距离
    """
    # 只保留字母
    letters = ''.join(c for c in ciphertext.upper() if c.isalpha())
    repeats = {}  # 片段 -> 出现位置列表

    # 查找长度为 3 到 min(6, len//2) 的重复片段
    for length in range(3, min(7, len(letters) // 2 + 1)):
        for i in range(len(letters) - length + 1):
            segment = letters[i:i + length]
            if segment not in repeats:
                repeats[segment] = []
            repeats[segment].append(i)

    # 只保留出现多次的片段
    repeated = {seg: positions for seg, positions in repeats.items()
                if len(positions) > 1}

    # 计算距离
    distances = {}
    for seg, positions in repeated.items():
        dists = []
        for i in range(len(positions) - 1):
            dist = positions[i + 1] - positions[i]
            dists.append(dist)
        distances[seg] = dists

    return distances


def find_key_from_distances(distances: dict) -> int:
    """
    从 Kasiski 测试的距离中推断密钥长度

    取所有距离的最大公约数（GCD）作为密钥长度的估计。

    Args:
        distances: Kasiski 测试返回的距离字典

    Returns:
        估计的密钥长度
    """
    all_distances = []
    for dists in distances.values():
        all_distances.extend(dists)

    if not all_distances:
        return 0

    # 计算所有距离的 GCD
    result = reduce(gcd, all_distances)
    return result


def caesar_decrypt_char(cipher_char: str, key_char: str) -> str:
    """辅助函数：用单个密钥字符解密单个密文字符"""
    return chr((ord(cipher_char) - ord(key_char)) % 26 + ord('A'))


def crack_with_known_key_length(ciphertext: str, key_length: int) -> str:
    """
    已知密钥长度时，通过频率分析破解密钥

    原理：将密文按密钥长度分组，每组相当于一个凯撒密码。
    对每组使用频率分析找出对应的密钥字母。

    Args:
        ciphertext: 密文
        key_length: 密钥长度

    Returns:
        推测的密钥
    """
    letters = ''.join(c for c in ciphertext.upper() if c.isalpha())
    key = []

    for i in range(key_length):
        # 提取第 i 组字母
        group = get_nth_chars(letters, key_length, i)

        # 统计频率
        freq = Counter(group)
        most_common = freq.most_common(1)[0][0]

        # 假设最高频字母对应 'E'
        shift = (ord(most_common) - ord('E')) % 26
        key.append(chr(shift + ord('A')))

    return ''.join(key)


def print_demo():
    """运行完整的演示程序"""
    print("=" * 48)
    print("  维吉尼亚密码演示程序")
    print("=" * 48)

    # --- 加密演示 ---
    print("\n--- 加密演示 ---")
    plaintext = "ATTACKATDAWN"
    key = "LEMON"
    ciphertext = vigenere_encrypt(plaintext, key)
    print(f"明文: {plaintext}")
    print(f"密钥: {key}")
    print(f"密文: {ciphertext}")

    # --- 解密演示 ---
    print("\n--- 解密演示 ---")
    decrypted = vigenere_decrypt(ciphertext, key)
    print(f"密文: {ciphertext}")
    print(f"密钥: {key}")
    print(f"明文: {decrypted}")

    # --- 维吉尼亚方阵 ---
    print("\n--- 维吉尼亚方阵（前6行） ---")
    print_vigenere_table(6)

    # --- Kasiski 测试 ---
    print("\n--- Kasiski 测试演示 ---")
    # 使用更长的密文以便 Kasiski 测试有效
    long_plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    long_key = "SECRET"
    long_ciphertext = vigenere_encrypt(long_plaintext, long_key)
    print(f"明文: {long_plaintext}")
    print(f"密钥: {long_key}")
    print(f"密文: {long_ciphertext}")

    distances = kasiski_test(long_ciphertext)
    if distances:
        print("\n重复片段及距离:")
        for seg, dists in list(distances.items())[:5]:
            print(f"  '{seg}': 距离 = {dists}")

        estimated_len = find_key_from_distances(distances)
        print(f"\nKasiski 测试估计密钥长度: {estimated_len}")
    else:
        print("\n未找到重复片段（密文太短）")

    # --- 重合指数法 ---
    print("\n--- 重合指数法估算密钥长度 ---")
    ic_results = estimate_key_length(long_ciphertext, max_length=10)
    print("密钥长度 | 平均重合指数")
    print("-" * 30)
    for key_len, avg_ic in ic_results[:8]:
        bar = "█" * int(avg_ic * 100)
        print(f"  {key_len:2d}     | {avg_ic:.4f} {bar}")
    print(f"\n英语期望重合指数 ≈ 0.065")

    # --- 频率分析破解 ---
    print("\n--- 频率分析破解演示 ---")
    guessed_key = crack_with_known_key_length(long_ciphertext, len(long_key))
    print(f"推测密钥: {guessed_key}")
    guessed_plaintext = vigenere_decrypt(long_ciphertext, guessed_key)
    print(f"解密结果: {guessed_plaintext}")
    print(f"实际密钥: {long_key}")
    if guessed_key == long_key:
        print("✓ 密钥推测正确！")
    else:
        print("✗ 密钥推测不完全正确（密文较短时频率分析不够精确）")


def main():
    """主入口函数"""
    import argparse

    parser = argparse.ArgumentParser(description="维吉尼亚密码加解密工具")
    parser.add_argument("--encrypt", "-e", type=str, help="加密明文")
    parser.add_argument("--decrypt", "-d", type=str, help="解密密文")
    parser.add_argument("-k", "--key", type=str, default="LEMON", help="密钥 (默认: LEMON)")
    parser.add_argument("--kasiski", type=str, help="对密文进行 Kasiski 测试")
    parser.add_argument("--crack", type=str, help="尝试破解密文")
    parser.add_argument("--keylen", type=int, help="已知密钥长度（配合 --crack 使用）")

    args = parser.parse_args()

    if args.encrypt:
        result = vigenere_encrypt(args.encrypt, args.key)
        print(f"明文: {args.encrypt}")
        print(f"密钥: {args.key}")
        print(f"密文: {result}")
    elif args.decrypt:
        result = vigenere_decrypt(args.decrypt, args.key)
        print(f"密文: {args.decrypt}")
        print(f"密钥: {args.key}")
        print(f"明文: {result}")
    elif args.kasiski:
        print(f"=== Kasiski 测试 ===")
        print(f"密文: {args.kasiski}\n")

        distances = kasiski_test(args.kasiski)
        if distances:
            print("重复片段及距离:")
            for seg, dists in distances.items():
                print(f"  '{seg}': 距离 = {dists}")

            estimated_len = find_key_from_distances(distances)
            print(f"\n估计密钥长度: {estimated_len}")
        else:
            print("未找到足够长的重复片段（密文太短）")

        print(f"\n=== 使用重合指数法估算密钥长度 ===")
        print(f"密文长度: {len(args.kasiski)}")
        ic_results = estimate_key_length(args.kasiski)
        for key_len, avg_ic in ic_results[:10]:
            print(f"密钥长度 {key_len} 的重合指数: {avg_ic:.4f}")
        print(f"\n英语的期望重合指数约为 0.065")
        best = ic_results[0]
        print(f"最可能的密钥长度: {best[0]}（重合指数最接近 0.065）")
    elif args.crack:
        print(f"=== 频率分析破解 ===")
        print(f"密文: {args.crack}\n")

        # 先估算密钥长度
        if args.keylen:
            key_len = args.keylen
        else:
            ic_results = estimate_key_length(args.crack)
            key_len = ic_results[0][0]
            print(f"估算密钥长度: {key_len}")

        guessed_key = crack_with_known_key_length(args.crack, key_len)
        print(f"推测密钥: {guessed_key}")
        plaintext = vigenere_decrypt(args.crack, guessed_key)
        print(f"解密结果: {plaintext}")
    else:
        # 无参数时运行完整演示
        print_demo()


if __name__ == "__main__":
    main()
