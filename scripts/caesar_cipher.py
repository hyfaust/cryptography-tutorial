#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
凯撒密码加解密演示脚本

功能：
  1. 凯撒密码加密
  2. 凯撒密码解密
  3. 暴力破解（尝试所有25种密钥）
  4. 频率分析辅助破解

使用方法：
  python caesar_cipher.py                        # 运行完整演示
  python caesar_cipher.py --encrypt "TEXT" -k 3  # 指定加密
  python caesar_cipher.py --decrypt "TEXT" -k 3  # 指定解密
  python caesar_cipher.py --bruteforce "TEXT"    # 暴力破解
"""


def caesar_encrypt(plaintext: str, key: int) -> str:
    """
    凯撒密码加密函数

    数学公式: E(x) = (x + key) mod 26
    其中 x 是字母对应的数字（A=0, B=1, ..., Z=25）

    Args:
        plaintext: 明文字符串（支持大小写）
        key: 移位密钥（0-25）

    Returns:
        加密后的密文字符串
    """
    result = []
    key = key % 26  # 确保密钥在 0-25 范围内

    for char in plaintext:
        if char.isalpha():
            # 确定基准字符（大写用 'A'，小写用 'a'）
            base = ord('A') if char.isupper() else ord('a')
            # 将字符转换为数字（0-25），应用移位，再转回字符
            encrypted_char = chr((ord(char) - base + key) % 26 + base)
            result.append(encrypted_char)
        else:
            # 非字母字符保持不变
            result.append(char)

    return ''.join(result)


def caesar_decrypt(ciphertext: str, key: int) -> str:
    """
    凯撒密码解密函数

    数学公式: D(y) = (y - key) mod 26
    解密就是反向移位，等价于用 (26 - key) 进行加密

    Args:
        ciphertext: 密文字符串
        key: 移位密钥（0-25）

    Returns:
        解密后的明文字符串
    """
    # 解密 = 用 (26 - key) 加密
    return caesar_encrypt(ciphertext, 26 - (key % 26))


def caesar_bruteforce(ciphertext: str) -> list:
    """
    凯撒密码暴力破解

    尝试所有 25 种可能的密钥，返回所有解密结果。
    对于凯撒密码，这是最直接的破解方式。

    Args:
        ciphertext: 密文字符串

    Returns:
        列表，每个元素为 (密钥, 解密结果) 的元组
    """
    results = []
    for key in range(1, 26):  # 密钥 0 等于不加密，跳过
        decrypted = caesar_decrypt(ciphertext, key)
        results.append((key, decrypted))
    return results


def frequency_analysis(text: str) -> dict:
    """
    字频分析

    统计文本中每个字母的出现频率。
    英语中最高频的字母是 E (12.7%), T (9.1%), A (8.2%)...

    Args:
        text: 要分析的文本

    Returns:
        字典，键为字母，值为 (出现次数, 频率百分比)
    """
    # 只统计字母，忽略大小写
    letters = [c for c in text.upper() if c.isalpha()]
    total = len(letters)

    if total == 0:
        return {}

    # 统计每个字母的出现次数
    freq = {}
    for char in letters:
        freq[char] = freq.get(char, 0) + 1

    # 转换为百分比并排序
    result = {}
    for char in sorted(freq, key=freq.get, reverse=True):
        result[char] = (freq[char], freq[char] / total * 100)

    return result


def guess_key_by_frequency(ciphertext: str) -> int:
    """
    通过频率分析猜测凯撒密码的密钥

    原理：英语中出现频率最高的字母是 'E'，
    所以密文中出现频率最高的字母很可能对应 'E'。

    Args:
        ciphertext: 密文

    Returns:
        最可能的密钥值
    """
    freq = frequency_analysis(ciphertext)
    if not freq:
        return 0

    # 获取密文中频率最高的字母
    most_frequent = list(freq.keys())[0]

    # 假设它对应 'E'，计算密钥
    # 密钥 = (密文字母 - 'E') mod 26
    key = (ord(most_frequent) - ord('E')) % 26
    return key


def print_demo():
    """运行完整的演示程序"""
    print("=" * 48)
    print("  凯撒密码演示程序")
    print("=" * 48)

    # --- 加密演示 ---
    print("\n--- 加密演示 ---")
    plaintext = "HELLO WORLD"
    key = 3
    ciphertext = caesar_encrypt(plaintext, key)
    print(f"明文: {plaintext}")
    print(f"密钥: {key}")
    print(f"密文: {ciphertext}")

    # --- 解密演示 ---
    print("\n--- 解密演示 ---")
    decrypted = caesar_decrypt(ciphertext, key)
    print(f"密文: {ciphertext}")
    print(f"密钥: {key}")
    print(f"明文: {decrypted}")

    # --- 暴力破解 ---
    print("\n--- 暴力破解（尝试所有25种密钥） ---")
    print(f"密文: {ciphertext}")
    results = caesar_bruteforce(ciphertext)
    for k, text in results:
        marker = "    <-- 正确明文" if k == key else ""
        print(f"密钥 {k:2d}: {text}{marker}")

    # --- 频率分析 ---
    print("\n--- 频率分析演示 ---")
    longer_text = "The quick brown fox jumps over the lazy dog"
    encrypted_long = caesar_encrypt(longer_text, 7)
    print(f"原文: {longer_text}")
    print(f"密钥: 7")
    print(f"密文: {encrypted_long}")

    print("\n密文字母频率分析:")
    freq = frequency_analysis(encrypted_long)
    for char, (count, percent) in list(freq.items())[:10]:
        bar = "█" * int(percent / 2)
        print(f"  {char}: {count:2d} 次 ({percent:5.1f}%) {bar}")

    guessed_key = guess_key_by_frequency(encrypted_long)
    print(f"\n频率分析猜测密钥: {guessed_key}")
    print(f"尝试解密: {caesar_decrypt(encrypted_long, guessed_key)}")
    if guessed_key != 7:
        print(f"（猜测不正确，因为密文较短，频率统计不够准确）")
        print(f"正确密钥: 7")
        print(f"正确解密: {caesar_decrypt(encrypted_long, 7)}")


def main():
    """主入口函数"""
    import argparse

    parser = argparse.ArgumentParser(description="凯撒密码加解密工具")
    parser.add_argument("--encrypt", "-e", type=str, help="加密明文")
    parser.add_argument("--decrypt", "-d", type=str, help="解密密文")
    parser.add_argument("--bruteforce", "-b", type=str, help="暴力破解密文")
    parser.add_argument("-k", "--key", type=int, default=3, help="密钥 (默认: 3)")

    args = parser.parse_args()

    if args.encrypt:
        result = caesar_encrypt(args.encrypt, args.key)
        print(f"明文: {args.encrypt}")
        print(f"密钥: {args.key}")
        print(f"密文: {result}")
    elif args.decrypt:
        result = caesar_decrypt(args.decrypt, args.key)
        print(f"密文: {args.decrypt}")
        print(f"密钥: {args.key}")
        print(f"明文: {result}")
    elif args.bruteforce:
        print(f"=== 暴力破解凯撒密码 ===")
        print(f"密文: {args.bruteforce}\n")
        results = caesar_bruteforce(args.bruteforce)
        for k, text in results:
            print(f"密钥 {k:2d}: {text}")
    else:
        # 无参数时运行完整演示
        print_demo()


if __name__ == "__main__":
    main()
