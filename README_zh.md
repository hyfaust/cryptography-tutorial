# 密码学从入门到精通

[English](README.md) | [简体中文](README_zh.md)

---

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![MkDocs](https://img.shields.io/badge/MkDocs-1.6.1-green.svg)](https://www.mkdocs.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-学习资源-brightgreen.svg)]()

> **⚠️ 声明：本项目的所有内容，包括文档、代码示例和脚本，均由 AI（人工智能）生成。内容仅供学习参考，使用前请自行验证其准确性，切勿直接用于生产环境或安全关键场景。**

一套系统化的密码学学习资源，包含 7 个递进式模块、39 篇文档和 26 个 Python 实战脚本。基于 MkDocs Material 主题构建，提供交互式阅读体验。

## 目录

- [简介](#简介)
- [学习路线](#学习路线)
- [模块概览](#模块概览)
- [工具链](#工具链)
- [环境要求](#环境要求)
- [安装](#安装)
- [使用方法](#使用方法)
- [项目结构](#项目结构)
- [参与贡献](#参与贡献)
- [许可证](#许可证)
- [致谢](#致谢)

## 简介

本教程通过 **25 个递进式主题**，带你从零基础到深入理解现代密码学的核心原理与实战技术。每个主题包含：

- 核心概念和术语的详细解释
- 使用行业标准工具的动手实验
- 可执行的 Python 演示脚本
- 练习题和延伸阅读

## 学习路线

```
模块1  ──▶  模块2  ──▶  模块2b  ──▶  模块3  ──▶  模块4  ──▶  模块5  ──▶  模块6
 基础        哈希        随机数       对称加密      非对称加密     密码破解       高级应用
  ⭐          ⭐⭐         ⭐⭐         ⭐⭐⭐        ⭐⭐⭐⭐       ⭐⭐⭐⭐⭐      ⭐⭐⭐⭐⭐⭐
```

## 模块概览

| 模块 | 主题数 | 核心内容 |
|------|--------|---------|
| **1 — 基础** | 5 | 古典密码、凯撒密码、维吉尼亚密码、编码与加密的区别 |
| **2 — 哈希** | 4 | MD5、SHA-256、碰撞攻击、HMAC、密码哈希与盐值 |
| **2b — 随机数** | 3 | TRNG/PRNG/CSPRNG、HMAC-DRBG、随机数攻击案例 |
| **3 — 对称加密** | 4 | DES、AES、分组密码模式（ECB/CBC/CTR/GCM）、流密码 |
| **4 — 非对称加密** | 4 | 数论基础、RSA、椭圆曲线、Diffie-Hellman |
| **5 — 密码破解** | 5 | 频率分析、hashcat、John the Ripper、RSA 攻击 |
| **6 — 高级应用** | 5 | 数字签名、PKI、TLS/SSL、零知识证明、后量子密码 |

## 工具链

| 工具 | 用途 |
|------|------|
| **OpenSSL** | 加密、哈希、证书管理、密钥生成 |
| **CyberChef** | 可视化编码/解码与分析 |
| **hashcat** | GPU 加速哈希破解 |
| **John the Ripper** | 密码哈希破解 |
| **SageMath** | 数论计算与椭圆曲线 |
| **Python** | 脚本演示与算法实现 |
| **Node.js** | 网络协议演示 |

## 环境要求

| 依赖 | 版本 | 是否必需 |
|------|------|---------|
| Python | >= 3.11 | 是 |
| OpenSSL | >= 3.x | 是 |
| Node.js | >= 18 | 否（仅模块6） |
| SageMath | >= 9.x | 否（模块4-6） |
| hashcat | >= 7.x | 否（仅模块5） |
| John the Ripper | jumbo | 否（仅模块5） |

## 安装

```bash
# 进入项目目录
cd cryptography_learn/crypto-tutorial

# 安装 Python 依赖
pip install cryptography pycryptodome sympy

# 构建站点
mkdocs build

# 本地预览
mkdocs serve -a 127.0.0.1:8888
```

在浏览器中打开 `http://127.0.0.1:8888`。

## 使用方法

### 阅读文档

构建后的站点提供：

- **深色/浅色主题切换**
- **代码块一键复制**
- **Mermaid 图表**可视化解释
- **KaTeX 数学公式**渲染
- **标签页**多工具对比演示
- **全文搜索**

### 运行脚本

所有 26 个 Python 脚本位于 `docs/scripts/` 目录：

```bash
cd docs/scripts

# 古典密码演示
python caesar_cipher.py --encrypt "HELLO" --key 3
python vigenere_cipher.py --encrypt "HELLO" --key "SECRET"

# 哈希演示
python hash_demo.py
python birthday_attack.py --attack

# 随机数演示
python random_demo.py --predict
python randomness_attack.py --ecdsa

# 对称加密演示
python aes_demo.py
python block_modes_demo.py

# 数论与非对称加密演示
python number_theory_demo.py
python rsa_demo.py
python ecc_demo.py
python dh_demo.py

# RSA 攻击演示
python rsa_small_e.py
python rsa_common_modulus.py
python rsa_wiener.py

# 高级应用演示
python rsa_signature.py
python ecdsa_demo.py
python zkp_demo.py
```

## 项目结构

```
crypto-tutorial/
├── mkdocs.yml                  # MkDocs 配置文件
├── LICENSE                     # GPL v3 许可证
├── README.md                   # 英文 README
├── README_zh.md                # 中文 README（本文件）
├── docs/
│   ├── index.md                # 站点首页
│   ├── getting-started.md      # 环境搭建指南
│   ├── stylesheets/            # 自定义样式
│   ├── javascripts/            # 自定义脚本
│   ├── scripts/                # 26 个 Python 演示脚本
│   ├── 01-foundations/          # 模块1：古典密码
│   ├── 02-hashing/              # 模块2：哈希函数
│   ├── 02b-random/              # 模块2b：随机数
│   ├── 03-symmetric/            # 模块3：对称加密
│   ├── 04-asymmetric/           # 模块4：非对称加密
│   ├── 05-cryptanalysis/        # 模块5：密码破解
│   └── 06-advanced/             # 模块6：高级应用
└── site/                       # 构建输出目录（自动生成）
```

## 参与贡献

欢迎提交 Issue 或 Pull Request！

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add amazing feature'`）
4. 推送分支（`git push origin feature/amazing-feature`）
5. 发起 Pull Request

## 许可证

本项目基于 **GNU 通用公共许可证 v3.0** 发布 — 详见 [LICENSE](LICENSE) 文件。

## 致谢

- [MkDocs](https://www.mkdocs.org/) 和 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 提供文档框架
- [OpenSSL](https://www.openssl.org/) 提供密码学工具
- [CyberChef](https://github.com/gchq/CyberChef)（GCHQ）提供编码/解码工具
- [hashcat](https://hashcat.net/) 和 [John the Ripper](https://www.openwall.com/john/) 提供密码审计工具
- [SageMath](https://www.sagemath.org/) 提供数学计算
- [Python cryptography](https://cryptography.io/) 和 [PyCryptodome](https://pycryptodome.readthedocs.io/) 库
