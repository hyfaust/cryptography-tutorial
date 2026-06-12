---
title: "流密码与异或加密"
---

# 流密码与异或加密

## 学习目标

完成本节后，你将能够：

- 理解流密码与分组密码的区别
- 掌握异或运算的性质及其在加密中的应用
- 了解一次性密码本（OTP）的完美保密性及其实际限制
- 分析RC4流密码的安全问题
- 使用Python演示异或加密和密钥重用攻击
- 理解密钥重用带来的安全风险

## 前置知识

- 二进制运算基础
- 对称加密的基本概念
- [分组密码模式](03-block-modes.md)中的CTR模式概念

## 核心概念与术语

### 流密码 vs 分组密码

**分组密码**：
- 将数据分成固定大小的块（如128位）
- 每个块独立加密
- 需要填充处理不完整块
- 例子：AES、DES

**流密码**：
- 逐位或逐字节加密
- 生成密钥流与明文异或
- 不需要填充
- 例子：RC4、ChaCha20、Salsa20

**对比表**：

| 特性 | 分组密码 | 流密码 |
|------|----------|--------|
| 数据单位 | 固定块（128位） | 位或字节 |
| 填充 | 需要 | 不需要 |
| 错误传播 | 有限 | 无 |
| 并行处理 | 可能 | 通常不能 |
| 硬件实现 | 复杂 | 简单 |
| 典型应用 | 通用加密 | 实时通信 |

### 异或运算（XOR）

异或（exclusive OR，XOR）是流密码的基础运算，符号为$\oplus$。

#### 异或的真值表

| A | B | A $\oplus$ B |
|---|---|-------------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**简单记忆**：相同为0，不同为1。

#### 异或的重要性质

**1. 自反性**：
$$
A \oplus A = 0
$$

**2. 与零的恒等性**：
$$
A \oplus 0 = A
$$

**3. 交换律**：
$$
A \oplus B = B \oplus A
$$

**4. 结合律**：
$$
(A \oplus B) \oplus C = A \oplus (B \oplus C)
$$

**5. 双重异或还原**：
$$
A \oplus B \oplus B = A
$$

这个性质是流密码加密和解密的基础。

#### 异或在加密中的应用

**加密过程**：
$$
C = P \oplus K
$$

**解密过程**：
$$
P = C \oplus K
$$

其中：
- $P$ 是明文
- $C$ 是密文
- $K$ 是密钥（或密钥流）

### 一次性密码本（OTP）

一次性密码本（One-Time Pad，OTP）是最简单的流密码，由Vernam在1917年提出。

#### OTP的原理

1. 生成与明文等长的随机密钥
2. 将明文与密钥逐位异或
3. 使用后立即销毁密钥

**数学表示**：
$$
C = P \oplus K
$$
$$
P = C \oplus K
$$

#### OTP的完美保密性

OTP具有**完美保密性**（Perfect Secrecy），由Shannon在1949年证明。

**完美保密性的定义**：
$$
P(P|C) = P(P)
$$

即：知道密文不会提供关于明文的任何信息。

**证明思路**：
- 对于任何密文$C$和任何明文$P$，存在唯一密钥$K = P \oplus C$
- 所有密钥等可能，因此所有明文等可能
- 密文不泄露明文信息

#### OTP的实际限制

**1. 密钥长度问题**：
- 密钥必须和明文一样长
- 如果明文是1GB，密钥也需要1GB
- 密钥分发和存储成本极高

**2. 密钥随机性要求**：
- 密钥必须是真随机数
- 伪随机数生成器（PRNG）不够安全
- 随机性不足会降低安全性

**3. 密钥管理问题**：
- 每次加密需要新的密钥
- 密钥只能使用一次
- 密钥的安全销毁

**4. 同步问题**：
- 发送方和接收方必须保持同步
- 任何不同步都会导致解密失败

!!! info "OTP的历史应用"
    OTP在冷战时期被广泛使用：
    - 热线电话（莫斯科-华盛顿）
    - 外交通信
    - 核武器指挥控制
    
    现代应用中，OTP的密钥管理问题使其不实用，通常用流密码代替。

### RC4流密码

RC4（Rivest Cipher 4）是由Ron Rivest在1987年设计的流密码，曾广泛用于SSL/TLS和WEP。

