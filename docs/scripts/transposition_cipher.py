#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
换位密码演示脚本

功能：
  1. 列换位密码（Columnar Transposition）加密
  2. 列换位密码解密
  3. 加密矩阵可视化
  4. 安全性分析（字母频率保持不变）
  5. 双列换位密码演示

使用方法：
  python transposition_cipher.py                              # 运行完整演示
  python transposition_cipher.py --encrypt "TEXT" -k "3142"   # 指定加密
  python transposition_cipher.py --decrypt "TEXT" -k "3142"   # 指定解密
  python transposition_cipher.py --double "TEXT" -k "3142"    # 双列换位
"""

from collections import Counter
import string


def parse_key(key_str: str) -> list:
    """
    将密钥字符串解析为列顺序列表

    支持两种格式：
    - 数字字符串: "3142" → [3, 1, 4, 2]
    - 单词密钥: "KEY" → 根据字母顺序 [2, 1, 3]（K=2, E=1, Y=3）

    Args:
        key_str: 密钥字符串

    Returns:
        列顺序列表（1-indexed）
    """
    if key_str.isdigit():
        return [int(c) for c in key_str]
    else:
        # 按字母在字母表中的顺序排列
        key_upper = key_str.upper()
        sorted_chars = sorted(enumerate(key_upper), key=lambda x: x[1])
        key_order = [0] * len(key_str)
        for rank, (idx, _) in enumerate(sorted_chars, 1):
            key_order[idx] = rank
        return key_order


def columnar_encrypt(plaintext: str, key: list) -> tuple:
    """
    列换位密码加密

    过程：
    1. 将明文按行写入固定列数的矩阵
    2. 按密钥指定的列顺序读出密文

    Args:
        plaintext: 明文字符串
        key: 列顺序列表（1-indexed），如 [3, 1, 4, 2]

    Returns:
        (密文字符串, 矩阵数据) 的元组
    """
    num_cols = len(key)
    # 移除空格（可选），保留原始字符
    text = plaintext.replace(' ', '_')

    # 计算需要的行数
    num_rows = len(text) // num_cols
    if len(text) % num_cols != 0:
        num_rows += 1

    # 用 '_' 填充
    padded_text = text.ljust(num_rows * num_cols, '_')

    # 构建矩阵
    matrix = []
    for row in range(num_rows):
        start = row * num_cols
        end = start + num_cols
        matrix.append(list(padded_text[start:end]))

    # 按密钥顺序读出密文
    # 先确定读列的顺序：按密钥值排序，得到列的读出顺序
    key_order = sorted(range(num_cols), key=lambda i: key[i])

    ciphertext_parts = []
    for col_idx in key_order:
        col_text = ''.join(matrix[row][col_idx] for row in range(num_rows))
        ciphertext_parts.append(col_text)

    ciphertext = ' '.join(ciphertext_parts)
    return ciphertext, matrix


def columnar_decrypt(ciphertext: str, key: list) -> str:
    """
    列换位密码解密

    过程：
    1. 根据密钥确定每列的长度
    2. 将密文按列填回矩阵
    3. 按行读出明文

    Args:
        ciphertext: 密文字符串
        key: 列顺序列表（1-indexed）

    Returns:
        解密后的明文字符串
    """
    # 移除密文中的空格分隔符
    cipher_clean = ciphertext.replace(' ', '')
    num_cols = len(key)
    num_rows = len(cipher_clean) // num_cols

    # 确定读列的顺序
    key_order = sorted(range(num_cols), key=lambda i: key[i])

    # 将密文分配到各列
    col_data = {}
    pos = 0
    for col_idx in key_order:
        col_data[col_idx] = cipher_clean[pos:pos + num_rows]
        pos += num_rows

    # 重建矩阵并按行读出
    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            result.append(col_data[col][row])

    plaintext = ''.join(result).replace('_', ' ')
    return plaintext


def print_matrix(matrix: list, key: list):
    """
    打印加密矩阵的可视化表示

    Args:
        matrix: 二维字符矩阵
        key: 列顺序列表
    """
    num_cols = len(key)
    key_order = sorted(range(num_cols), key=lambda i: key[i])

    # 打印密钥行
    key_str = "  密钥:    " + "  ".join(f"{key[i]}" for i in range(num_cols))
    print(key_str)

    # 打印读出顺序
    order_str = "  读出顺序: " + "  ".join(
        f"{key_order.index(i) + 1}" for i in range(num_cols)
    )
    print(order_str)

    # 打印矩阵
    for row_idx, row in enumerate(matrix):
        row_str = f"  第 {row_idx + 1} 行:  " + "  ".join(f" {c} " for c in row)
        print(row_str)

    # 按列读出说明
    print(f"\n按密钥顺序读出各列:")
    for rank, col_idx in enumerate(key_order):
        col_chars = ''.join(matrix[row][col_idx] for row in range(len(matrix)))
        print(f"  第 {rank + 1} 个读出 (原列 {col_idx + 1}): {col_chars}")


def analyze_frequency(text: str) -> dict:
    """
    分析文本的字母频率

    Args:
        text: 输入文本

    Returns:
        字典，键为字母，值为 (出现次数, 频率百分比)
    """
    letters = [c for c in text.upper() if c.isalpha() or c == '_']
    total = len(letters)
    if total == 0:
        return {}

    counts = Counter(letters)
    result = {}
    for char in sorted(counts, key=counts.get, reverse=True):
        result[char] = (counts[char], counts[char] / total * 100)

    return result


def double_transposition(plaintext: str, key: list) -> tuple:
    """
    双列换位密码

    对明文进行两次列换位加密，增强安全性。

    Args:
        plaintext: 明文
        key: 列顺序列表

    Returns:
        (最终密文, 中间密文) 的元组
    """
    # 第一次换位
    first_cipher, _ = columnar_encrypt(plaintext, key)
    first_clean = first_cipher.replace(' ', '')

    # 第二次换位
    second_cipher, _ = columnar_encrypt(first_clean, key)

    return second_cipher, first_cipher


def print_demo():
    """运行完整的演示程序"""
    print("=" * 48)
    print("  列换位密码演示程序")
    print("=" * 48)

    # --- 加密演示 ---
    print("\n--- 加密演示 ---")
    plaintext = "HELLO WORLD"
    key = [3, 1, 4, 2]
    print(f"明文: {plaintext}")
    print(f"密钥: {key}")

    ciphertext, matrix = columnar_encrypt(plaintext, key)

    print(f"\n加密矩阵:")
    print_matrix(matrix, key)
    print(f"\n密文: {ciphertext}")

    # --- 解密演示 ---
    print("\n--- 解密演示 ---")
    decrypted = columnar_decrypt(ciphertext, key)
    print(f"密文: {ciphertext}")
    print(f"密钥: {key}")
    print(f"明文: {decrypted}")

    # --- 不同密钥的效果 ---
    print("\n--- 不同密钥的加密效果 ---")
    text = "CRYPTOGRAPHY IS FUN"
    keys = [
        ([2, 4, 1, 3], "密钥 [2,4,1,3]"),
        ([3, 1, 4, 2], "密钥 [3,1,4,2]"),
        ([4, 3, 2, 1], "密钥 [4,3,2,1]（逆序）"),
    ]
    print(f"明文: {text}\n")
    for k, desc in keys:
        cipher, _ = columnar_encrypt(text, k)
        print(f"  {desc}: {cipher}")

    # --- 安全性分析 ---
    print("\n--- 安全性分析 ---")
    print("换位密码保持字母频率不变！\n")

    # 原文频率
    print("原文字母频率:")
    orig_freq = analyze_frequency(text)
    for char, (count, percent) in list(orig_freq.items())[:8]:
        bar = "█" * max(1, int(percent / 2))
        print(f"  {char}: {count} 次 ({percent:.1f}%) {bar}")

    # 密文频率
    cipher_text, _ = columnar_encrypt(text, [3, 1, 4, 2])
    print(f"\n密文字母频率:")
    cipher_freq = analyze_frequency(cipher_text)
    for char, (count, percent) in list(cipher_freq.items())[:8]:
        bar = "█" * max(1, int(percent / 2))
        print(f"  {char}: {count} 次 ({percent:.1f}%) {bar}")

    print("\n结论: 密文字母频率与原文完全相同！")
    print("这意味着频率分析可以判断密文是否由换位密码加密。")

    # --- 双列换位 ---
    print("\n--- 双列换位密码演示 ---")
    text2 = "MEET ME AT NOON"
    key2 = [3, 1, 4, 2]
    print(f"明文: {text2}")
    print(f"密钥: {key2}")

    double_cipher, first_cipher = double_transposition(text2, key2)
    print(f"\n第一次换位结果: {first_cipher}")
    print(f"第二次换位结果: {double_cipher}")

    # 验证双列换位的解密
    # 先解密第二次，再解密第一次
    first_decrypted = columnar_decrypt(double_cipher.replace(' ', ''), key2)
    final_decrypted = columnar_decrypt(first_decrypted.replace(' ', ''), key2).replace('_', ' ')
    print(f"\n解密验证: {final_decrypted}")

    # --- 换位密码的弱点 ---
    print("\n--- 换位密码的弱点 ---")
    print("""
