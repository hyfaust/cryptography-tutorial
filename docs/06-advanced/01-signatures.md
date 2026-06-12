---
title: 6.1 数字签名
---

# 6.1 数字签名

## 学习目标

- 理解数字签名的三大安全性质：认证性、完整性、不可否认性
- 掌握 RSA 数字签名的原理，区分签名与加密的密钥使用方式
- 理解 ECDSA 签名算法的工作流程
- 能够使用 OpenSSL 和 Python 完成签名与验证操作
- 了解数字签名在代码签名、区块链等领域的实际应用

## 前置知识

- 哈希函数的性质（模块2：SHA-256、抗碰撞性）
- RSA 算法原理（模块4：模幂运算、公钥/私钥）
- 椭圆曲线基础（模块4：ECC 概念）

## 核心概念与术语

### 数字签名的本质

数字签名是手写签名的数字化对应物，但远比手写签名安全。它解决了一个核心问题：**如何在数字世界中证明一段消息确实来自某个特定的发送者，且未被篡改？**

数字签名提供三个关键安全保证：

| 性质 | 含义 | 类比 |
|------|------|------|
| **认证性** (Authentication) | 消息确实由声称的发送者创建 | 手写签名验证笔迹 |
| **完整性** (Integrity) | 消息在传输过程中未被修改 | 文件上的骑缝章 |
| **不可否认性** (Non-repudiation) | 签名者事后无法否认签名行为 | 公证处的公证 |

!!! note "签名 vs 加密"
    数字签名和加密是两个独立的操作：

    - **加密**：用接收者的 **公钥** 加密，用接收者的 **私钥** 解密 → 保密性
    - **签名**：用发送者的 **私钥** 签名，用发送者的 **公钥** 验证 → 认证性

    两者可以组合使用：先签名再加密，同时实现认证性和保密性。

### RSA 数字签名

RSA 签名利用了 RSA 算法的数学性质，但密钥使用方向与加密相反。

#### RSA 加密回顾

$$
\text{加密}: C = M^e \bmod n
$$

$$
\text{解密}: M = C^d \bmod n
$$

- 加密用 **公钥** $(e, n)$
- 解密用 **私钥** $(d, n)$

#### RSA 签名

RSA 签名的过程分为两步：先对消息计算哈希，再用私钥对哈希值进行"解密"操作。

**签名过程：**

1. 计算消息的哈希值：$H = \text{Hash}(m)$
2. 用私钥签名：$S = H^d \bmod n$

$$
S = H(m)^d \bmod n
$$

**验证过程：**

1. 用公钥计算：$H' = S^e \bmod n$
2. 计算消息的哈希值：$H = \text{Hash}(m)$
3. 比较：$H' \stackrel{?}{=} H$

$$
\text{验证}: H(m) \stackrel{?}{=} S^e \bmod n
$$

!!! tip "为什么先哈希再签名？"
    直接对消息签名 $S = m^d \bmod n$ 存在两个问题：

    1. **效率**：消息可能很长，模幂运算代价高
    2. **安全**：存在乘法同态性攻击 —— $\text{Sig}(m_1) \times \text{Sig}(m_2) = \text{Sig}(m_1 \times m_2)$

    使用哈希 + 填充方案（如 PSS）可以同时解决这两个问题。

#### RSA-PSS 填充方案

裸 RSA 签名（教科书 RSA）不安全。实践中使用 **PSS (Probabilistic Signature Scheme)** 填充：

$$
\text{EM} = \text{PSS-Encode}(H(m), \text{salt})
$$

$$
S = \text{EM}^d \bmod n
$$

PSS 引入随机盐值，使每次签名结果不同，增强安全性。

### ECDSA 签名

**ECDSA (Elliptic Curve Digital Signature Algorithm)** 是基于椭圆曲线离散对数问题的签名算法。

#### 数学基础

在椭圆曲线 $E$ 上，给定基点 $G$ 和公钥 $Q = dG$（$d$ 为私钥），已知 $Q$ 和 $G$ 求 $d$ 是困难的（椭圆曲线离散对数问题，ECDLP）。

#### ECDSA 签名过程

给定消息 $m$，私钥 $d$，曲线阶 $n$：

1. 计算 $e = \text{Hash}(m)$
2. 选择随机数 $k \in [1, n-1]$（**必须真正随机，绝不重复！**）
3. 计算 $(x_1, y_1) = kG$
4. 计算 $r = x_1 \bmod n$，若 $r = 0$ 则重新选 $k$
5. 计算 $s = k^{-1}(e + rd) \bmod n$，若 $s = 0$ 则重新选 $k$
6. 签名为 $(r, s)$

