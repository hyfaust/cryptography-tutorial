---
title: 环境搭建指南
---

# :material-wrench: 环境搭建指南

在开始学习之前，请确保以下工具已正确安装和配置。

---

## :material-language-python: Python

本教程使用 Python 3.11+ 运行演示脚本。

```bash
# 验证安装
python --version
# Python 3.11.9

# 安装密码学库
pip install cryptography pycryptodome sympy
```

!!! info "常用库说明"

    | 库 | 用途 |
    |---|------|
    | `cryptography` | 现代密码学API（OpenSSL封装） |
    | `pycryptodome` | 经典密码学算法实现（DES/AES/等） |
    | `sympy` | 符号数学（数论计算） |

!!! tip "Windows 用户提示"

    如果文档中出现 Linux 专用命令（如 `xxd`、`base64` 等），可以通过以下方式替代：
    
    1. **WSL**（推荐）：在 WSL 终端中直接运行 Linux 命令
    2. **MinGW/Git Bash**：使用 Git for Windows 自带的 Bash 环境
    3. **Python/OpenSSL**：大多数功能都可以用 Python 脚本或 OpenSSL 命令替代

---

## :material-nodejs: Node.js

部分网络协议演示需要 Node.js 22+。

```bash
# 验证安装
node --version
# v22.21.0
```

---

## :material-lock-open-outline: OpenSSL

OpenSSL 是本教程最常用的命令行加密工具。

```bash
# 验证安装
openssl version
# OpenSSL 3.4.0

# Windows 用户：如果系统PATH中没有OpenSSL，
# 可以使用 GNU Octave 自带的版本，或自行安装
```

!!! tip "Windows 用户提示"

    如果 `openssl` 命令不可用，可以通过以下方式获取：
    
    1. 安装 [Git for Windows](https://git-scm.com/)（自带 OpenSSL）
    2. 安装 [Win64 OpenSSL](https://slproweb.com/products/Win32OpenSSL.html)
    3. 使用 WSL 中的 OpenSSL

---

## :material-hashing: hashcat

GPU 加速的密码哈希破解工具。

```bash
# 验证安装（本教程中已包含）
F:\Users\code_data\vibe\cryptography_learn\hashcat-7.1.2\hashcat.exe --version
# v7.1.2
```

!!! note "GPU 要求"

    hashcat 需要支持 CUDA 或 OpenCL 的 GPU。如果没有独立显卡，部分实验可能无法运行，但文档中的输出示例仍可供参考。

---

## :material-account-lock: John the Ripper

经典密码破解工具。

```bash
# 验证安装（本教程中已包含）
# 路径：F:\Users\code_data\vibe\cryptography_learn\john-1.9.0-jumbo-1-win64\run\john.exe
```

---

## :material-math-compass: SageMath

强大的数学计算系统，用于数论和椭圆曲线计算。安装完成后，请确保 `sage` 命令已加入系统 PATH。

```bash
# 验证安装
sage --version
```

!!! info "SageMath 使用方式"

    后续文档中所有 SageMath 命令统一使用 `sage`：

    ```bash
    # 交互模式
    sage

    # 单行命令
    sage -c 'print(gcd(48, 18))'
    ```

    对于简单的数论计算，Python 的 `sympy` 库也可以替代。

---

## :material-chef-hat: CyberChef

CyberChef 是一个基于浏览器的编码/解码/分析工具，**无需安装**。

直接在浏览器中打开本项目中已包含的 CyberChef 文件：

```
F:\Users\code_data\vibe\cryptography_learn\CyberChef_v10.19.4\CyberChef_v10.19.4.html
```

---

## :material-check-all: 环境检查清单

在开始学习前，确认以下检查项：

- [x] Python 3.11+ 可用
- [x] OpenSSL 3.x 可用
- [x] Node.js 22+ 可用
- [x] hashcat 可执行
- [x] John the Ripper 可执行
- [x] SageMath 可用
- [x] CyberChef HTML 文件可打开
- [x] `pip install cryptography pycryptodome sympy` 已执行

---

## :material-arrow-right: 准备就绪

环境搭建完成后，开始你的密码学学习之旅吧！

[:octicons-arrow-right-24: **模块1：密码学基础与古典密码**](01-foundations/index.md){ .md-button .md-button--primary }