1. 字母频率不变：
   - 密文中的字母频率与明文完全相同
   - 可以通过频率分析判断是否为换位密码

2. 可以通过已知明文攻击：
   - 如果攻击者知道部分明文，可以推断出换位规则

3. 双列换位可以增强安全性：
   - 两次换位使模式更难识别
   - 但仍不能抵抗现代密码分析
    """)


def main():
    """主入口函数"""
    import argparse

    parser = argparse.ArgumentParser(description="列换位密码加解密工具")
    parser.add_argument("--encrypt", "-e", type=str, help="加密明文")
    parser.add_argument("--decrypt", "-d", type=str, help="解密密文")
    parser.add_argument("-k", "--key", type=str, default="3142",
                        help="密钥 (默认: 3142)")
    parser.add_argument("--double", type=str, help="双列换位加密")
    parser.add_argument("--show-matrix", action="store_true",
                        help="显示加密矩阵")

    args = parser.parse_args()
    key = parse_key(args.key)

    if args.encrypt:
        ciphertext, matrix = columnar_encrypt(args.encrypt, key)
        print(f"明文: {args.encrypt}")
        print(f"密钥: {key}")
        if args.show_matrix:
            print(f"\n加密矩阵:")
            print_matrix(matrix, key)
        print(f"\n密文: {ciphertext}")
    elif args.decrypt:
        plaintext = columnar_decrypt(args.decrypt, key)
        print(f"密文: {args.decrypt}")
        print(f"密钥: {key}")
        print(f"明文: {plaintext}")
    elif args.double:
        double_cipher, first_cipher = double_transposition(args.double, key)
        print(f"明文: {args.double}")
        print(f"密钥: {key}")
        print(f"第一次换位: {first_cipher}")
        print(f"双列换位结果: {double_cipher}")
    else:
        # 无参数时运行完整演示
        print_demo()


if __name__ == "__main__":
    main()