#### ECDSA 验证过程

给定签名 $(r, s)$，公钥 $Q$，消息 $m$：

1. 计算 $e = \text{Hash}(m)$
2. 计算 $w = s^{-1} \bmod n$
3. 计算 $u_1 = ew \bmod n$，$u_2 = rw \bmod n$
4. 计算 $(x_1, y_1) = u_1 G + u_2 Q$
5. 验证 $r \stackrel{?}{=} x_1 \bmod n$

!!! warning "ECDSA 随机数安全"
    ECDSA 的安全性严重依赖随机数 $k$ 的质量：

    - **$k$ 重复使用**：攻击者可以通过两个使用相同 $k$ 的签名直接计算出私钥 $d$
    - **$k$ 可预测**：同样可以恢复私钥

    索尼 PS3 曾因使用固定的 $k$ 值导致私钥被破解！

    **解决方案**：确定性 ECDSA (RFC 6979) 使用 $k = \text{HMAC}(d, h)$ 生成确定性随机数。

### RSA 签名 vs ECDSA 对比

| 特性 | RSA-2048 | ECDSA P-256 |
|------|----------|-------------|
| 安全级别 | ~112 bits | ~128 bits |
| 密钥大小 | 2048 bits (256 bytes) | 256 bits (32 bytes) |
| 签名大小 | 256 bytes | ~64 bytes |
| 签名速度 | 较慢 | 较快 |
| 验证速度 | 较快 | 较慢 |
| 量子威胁 | Shor 算法可破解 | Shor 算法可破解 |
| 标准化 | PKCS#1, PSS | FIPS 186-4, RFC 6979 |
| 应用场景 | TLS、代码签名 | Bitcoin、TLS 1.3、SSH |

## 动手实践

### 实验1：RSA 数字签名（OpenSSL）

使用 OpenSSL 生成 RSA 密钥对、签名和验证消息。

**准备工作：创建消息文件**

```bash
echo "This is a secret message for RSA signature demo." > message.txt
```

**生成 RSA 密钥对**

```bash
# 生成 2048 位 RSA 私钥
openssl genrsa -out sign_private.pem 2048

# 提取公钥
openssl rsa -in sign_private.pem -pubout -out sign_public.pem

# 查看私钥信息
openssl rsa -in sign_private.pem -text -noout | head -5
```

**签名消息**

```bash
# 使用 SHA-256 哈希 + 私钥签名
openssl dgst -sha256 -sign sign_private.pem -out signature.bin message.txt

# 查看签名的十六进制表示
xxd signature.bin | head -10
```

**验证签名**

```bash
# 使用公钥验证签名
openssl dgst -sha256 -verify sign_public.pem -signature signature.bin message.txt

# 篡改消息后再验证
echo "This is a TAMPERED message!" > tampered.txt
openssl dgst -sha256 -verify sign_public.pem -signature signature.bin tampered.txt
```

预期输出：

```console
# 验证成功
Verified OK

# 篡改后验证失败
Verification Failure
```

### 实验2：ECDSA 数字签名（OpenSSL）

**生成 ECDSA 密钥对**

```bash
# 生成 P-256 曲线的私钥
openssl ecparam -genkey -name prime256v1 -out ec_sign_private.pem

# 提取公钥
openssl ec -in ec_sign_private.pem -pubout -out ec_public.pem

# 查看密钥信息
openssl ec -in ec_sign_private.pem -text -noout
```

**签名和验证**

```bash
# ECDSA 签名
openssl dgst -sha256 -sign ec_sign_private.pem -out ec_signature.bin message.txt

# ECDSA 验证
openssl dgst -sha256 -verify ec_public.pem -signature ec_signature.bin message.txt
```

**对比签名大小**

```bash
# RSA 签名大小
openssl dgst -sha256 -sign sign_private.pem -out rsa_sig.bin message.txt
ls -la rsa_sig.bin ec_signature.bin
```

预期输出：

```console
-rw-r--r-- 1 user user 256 rsa_sig.bin
-rw-r--r-- 1 user user  71 ec_signature.bin
```

RSA 签名固定 256 字节，ECDSA 签名约 70-72 字节（DER 编码）。

### 实验3：Python 脚本实现签名

**使用配套脚本演示 RSA 签名：**