#### RC4的工作原理

RC4包含两个阶段：

**1. 密钥调度算法（KSA）**：
```
初始化S盒：S[i] = i，i = 0, 1, ..., 255
使用密钥打乱S盒：
j = 0
for i = 0 to 255:
    j = (j + S[i] + K[i mod keylen]) mod 256
    swap(S[i], S[j])
```

**2. 伪随机数生成算法（PRGA）**：
```
i = 0, j = 0
while generating:
    i = (i + 1) mod 256
    j = (j + S[i]) mod 256
    swap(S[i], S[j])
    output S[(S[i] + S[j]) mod 256]
```

#### RC4的安全问题

**1. 初始字节偏差**：
- RC4生成的前几个字节存在统计偏差
- 攻击者可以利用这些偏差恢复密钥
- 解决方案：丢弃前256-1024字节

**2. 相关密钥攻击**：
- 某些密钥之间存在相关性
- WEP协议中的弱密钥问题

**3. 已知攻击**：
- Fluhrer-Mantin-Shamir攻击（2001）
- Klein攻击（2005）
- 针对TLS的攻击（2013）

**RC4的淘汰**：
- 2015年：RFC 7465禁止在TLS中使用RC4
- 现代应用应使用ChaCha20或AES-CTR

!!! warning "RC4安全警告"
    **永远不要使用RC4**。它已被证明不安全，应使用ChaCha20或AES-CTR代替。

### 现代流密码

#### ChaCha20

ChaCha20是Daniel J. Bernstein设计的流密码，是Salsa20的改进版本。

**特点**：
- 256位密钥
- 96位随机数（Nonce）
- 20轮运算
- 高性能（特别是在没有AES硬件加速的平台上）

**应用**：
- TLS 1.3（与Poly1305认证结合）
- SSH协议
- WireGuard VPN

#### Salsa20

Salsa20是ChaCha20的前身，安全性相当但性能略低。

### 密钥重用攻击（Two-time Pad）

当同一个密钥流被使用两次时，会发生严重的安全问题。

#### 攻击原理

假设有两个明文$P_1$和$P_2$，使用相同的密钥流$K$加密：

$$
C_1 = P_1 \oplus K
$$
$$
C_2 = P_2 \oplus K
$$

攻击者计算两个密文的异或：

$$
C_1 \oplus C_2 = (P_1 \oplus K) \oplus (P_2 \oplus K) = P_1 \oplus P_2
$$

**结果**：攻击者得到两个明文的异或，可以进一步恢复明文。

#### 实际攻击示例

**场景**：两个加密消息使用相同的密钥流

**攻击步骤**：
1. 截获两个密文$C_1$和$C_2$
2. 计算$P_1 \oplus P_2 = C_1 \oplus C_2$
3. 利用语言统计特性（如英语字母频率）猜测明文
4. 通过已知明文攻击恢复密钥流

**历史案例**：
- Venona项目：苏联在二战期间重复使用一次性密码本，美国成功破解
- WEP协议：由于IV空间太小，导致密钥重用

#### 防御措施

1. **使用唯一的Nonce/IV**：
   - 每次加密使用不同的Nonce
   - Nonce可以是计数器或随机数

2. **使用AEAD模式**：
   - GCM、ChaCha20-Poly1305等
   - 认证可以检测密钥重用

3. **密钥轮换**：
   - 定期更换加密密钥
   - 限制单个密钥的使用次数

## 动手实践

### 实验1：使用CyberChef进行XOR操作

#### XOR加密演示

1. 打开CyberChef：https://gchq.github.io/CyberChef/
2. 搜索"XOR"操作
3. 配置参数：
   - Key: `0123456789ABCDEF`
   - Key format: Hex
4. 输入明文：`Hello, XOR Encryption!`
5. 查看加密结果

#### XOR解密演示

1. 使用相同的XOR操作
2. 输入密文（十六进制格式）
3. 使用相同的密钥
4. 验证解密结果

#### XOR性质验证

1. 输入：`Hello`
2. 密钥：`0123456789`
3. 第一次XOR：得到密文
4. 第二次XOR（使用相同密钥）：恢复明文
5. 验证双重异或还原性质

### 实验2：Python脚本演示异或加密

