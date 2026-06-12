#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字频分析工具脚本

功能：
  1. 统计文本中字母的出现频率
  2. 与英语标准频率对比
  3. 通过频率分析破解单表替换密码（包括凯撒密码）
  4. 生成频率分布的可视化柱状图
  5. 计算重合指数（Index of Coincidence）

使用方法：
  python frequency_analysis.py                            # 运行完整演示
  python frequency_analysis.py --analyze "CIPHERTEXT"     # 分析密文频率
  python frequency_analysis.py --decrypt "CIPHERTEXT"     # 尝试频率分析破解
  python frequency_analysis.py --ic "CIPHERTEXT"          # 计算重合指数
"""

from collections import Counter
import string

# 英语字母标准频率（百分比），来源：维基百科
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074,
}

# 英语字母频率排序（从高到低）
ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"


def count_letters(text: str) -> dict:
    """
    统计文本中每个字母的出现次数

    Args:
        text: 输入文本

    Returns:
        字典，键为大写字母，值为出现次数
    """
    text_upper = text.upper()
    counts = Counter(c for c in text_upper if c.isalpha())
    return dict(sorted(counts.items()))


def letter_frequency(text: str) -> dict:
    """
    计算文本中每个字母的频率（百分比）

    Args:
        text: 输入文本

    Returns:
        字典，键为大写字母，值为频率百分比
    """
    text_upper = text.upper()
    letters = [c for c in text_upper if c.isalpha()]
    total = len(letters)

    if total == 0:
        return {}

    counts = Counter(letters)
    freq = {}
    for char in string.ascii_uppercase:
        freq[char] = counts.get(char, 0) / total * 100

    return freq


def print_frequency_table(text: str, title: str = "字母频率分析"):
    """
    打印字母频率表格和柱状图

    Args:
        text: 要分析的文本
        title: 表格标题
    """
    freq = letter_frequency(text)
    counts = count_letters(text)
    total = sum(counts.values())

    print(f"\n--- {title} ---")
    print(f"文本长度: {len(text)} 字符，字母数: {total}")
    print(f"\n{'字母':>4} | {'次数':>4} | {'频率':>6} | {'柱状图'}")
    print("-" * 60)

    # 按频率从高到低排序
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    for char, percent in sorted_freq:
        if percent > 0:
            count = counts.get(char, 0)
            bar = "█" * max(1, int(percent / 1.5))
            print(f"  {char}  | {count:4d} | {percent:5.1f}% | {bar}")


def index_of_coincidence(text: str) -> float:
    """
    计算文本的重合指数（Index of Coincidence, IC）

    IC 定义：从文本中随机选取两个字母，它们相同的概率。

    数学公式:
    IC = Σ(n_i * (n_i - 1)) / (N * (N - 1))

    其中 n_i 是第 i 个字母的出现次数，N 是字母总数。

    参考值：
    - 英语自然文本: IC ≈ 0.065
    - 完全随机文本: IC ≈ 0.038 (1/26)
    - 单表替换密码: IC ≈ 0.065（保留了频率特征）
    - 多表替换密码: IC ≈ 0.038 ~ 0.065（取决于密钥长度）

    Args:
        text: 输入文本

    Returns:
        重合指数值
    """
    letters = [c for c in text.upper() if c.isalpha()]
    n = len(letters)
    if n <= 1:
        return 0.0

    counts = Counter(letters)
    numerator = sum(count * (count - 1) for count in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator if denominator > 0 else 0.0


def chi_squared(text: str) -> float:
    """
    计算卡方统计量（Chi-squared statistic）

    用于衡量文本的字母频率与英语标准频率的偏离程度。
    卡方值越小，文本越可能是英语明文或单表替换密文。

    Args:
        text: 输入文本

    Returns:
        卡方统计量
    """
    letters = [c for c in text.upper() if c.isalpha()]
    n = len(letters)
    if n == 0:
        return float('inf')

    counts = Counter(letters)
    chi2 = 0.0
    for char in string.ascii_uppercase:
        observed = counts.get(char, 0)
        expected = n * ENGLISH_FREQ[char] / 100
        if expected > 0:
            chi2 += (observed - expected) ** 2 / expected

    return chi2


def frequency_attack(ciphertext: str, num_guesses: int = 3) -> list:
    """
    使用频率分析攻击单表替换密码（以凯撒密码为例）

    原理：
    1. 统计密文字母频率
    2. 将最高频的密文字母映射到英语最高频字母
    3. 由此推算移位量，尝试解密
    4. 用卡方检验评估解密结果的质量

    Args:
        ciphertext: 密文
        num_guesses: 返回前 N 个最佳猜测

    Returns:
        列表，每个元素为 (推测密钥, 解密文本, 卡方值) 的元组
    """
    freq = letter_frequency(ciphertext)

    # 按频率排序
    sorted_chars = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    # 过滤掉频率为 0 的字母
    sorted_chars = [(c, f) for c, f in sorted_chars if f > 0]

    if not sorted_chars:
        return []

    guesses = []

    # 尝试将最高频的几个密文字母分别映射到英语高频字母
    top_cipher_chars = [c for c, _ in sorted_chars[:5]]

    for cipher_char in top_cipher_chars:
        for eng_char in ENGLISH_FREQ_ORDER[:5]:
            # 计算移位量
            shift = (ord(cipher_char) - ord(eng_char)) % 26

            # 用这个移位量解密
            decrypted = []
            for c in ciphertext:
                if c.isalpha():
                    base = ord('A') if c.isupper() else ord('a')
                    dec = chr((ord(c.upper()) - shift) % 26 + base)
                    if c.islower():
                        dec = dec.lower()
                    decrypted.append(dec)
                else:
                    decrypted.append(c)
            decrypted_text = ''.join(decrypted)

            # 用卡方检验评估
            chi2 = chi_squared(decrypted_text)
            guesses.append((shift, decrypted_text, chi2))

    # 去重并按卡方值排序
    seen = set()
    unique_guesses = []
    for shift, text, chi2 in guesses:
        if shift not in seen:
            seen.add(shift)
            unique_guesses.append((shift, text, chi2))

    unique_guesses.sort(key=lambda x: x[2])
    return unique_guesses[:num_guesses]


def print_demo():
    """运行完整的演示程序"""
    print("=" * 48)
    print("  字频分析演示程序")
    print("=" * 48)

    # --- 英语标准频率 ---
    print("\n--- 英语标准字母频率 ---")
    sorted_eng = sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)
    for char, percent in sorted_eng:
        bar = "█" * max(1, int(percent / 0.5))
        print(f"{char}: {percent:5.2f}% {bar}")

    # --- 分析英语文本 ---
    print("\n--- 分析英语文本 ---")
    sample_text = (
        "The quick brown fox jumps over the lazy dog. "
        "Pack my box with five dozen liquor jugs. "
        "How vexingly quick daft zebras jump!"
    )
    print(f"样本文本: {sample_text}")
    print_frequency_table(sample_text, "英语文本频率分析")

    # --- 分析凯撒密码密文 ---
    print("\n--- 分析凯撒密码密文 ---")
    # 密钥为 7 的凯撒密码
    secret_message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key = 7
    encrypted = ""
    for c in secret_message:
        if c.isalpha():
            base = ord('A')
            encrypted += chr((ord(c) - base + key) % 26 + base)
        else:
            encrypted += c

    print(f"原文: {secret_message}")
    print(f"密钥: {key}")
    print(f"密文: {encrypted}")
    print_frequency_table(encrypted, "密文字母频率分析")

    # --- 重合指数 ---
    print("\n--- 重合指数分析 ---")
    ic_english = index_of_coincidence(sample_text)
    ic_cipher = index_of_coincidence(encrypted)
    print(f"英语文本 IC: {ic_english:.4f} (期望 ≈ 0.065)")
    print(f"密文 IC:     {ic_cipher:.4f} (期望 ≈ 0.065)")
    print(f"\n说明: 单表替换密码的 IC 与明文接近，因为频率特征被保留")

    # --- 频率分析破解 ---
    print("\n--- 频率分析破解 ---")
    print(f"密文: {encrypted}\n")

    guesses = frequency_attack(encrypted, num_guesses=5)
    print("频率分析破解结果（按卡方值排序）:")
    for i, (shift, text, chi2) in enumerate(guesses):
        marker = " ★" if shift == key else ""
        print(f"  猜测 {i+1}: 密钥={shift:2d}, 卡方={chi2:8.1f} → {text}{marker}")

    # --- 更长文本的分析 ---
    print("\n--- 更长密文的频率分析 ---")
    long_text = (
        "Cryptography is the practice and study of techniques for secure communication "
        "in the presence of adversarial behavior. More generally, cryptography is about "
        "constructing and analyzing protocols that prevent third parties or the public "
        "from reading private messages."
    )
    long_key = 13
    long_encrypted = ""
    for c in long_text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            long_encrypted += chr((ord(c) - base + long_key) % 26 + base)
        else:
            long_encrypted += c

    print(f"原文: {long_text[:60]}...")
    print(f"密钥: {long_key}")
    print(f"密文: {long_encrypted[:60]}...")

    long_guesses = frequency_attack(long_encrypted, num_guesses=3)
    print(f"\n频率分析破解结果:")
    for i, (shift, text, chi2) in enumerate(long_guesses):
        marker = " ★" if shift == long_key else ""
        print(f"  猜测 {i+1}: 密钥={shift:2d}, 卡方={chi2:8.1f}")
        print(f"         → {text[:60]}...{marker}")


def main():
    """主入口函数"""
    import argparse

    parser = argparse.ArgumentParser(description="字频分析与密码破解工具")
    parser.add_argument("--analyze", "-a", type=str, help="分析文本的字母频率")
    parser.add_argument("--decrypt", "-d", type=str, help="使用频率分析尝试破解密文")
    parser.add_argument("--ic", type=str, help="计算文本的重合指数")
    parser.add_argument("--chi2", type=str, help="计算卡方统计量")

    args = parser.parse_args()

    if args.analyze:
        print_frequency_table(args.analyze, "字母频率分析")
        ic = index_of_coincidence(args.analyze)
        print(f"\n重合指数 (IC): {ic:.4f}")
    elif args.decrypt:
        print(f"=== 频率分析破解 ===")
        print(f"密文: {args.decrypt}\n")
        guesses = frequency_attack(args.decrypt, num_guesses=5)
        print("破解结果（按卡方值排序）:")
        for i, (shift, text, chi2) in enumerate(guesses):
            print(f"  猜测 {i+1}: 密钥={shift:2d}, 卡方={chi2:8.1f}")
            print(f"         → {text}")
    elif args.ic:
        ic = index_of_coincidence(args.ic)
        print(f"重合指数 (IC): {ic:.4f}")
        print(f"英语期望值:    0.0650")
        print(f"随机文本期望:  0.0385")
    elif args.chi2:
        chi2 = chi_squared(args.chi2)
        print(f"卡方统计量: {chi2:.2f}")
        print(f"值越小，越可能是英语明文")
    else:
        # 无参数时运行完整演示
        print_demo()


if __name__ == "__main__":
    main()