```bash
python scripts/rsa_signature.py
```

预期输出（部分）：

```console
============================================================
  RSA Digital Signature Demonstration
============================================================

[1] Generating RSA-2048 key pair...
    Public exponent (e): 65537
    Modulus (n) bit length: 2048 bits

[2] Signing message: This is a secret message for RSA signature demo.
    Message hash (SHA-256): 7a8b9c...
    Signature (256 bytes): 3f2a1b...

[3] Verifying signature...
    Verification result: VALID

[4] Tamper detection test...
    Verification result: INVALID (tampered!)

[5] Wrong key detection test...
    Verification with wrong key: INVALID (wrong key!)

[7] Performance test (1000 sign/verify operations)...
    Signing:   1000 ops in 2.341s (427 ops/s)
    Verifying: 1000 ops in 0.156s (6410 ops/s)
```

**使用配套脚本演示 ECDSA 签名：**

```bash
python scripts/ecdsa_demo.py
```

预期输出（部分）：

```console
============================================================
  ECDSA Digital Signature Demonstration
============================================================

[1] Generating ECDSA key pair (secp256r1 / P-256)...
    Curve: secp256r1
    Key size: 256 bits

[6] ECDSA vs RSA comparison:
    Metric                       RSA-2048   ECDSA P-256
    ------------------------- ------------ ------------
    Key size (bits)                  2048          256
    Signature size (bytes)            256           71
    Sign speed (ops/s)               427         1850
    Verify speed (ops/s)            6410         1420
    Security level (bits)             112          128
```

## 安全分析与思考

### 常见签名攻击

**1. 密钥泄露攻击**

如果私钥被泄露，攻击者可以伪造任何签名。保护私钥是签名安全的第一要务。

**2. 选择消息攻击**

攻击者可能构造特定消息来分析签名模式。使用随机填充（PSS）和随机化签名（ECDSA 的随机 $k$）可以防御。

**3. 签名延展性**

某些签名方案允许对同一消息生成不同的有效签名。在区块链中，这可能导致交易 ID 变化。BIP-62 和 SegWit 修复了比特币中的这个问题。

**4. 哈希碰撞攻击**

如果使用的哈希函数被攻破（如 SHA-1），签名安全性也会被破坏。务必使用 SHA-256 或更强的哈希函数。

### 签名算法选择建议

| 场景 | 推荐算法 | 原因 |
|------|----------|------|
| 通用场景 | ECDSA P-256 | 安全性高、签名小、速度快 |
| 需要确定性 | Ed25519 | 无随机数依赖，实现更安全 |
| 遗留系统兼容 | RSA-PSS | 广泛支持 |
| 长期存档 | RSA-3072+ | 保守选择 |
| 后量子迁移 | ML-DSA (Dilithium) | NIST 后量子标准 |

## 练习题

1. **概念题**：解释为什么"加密用公钥，签名用私钥"。如果反过来使用会有什么安全问题？

2. **计算题**：在 RSA 签名中，假设 $p = 61, q = 53$，$e = 17$，消息哈希值 $H = 100$。计算签名值 $S$。

3. **实验题**：修改 `rsa_signature.py` 脚本，添加以下功能：
   - 将签名保存到文件并从文件加载
   - 支持不同的哈希算法（SHA-256, SHA-384, SHA-512）
   - 测试不同密钥大小（1024, 2048, 4096）对性能的影响

4. **安全分析题**：假设攻击者获得了两个使用相同随机数 $k$ 的 ECDSA 签名 $(r, s_1)$ 和 $(r, s_2)$，对应的消息哈希为 $e_1$ 和 $e_2$。推导如何恢复私钥 $d$。

5. **研究题**：查找 Ed25519 签名算法的资料，比较它与 ECDSA 的异同。

## 延伸阅读

- [RFC 8017 - PKCS #1: RSA Cryptography Specifications](https://datatracker.ietf.org/doc/html/rfc8017)
- [FIPS 186-5 - Digital Signature Standard (DSS)](https://csrc.nist.gov/publications/detail/fips/186/5/final)
- [RFC 6979 - Deterministic Usage of DSA and ECDSA](https://datatracker.ietf.org/doc/html/rfc6979)
- [RFC 8032 - Edwards-Curve Digital Signature Algorithm (EdDSA)](https://datatracker.ietf.org/doc/html/rfc8032)
- [Crypto101 - Digital Signatures](https://www.crypto101.io/)
