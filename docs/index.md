---
title: 密码学从入门到精通
hide:
  - navigation
---

# :material-lock: 密码学从入门到精通

> **Cryptography Learning Path — From Beginner to Expert**

欢迎来到密码学学习之旅！本教程通过 **25 个递进式主题**，带你从零基础到深入理解现代密码学的核心原理与实战技术。

---

## :material-map: 学习路线

```mermaid
graph LR
    A["模块1<br>基础与古典密码"] --> B["模块2<br>哈希函数"]
    B --> B2["模块2b<br>CSPRNG与随机数"]
    B2 --> C["模块3<br>对称加密"]
    C --> D["模块4<br>非对称加密"]
    D --> E["模块5<br>密码破解"]
    E --> F["模块6<br>高级应用"]

    style A fill:#4CAF50,color:#fff
    style B fill:#8BC34A,color:#fff
    style B2 fill:#66BB6A,color:#fff
    style C fill:#FFC107,color:#000
    style D fill:#FF9800,color:#fff
    style E fill:#FF5722,color:#fff
    style F fill:#F44336,color:#fff
```

---

## :material-school: 模块概览

=== "⭐ 模块1 — 基础"

    **密码学基础与古典密码**

    了解密码学的历史与基本概念，掌握编码与加密的区别，动手实现凯撒密码、维吉尼亚密码等古典加密方法。

    [:octicons-arrow-right-24: 开始学习](01-foundations/index.md)

=== "⭐⭐ 模块2 — 哈希"

    **哈希函数与消息完整性**

    深入理解哈希函数的原理与安全性，学习 HMAC、密码哈希与盐值机制，了解哈希碰撞的实际影响。

    [:octicons-arrow-right-24: 开始学习](02-hashing/index.md)

=== "⭐⭐ 模块2b — 随机数"

    **CSPRNG与随机数生成**

    理解密码学安全随机数的重要性，学习 TRNG/PRNG/CSPRNG 的区别，了解 HMAC-DRBG 等算法，通过真实攻击案例认识弱随机数的致命后果。

    [:octicons-arrow-right-24: 开始学习](02b-random/index.md)

=== "⭐⭐⭐ 模块3 — 对称加密"

    **对称加密**

    学习 DES、AES 等对称加密算法的工作原理，理解分组密码的各种模式（ECB/CBC/CTR/GCM）及其安全性差异。

    [:octicons-arrow-right-24: 开始学习](03-symmetric/index.md)

=== "⭐⭐⭐⭐ 模块4 — 非对称加密"

    **非对称加密与数论**

    掌握密码学所需的数论基础，深入理解 RSA 算法的数学原理，探索椭圆曲线密码学和密钥交换协议。

    [:octicons-arrow-right-24: 开始学习](04-asymmetric/index.md)

=== "⭐⭐⭐⭐⭐ 模块5 — 密码破解"

    **密码破解实战**

    使用 hashcat、John the Ripper 等工具进行哈希破解实战，学习 RSA 的多种攻击方法，理解密码系统的脆弱性。

    [:octicons-arrow-right-24: 开始学习](05-cryptanalysis/index.md)

=== "⭐⭐⭐⭐⭐⭐ 模块6 — 高级"

    **高级应用与现代密码学**

    探索数字签名、PKI 证书体系、TLS 协议，了解零知识证明和后量子密码学的前沿发展。

    [:octicons-arrow-right-24: 开始学习](06-advanced/index.md)

---

## :material-tools: 工具链

本教程使用的工具：

| 工具 | 用途 | 模块 |
|------|------|------|
| **OpenSSL** | 加密算法实现、证书管理 | 1-6 |
| **CyberChef** | 编码解码、可视化分析 | 1-3, 5 |
| **hashcat** | GPU加速哈希破解 | 5 |
| **John the Ripper** | 密码哈希破解 | 5 |
| **SageMath** | 数论计算、椭圆曲线 | 4-6 |
| **Python** | 脚本演示、算法实现 | 1-6 |
| **Node.js** | 网络协议演示 | 6 |

---

## :material-information: 如何使用本教程

!!! tip "学习建议"

    1. **按顺序学习**：模块之间有递进关系，建议从模块1开始
    2. **动手实践**：每个主题都有配套的命令和脚本，请亲自运行
    3. **理解原理**：不要只记操作，要理解背后的数学和安全原理
    4. **完成练习**：每个主题末尾的练习题是巩固知识的好方法

!!! warning "安全声明"

    本教程中的密码破解技术**仅用于教育目的**，帮助理解密码系统的安全性。请勿将这些技术用于未授权的系统攻击。