我们将使用Python演示异或加密的各种方面。

#### 运行演示脚本

```bash
python scripts/xor_cipher.py
```

**预期输出**：

```
=== XOR Cipher Demo ===

Original text: Hello, XOR Encryption!
Key: SECRETKEY

--- Basic XOR Encryption ---
Encrypted (hex): [十六进制密文]
Encrypted (base64): [Base64密文]
Decrypted: Hello, XOR Encryption!

=== XOR Properties Demo ===

1. Self-inverse property:
   A = 0x41 (65)
   K = 0x13 (19)
   A XOR K = 0x52 (82)
   (A XOR K) XOR K = 0x41 (65) = A ✓

2. Identity property:
   A = 0x41 (65)
   A XOR 0 = 0x41 (65) = A ✓

3. Commutative property:
   A = 0x41, B = 0x13
   A XOR B = 0x52
   B XOR A = 0x52
   A XOR B = B XOR A ✓

=== One-Time Pad (OTP) Demo ===

Plaintext: ATTACK AT DAWN
Key (random): [随机密钥]
Ciphertext: [密文]
Decrypted: ATTACK AT DAWN

OTP Security Properties:
- Key length = Plaintext length (13 bytes)
- Key is truly random
- Key is used only once
- Key is destroyed after use

=== Key Reuse Attack Demo ===

Message 1: "HELLO WORLD"
Message 2: "GOODBYE NOW"

Encrypted with SAME key:
C1: [密文1]
C2: [密文2]

Attack: C1 XOR C2 = P1 XOR P2
Result: [P1 XOR P2]

Known-plaintext attack:
If we know P1 = "HELLO WORLD"
Then P2 = (P1 XOR P2) XOR P1 = "GOODBYE NOW"

=== RC4 Stream Cipher Demo ===

Key: "SecretKey"
RC4 Keystream (first 32 bytes): [密钥流字节]
Note: RC4 is BROKEN and should NOT be used!
Use ChaCha20 or AES-CTR instead.

=== Modern Stream Cipher: ChaCha20 ===

Key (32 bytes): [密钥]
Nonce (12 bytes): [随机数]
Encrypted: [密文]
Decrypted: Hello, ChaCha20 Encryption!
Note: ChaCha20 is secure and used in TLS 1.3.
```

### 实验3：密钥重用攻击演示

#### Python脚本演示

```bash
python scripts/xor_cipher.py --attack-demo
```

**攻击演示步骤**：

1. **生成两个明文消息**：
   ```python
   message1 = "The quick brown fox jumps over the lazy dog"
   message2 = "Pack my box with five dozen liquor jugs"
   ```

2. **使用相同密钥流加密**：
   ```python
   key_stream = generate_key_stream(len(message1))
   cipher1 = xor_bytes(message1.encode(), key_stream)
   cipher2 = xor_bytes(message2.encode(), key_stream)
   ```

3. **攻击者计算两个密文的异或**：
   ```python
   xor_result = xor_bytes(cipher1, cipher2)
   # 结果等于 message1 XOR message2
   ```

4. **利用语言统计恢复明文**：
   ```python
   # 英语中空格的ASCII码是0x20
   # 如果 xor_result[i] 的可打印字符是字母
   # 那么其中一个明文可能是空格
   ```

### 实验4：实际应用场景

#### 场景1：简单文件加密

```python
# 使用异或加密文件
def xor_encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # 重复密钥以匹配数据长度
    key_stream = (key * (len(data) // len(key) + 1))[:len(data)]
    
    # 异或加密
    encrypted = bytes(a ^ b for a, b in zip(data, key_stream))
    
    with open(output_file, 'wb') as f:
        f.write(encrypted)
```

#### 场景2：网络数据加密

```python
# 模拟网络数据包加密
def encrypt_packet(packet_data, session_key, packet_number):
    # 使用会话密钥和包号生成密钥流
    nonce = struct.pack('>I', packet_number)
    key_stream = generate_chacha20_key_stream(session_key, nonce)
    
    # 加密数据包
    return xor_bytes(packet_data, key_stream)
```

## 安全分析与思考

### 流密码的安全性分析

#### 1. 密钥流质量

**好的密钥流应该**：
- 统计上均匀分布
- 不可预测
- 没有明显的模式
- 周期足够长

**差的密钥流会导致**：
- 统计攻击
- 已知明文攻击
- 密钥恢复攻击

#### 2. 密钥管理

**流密码的密钥管理挑战**：
- 密钥必须保密
- Nonce必须唯一
- 密钥轮换策略

**最佳实践**：
- 使用密钥派生函数（KDF）
- 定期更换密钥
- 使用认证加密（AEAD）

#### 3. 实现安全

**常见实现错误**：
- 密钥重用
- Nonce重复
- 弱随机数生成
- 时序攻击

**防御措施**：
- 使用经过验证的库
- 常数时间实现
- 安全随机数生成器

### 现代流密码的选择

#### ChaCha20 vs AES-CTR

| 特性 | ChaCha20 | AES-CTR |
|------|----------|---------|
| 密钥长度 | 256位 | 128/192/256位 |
| Nonce长度 | 96位 | 128位 |
| 软件性能 | 优秀 | 良好 |
| 硬件加速 | 有限 | AES-NI |
| 安全性 | 高 | 高 |
| 应用场景 | 移动设备、嵌入式 | 服务器、桌面 |

**选择建议**：
- 有AES硬件加速：使用AES-CTR
- 没有AES硬件加速：使用ChaCha20
- 需要认证：使用ChaCha20-Poly1305或AES-GCM

### 流密码的未来

#### 后量子密码学

- 流密码受量子计算影响较小
- Grover算法将安全性减半
- 256位密钥提供128位后量子安全性

#### 新兴流密码

- **ChaCha20-Poly1305**：TLS 1.3标准
- **AES-GCM-SIV**：抗Nonce误用
- **XChaCha20**：扩展Nonce长度

## 练习题

### 基础题

1. **异或运算**：
   - 计算 $1010_2 \oplus 1100_2$
   - 验证 $A \oplus B \oplus B = A$ 对任意A、B成立

2. **流密码 vs 分组密码**：
   - 列出流密码和分组密码的三个主要区别
   - 各举一个实际应用例子

3. **一次性密码本**：
   - OTP的完美保密性是什么意思？
   - 为什么OTP在实际中不实用？

4. **RC4安全问题**：
   - RC4有哪些已知的安全问题？
   - 为什么RC4被淘汰？

### 进阶题

5. **密钥重用攻击**：
   - 解释密钥重用攻击的基本原理
   - 给出攻击者可以恢复明文的具体步骤

6. **密钥流生成**：
   - 好的密钥流应该具备什么特性？
   - 为什么伪随机数生成器（PRNG）不适合生成密钥流？

7. **Nonce管理**：
   - 流密码中Nonce的作用是什么？
   - Nonce重复会导致什么安全问题？

### 实践题

8. **Python编程**：
   编写Python脚本实现：
   - 简单的异或加密函数
   - 一次性密码本加密函数
   - 密钥重用攻击演示

9. **CyberChef实验**：
   使用CyberChef完成以下任务：
   - 用XOR加密一段文本
   - 验证双重异或还原性质
   - 分析密钥长度对加密强度的影响

10. **安全分析**：
    - 分析简单异或加密的弱点
    - 设计一个更安全的流密码方案
    - 比较RC4和ChaCha20的安全性

## 延伸阅读

### 官方文档

- [RFC 7539: ChaCha20 and Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC 7465: Prohibiting RC4 Cipher Suites](https://tools.ietf.org/html/rfc7465)

### 学术论文

- Shannon, C., "Communication Theory of Secrecy Systems," 1949
- Bernstein, D., "ChaCha, a variant of Salsa20," 2008
- Fluhrer, S., Mantin, I., Shamir, A., "Weaknesses in the Key Scheduling Algorithm of RC4," 2001

### 在线资源

- [流密码动画演示](https://www.youtube.com/watch?v=DLjzI5KXnS0)
- [CryptoHack流密码挑战](https://cryptohack.org/challenges/stream-ciphers/)

### 相关工具

- [CyberChef](https://gchq.github.io/CyberChef/)
- [Python cryptography库](https://cryptography.io/)
- [pycryptodome库](https://pycryptodome.readthedocs.io/)

---

**返回模块索引**：[模块3：对称加密](index.md)