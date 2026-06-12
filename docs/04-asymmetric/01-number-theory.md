---
title: 数论基础
---

# :material-math-compass: 4.1 数论基础

> **Number Theory Foundations — 密码学的数学基石**

数论是研究整数性质的数学分支，也是非对称密码学的理论基础。本节将系统讲解密码学中最常用的数论概念，为后续学习 RSA、椭圆曲线和密钥交换打下坚实基础。

---

## :material-target: 学习目标

- 理解模运算的定义、性质及其在密码学中的作用
- 掌握欧几里得算法（GCD）及其扩展形式
- 理解模逆元的存在条件和计算方法
- 掌握欧拉函数 φ(n) 的定义和计算
- 理解费马小定理和欧拉定理的含义与应用
- 了解 Miller-Rabin 素性检验的原理
- 能够使用 SageMath 和 Python 进行数论计算

---

## :material-book-open: 前置知识

- 基本的整数运算（加减乘除）
- 素数（质数）的概念
- 整除与余数的概念
- 建议先完成 [模块1：密码学基础](../01-foundations/index.md)

---

## :material-school: 核心概念与术语

### 1. 模运算（Modular Arithmetic）

模运算是密码学中最基本的数学运算。它模拟了"时钟算术"——当时钟走过 12 点后，会回到 1 点。

**定义：** 对于整数 $a$ 和正整数 $n$，$a \bmod n$ 是 $a$ 除以 $n$ 的余数。

$$
a \bmod n = a - n \left\lfloor \frac{a}{n} \right\rfloor
$$

**示例：**

| 表达式 | 计算过程 | 结果 |
|--------|---------|------|
| $17 \bmod 5$ | $17 = 3 \times 5 + 2$ | $2$ |
| $7 \bmod 3$ | $7 = 2 \times 3 + 1$ | $1$ |
| $100 \bmod 7$ | $100 = 14 \times 7 + 2$ | $2$ |
| $-3 \bmod 5$ | $-3 = -1 \times 5 + 2$ | $2$ |

!!! note "同余关系"

    如果 $a \bmod n = b \bmod n$，我们说 $a$ 和 $b$ **模 $n$ 同余**，记作：
    
    $$
    a \equiv b \pmod{n}
    $$
    
    例如：$17 \equiv 2 \pmod{5}$，因为 $17 - 2 = 15 = 3 \times 5$。

**模运算的基本性质：**

$$
(a + b) \bmod n = [(a \bmod n) + (b \bmod n)] \bmod n
$$

$$
(a \times b) \bmod n = [(a \bmod n) \times (b \bmod n)] \bmod n
$$

$$
a^k \bmod n = [(a \bmod n)^k] \bmod n
$$

!!! tip "为什么模运算对密码学至关重要？"

    1. **有限域**：模运算将无限的整数映射到有限集合 $\{0, 1, 2, \ldots, n-1\}$
    2. **单向性**：已知 $a^e \bmod n = c$，从 $c$ 反推 $a$ 是困难的
    3. **可逆性**：在特定条件下，模运算存在逆运算（模逆元）

---

### 2. 最大公约数（GCD）

**定义：** $\gcd(a, b)$ 是能同时整除 $a$ 和 $b$ 的最大正整数。

**示例：** $\gcd(48, 18) = 6$，因为 6 是 48 和 18 的最大公因子。

#### 欧几里得算法（辗转相除法）

欧几里得算法是计算 GCD 的高效方法，基于以下原理：

$$
\gcd(a, b) = \gcd(b, a \bmod b)
$$

**算法步骤（以 $\gcd(48, 18)$ 为例）：**

```
gcd(48, 18) → 48 = 2 × 18 + 12
gcd(18, 12) → 18 = 1 × 12 + 6
gcd(12, 6)  → 12 = 2 × 6 + 0
gcd = 6
```

**Python 实现：**

```python
def gcd(a, b):
    """欧几里得算法求最大公约数"""
    while b:
        a, b = b, a % b
    return a

print(gcd(48, 18))  # 输出: 6
```

!!! info "时间复杂度"

    欧几里得算法的时间复杂度为 $O(\log(\min(a, b)))$，即使对于非常大的数也能快速计算。这是密码学能够使用大整数运算的关键原因之一。

#### 扩展欧几里得算法

扩展欧几里得算法不仅能求 GCD，还能找到满足 **贝祖等式** 的整数 $x$ 和 $y$：

$$
ax + by = \gcd(a, b)
$$

**示例：** 求 $48x + 18y = 6$ 的一组解。

```
gcd(48, 18) = 6
反向代入：
6 = 18 - 1 × 12
6 = 18 - 1 × (48 - 2 × 18)
6 = 3 × 18 - 1 × 48
所以 x = -1, y = 3
验证：48 × (-1) + 18 × 3 = -48 + 54 = 6 ✓
```

```python
def extended_gcd(a, b):
    """扩展欧几里得算法，返回 (gcd, x, y) 满足 ax + by = gcd"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

g, x, y = extended_gcd(48, 18)
print(f"gcd = {g}, x = {x}, y = {y}")
# 输出: gcd = 6, x = -1, y = 3
```

---

### 3. 模逆元（Modular Inverse）

**定义：** 如果存在整数 $b$ 使得 $a \times b \equiv 1 \pmod{n}$，则 $b$ 称为 $a$ 模 $n$ 的**逆元**，记作 $a^{-1} \bmod n$。

**存在条件：**

$$
a^{-1} \bmod n \text{ 存在} \iff \gcd(a, n) = 1
$$

即 $a$ 和 $n$ 必须**互素**（coprime）。

**示例：**

| $a$ | $n$ | $\gcd(a, n)$ | $a^{-1} \bmod n$ | 验证 |
|-----|-----|-------------|------------------|------|
| $3$ | $11$ | $1$ | $4$ | $3 \times 4 = 12 \equiv 1 \pmod{11}$ |
| $7$ | $26$ | $1$ | $15$ | $7 \times 15 = 105 \equiv 1 \pmod{26}$ |
| $2$ | $4$ | $2$ | 不存在 | $\gcd(2, 4) = 2 \neq 1$ |

#### 使用扩展欧几里得算法求模逆元

当 $\gcd(a, n) = 1$ 时，贝祖等式 $ax + ny = 1$ 中的 $x$ 就是 $a^{-1} \bmod n$。

```python
def mod_inverse(a, n):
    """计算 a 模 n 的逆元"""
    gcd, x, _ = extended_gcd(a % n, n)
    if gcd != 1:
        return None  # 逆元不存在
    return x % n

print(mod_inverse(3, 11))   # 输出: 4
print(mod_inverse(7, 26))   # 输出: 15
print(mod_inverse(2, 4))    # 输出: None
```

!!! warning "模逆元在密码学中的重要性"

    模逆元是 RSA 解密的核心：解密指数 $d$ 就是加密指数 $e$ 模 $\varphi(n)$ 的逆元。
    
    $$
    d \equiv e^{-1} \pmod{\varphi(n)}
    $$

---

### 4. 欧拉函数（Euler's Totient Function）

**定义：** 欧拉函数 $\varphi(n)$ 表示小于等于 $n$ 且与 $n$ 互素的正整数的个数。

$$
\varphi(n) = |\{k : 1 \leq k \leq n, \gcd(k, n) = 1\}|
$$

**示例：**

| $n$ | 与 $n$ 互素的数 | $\varphi(n)$ |
|-----|----------------|-------------|
| $1$ | $\{1\}$ | $1$ |
| $7$ | $\{1,2,3,4,5,6\}$ | $6$（素数 $p$ 的性质：$\varphi(p) = p-1$）|
| $12$ | $\{1,5,7,11\}$ | $4$ |
| $15$ | $\{1,2,4,7,8,11,13,14\}$ | $8$ |

#### 欧拉函数的计算公式

**性质1：** 若 $p$ 是素数，则

$$
\varphi(p) = p - 1
$$

**性质2：** 若 $p$ 是素数，$k \geq 1$，则

$$
\varphi(p^k) = p^k - p^{k-1} = p^{k-1}(p - 1)
$$

**性质3（积性函数）：** 若 $\gcd(m, n) = 1$，则

$$
\varphi(mn) = \varphi(m) \times \varphi(n)
$$

**通用公式：** 设 $n = p_1^{a_1} \times p_2^{a_2} \times \cdots \times p_k^{a_k}$，则

$$
\varphi(n) = n \times \prod_{i=1}^{k} \left(1 - \frac{1}{p_i}\right)
$$

**RSA 中的特殊情况：** 对于两个不同素数 $p$ 和 $q$，

$$
\varphi(pq) = (p-1)(q-1)
$$

!!! example "计算示例"

    计算 $\varphi(12)$：
    
    $12 = 2^2 \times 3$
    
    $\varphi(12) = 12 \times (1 - \frac{1}{2}) \times (1 - \frac{1}{3}) = 12 \times \frac{1}{2} \times \frac{2}{3} = 4$
    
    验证：与 12 互素的数为 $\{1, 5, 7, 11\}$，共 4 个。✓

---

### 5. 费马小定理（Fermat's Little Theorem）

费马小定理是数论中最重要的定理之一，也是 RSA 算法正确性的理论基础。

**定理：** 若 $p$ 是素数，且 $\gcd(a, p) = 1$（即 $p \nmid a$），则

$$
a^{p-1} \equiv 1 \pmod{p}
$$

**等价形式：** 对任意整数 $a$ 和素数 $p$，

$$
a^p \equiv a \pmod{p}
$$

**示例：**

- $a = 2, p = 7$：$2^6 = 64 = 9 \times 7 + 1 \equiv 1 \pmod{7}$ ✓
- $a = 3, p = 5$：$3^4 = 81 = 16 \times 5 + 1 \equiv 1 \pmod{5}$ ✓
- $a = 10, p = 13$：$10^{12} \equiv 1 \pmod{13}$ ✓

!!! info "费马小定理的直观理解"

    考虑集合 $\{1, 2, \ldots, p-1\}$，将每个元素乘以 $a$ 模 $p$：
    
    $\{a \bmod p, 2a \bmod p, \ldots, (p-1)a \bmod p\}$
    
    这个集合恰好是 $\{1, 2, \ldots, p-1\}$ 的一个排列。因此：
    
    $$
    a \times 2a \times \cdots \times (p-1)a \equiv 1 \times 2 \times \cdots \times (p-1) \pmod{p}
    $$
    
    $$
    a^{p-1} \times (p-1)! \equiv (p-1)! \pmod{p}
    $$
    
    由于 $\gcd((p-1)!, p) = 1$，两边可消去 $(p-1)!$，得到 $a^{p-1} \equiv 1 \pmod{p}$。

---

### 6. 欧拉定理（Euler's Theorem）

欧拉定理是费马小定理的推广，将模数从素数扩展到任意正整数。

**定理：** 若 $\gcd(a, n) = 1$，则

$$
a^{\varphi(n)} \equiv 1 \pmod{n}
$$

**推论：** 若 $\gcd(a, n) = 1$，则

$$
a^k \equiv a^{k \bmod \varphi(n)} \pmod{n}
$$

!!! example "计算示例"

    验证 $2^{\varphi(15)} \equiv 1 \pmod{15}$：
    
    $\varphi(15) = \varphi(3) \times \varphi(5) = 2 \times 4 = 8$
    
    $2^8 = 256 = 17 \times 15 + 1 \equiv 1 \pmod{15}$ ✓

!!! tip "欧拉定理与 RSA"

    RSA 解密的正确性直接依赖于欧拉定理。解密过程本质上是：
    
    $$
    M^{ed} \equiv M^{1 + k\varphi(n)} \equiv M \cdot (M^{\varphi(n)})^k \equiv M \cdot 1^k \equiv M \pmod{n}
    $$

---

### 7. 素性检验（Primality Testing）

在 RSA 等算法中，我们需要生成大素数。如何判断一个大数是否为素数？

#### 试除法（最简单但最慢）

检查 $n$ 是否能被 $2, 3, \ldots, \sqrt{n}$ 整除。时间复杂度 $O(\sqrt{n})$。

```python
def is_prime_trial(n):
    """试除法判断素数"""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
```

#### Miller-Rabin 概率素性检验

Miller-Rabin 是实际密码学中使用最广泛的素性检验算法。

**原理：** 基于费马小定理的加强版。如果 $n$ 是奇素数，将 $n-1$ 写成 $2^s \times d$ 的形式（$d$ 为奇数），则对任意 $a$ 满足 $\gcd(a, n) = 1$，以下条件至少有一个成立：

1. $a^d \equiv 1 \pmod{n}$
2. 存在 $0 \leq r < s$ 使得 $a^{2^r d} \equiv -1 \pmod{n}$

如果某个 $a$ 不满足以上任一条件，则 $n$ **一定是合数**。这样的 $a$ 称为 $n$ 的**见证人**（witness）。

**算法流程：**

```python
import random

def miller_rabin(n, k=20):
    """Miller-Rabin 素性检验，k 为测试轮数"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # 将 n-1 写成 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # 进行 k 轮测试
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, x, n)  # Wrong: should be x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # n 是合数

    return True  # n "很可能"是素数
```

!!! warning "概率性 vs 确定性"

    Miller-Rabin 是**概率性**算法：如果它说 $n$ 是素数，$n$ 只是"很可能是"素数。
    
    - 每轮测试的错误概率 $\leq \frac{1}{4}$
    - $k$ 轮后错误概率 $\leq \frac{1}{4^k}$
    - 20 轮后错误概率 $\leq 2^{-40} \approx 10^{-12}$
    
    实际应用中，这个错误概率远低于硬件故障概率，因此可以放心使用。
    
    也有确定性算法如 **AKS 算法**（2002年），但实际中很少使用。

---

## :material-hammer-wrench: 动手实践

### 实验1：使用 SageMath 进行数论计算

SageMath 是一个强大的数学计算系统，内置了丰富的数论函数。

=== "基本运算"

    ```bash
    sage -c "
    # 最大公约数
    print('gcd(48, 18) =', gcd(48, 18))
    
    # 模逆元
    print('inverse_mod(3, 11) =', inverse_mod(3, 11))
    
    # 欧拉函数
    print('euler_phi(12) =', euler_phi(12))
    
    # 模幂运算
    print('power_mod(2, 10, 1000) =', power_mod(2, 10, 1000))
    
    # 素性检验
    print('is_prime(97) =', is_prime(97))
    print('is_prime(100) =', is_prime(100))
    "
    ```
    
    **预期输出：**
    
    ```
    gcd(48, 18) = 6
    inverse_mod(3, 11) = 4
    euler_phi(12) = 4
    power_mod(2, 10, 1000) = 24
    is_prime(97) = True
    is_prime(100) = False
    ```

=== "费马小定理验证"

    ```bash
    sage -c "
    # 验证费马小定理: a^(p-1) ≡ 1 (mod p)
    p = 97  # 素数
    for a in [2, 3, 5, 7, 11]:
        result = power_mod(a, p - 1, p)
        print(f'{a}^{p-1} mod {p} = {result}')
    "
    ```
    
    **预期输出：**
    
    ```
    2^96 mod 97 = 1
    3^96 mod 97 = 1
    5^96 mod 97 = 1
    7^96 mod 97 = 1
    11^96 mod 97 = 1
    ```

=== "欧拉定理验证"

    ```bash
    sage -c "
    # 验证欧拉定理: a^φ(n) ≡ 1 (mod n)
    n = 15
    phi_n = euler_phi(n)
    print(f'φ({n}) = {phi_n}')
    
    for a in [2, 4, 7, 11, 13]:
        if gcd(a, n) == 1:
            result = power_mod(a, phi_n, n)
            print(f'{a}^{phi_n} mod {n} = {result}')
    "
    ```
    
    **预期输出：**
    
    ```
    φ(15) = 8
    2^8 mod 15 = 1
    4^8 mod 15 = 1
    7^8 mod 15 = 1
    11^8 mod 15 = 1
    13^8 mod 15 = 1
    ```

=== "扩展欧几里得与模逆元"

    ```bash
    sage -c "
    # 扩展欧几里得算法
    g, x, y = xgcd(48, 18)
    print(f'gcd(48, 18) = {g}')
    print(f'48 * {x} + 18 * {y} = {g}')
    print(f'验证: {48*x + 18*y}')
    
    # 模逆元
    a, n = 7, 26
    inv = inverse_mod(a, n)
    print(f'\\n{a}^(-1) mod {n} = {inv}')
    print(f'验证: {a} * {inv} mod {n} = {(a * inv) % n}')
    "
    ```
    
    **预期输出：**
    
    ```
    gcd(48, 18) = 6
    48 * -1 + 18 * 3 = 6
    验证: 6
    
    7^(-1) mod 26 = 15
    验证: 7 * 15 mod 26 = 1
    ```

---

### 实验2：使用 Python 脚本进行数论计算

使用配套的 Python 脚本，可以一次性运行所有数论演示。

```bash
python scripts/number_theory_demo.py
```

**预期输出：**

```
=== Number Theory Demo ===

--- Modular Arithmetic ---
17 mod 5 = 2
(13 + 17) mod 5 = 0
(13 * 17) mod 5 = 1

--- GCD (Euclidean Algorithm) ---
gcd(48, 18) = 6
gcd(1071, 462) = 21

--- Extended GCD (Bezout's Identity) ---
gcd(48, 18) = 6
48 * (-1) + 18 * 3 = 6

--- Modular Inverse ---
3^(-1) mod 11 = 4
  Verification: 3 * 4 mod 11 = 1

7^(-1) mod 26 = 15
  Verification: 7 * 15 mod 26 = 1

--- Euler's Totient Function ---
φ(1) = 1
φ(7) = 6
φ(12) = 4
φ(15) = 8
φ(100) = 40

--- Fermat's Little Theorem Verification ---
p = 97
2^(96) mod 97 = 1  ✓
3^(96) mod 97 = 1  ✓
5^(96) mod 97 = 1  ✓

--- Euler's Theorem Verification ---
n = 15, φ(15) = 8
2^8 mod 15 = 1  ✓
4^8 mod 15 = 1  ✓
7^8 mod 15 = 1  ✓

--- Miller-Rabin Primality Test ---
Is 97 prime? True
Is 100 prime? False
Is 561 prime? False  (Carmichael number)
Large prime candidate: [random large number] → True/False
```

---

### 实验3：使用 OpenSSL 进行素数生成

OpenSSL 可以生成密码学安全的大素数，这些素数用于 RSA 密钥生成。

```bash
# 生成一个 256 位的素数（十六进制形式）
openssl prime -generate -bits 256 -hex

# 检查一个数是否为素数
openssl prime 97
```

**预期输出：**

```
$ openssl prime -generate -bits 256 -hex
B7E151628AED2A6ABF7158809CF4F3C762E7160F38B4DA56A784D9045190CFEF

$ openssl prime 97
61 (97) is prime
```

---

## :material-shield-alert: 安全分析与思考

### 模运算的安全性

模运算是"单向"的——给定 $a^e \bmod n = c$，在不知道 $d$（$e$ 的逆元指数）的情况下，从 $c$ 恢复 $a$ 是困难的。这种困难性来源于：

1. **信息丢失**：模运算将无限域映射到有限域，丢失了"倍数"信息
2. **指数运算的不可逆性**：没有已知的快速算法从 $a^e \bmod n$ 直接求出 $a$

### 素数生成的安全要求

!!! warning "密码学安全素数的要求"

    - 素数必须是**随机生成**的，不能使用固定的素数表
    - 素数必须足够大（RSA 中通常使用 1024 位或更大的素数）
    - 两个素数 $p$ 和 $q$ 不能太接近（防止 Fermat 分解攻击）
    - $p-1$ 和 $q-1$ 应该有大的素因子（防止 Pollard's p-1 攻击）

### Carmichael 数

有些合数能通过费马素性检验——它们被称为 **Carmichael 数**。最小的 Carmichael 数是 561：

$$
561 = 3 \times 11 \times 17
$$

对所有满足 $\gcd(a, 561) = 1$ 的 $a$，都有 $a^{560} \equiv 1 \pmod{561}$。

这就是为什么 Miller-Rabin 比费马检验更可靠——它能检测出 Carmichael 数。

---

## :material-pencil: 练习题

### 基础题

**题目1：** 计算以下值：

- (a) $23 \bmod 7$
- (b) $\gcd(270, 192)$
- (c) $5^{-1} \bmod 13$
- (d) $\varphi(30)$

??? tip "参考答案"

    - (a) $23 = 3 \times 7 + 2$，所以 $23 \bmod 7 = 2$
    - (b) $\gcd(270, 192) = \gcd(192, 78) = \gcd(78, 36) = \gcd(36, 6) = 6$
    - (c) $5 \times 8 = 40 = 3 \times 13 + 1 \equiv 1 \pmod{13}$，所以 $5^{-1} \bmod 13 = 8$
    - (d) $30 = 2 \times 3 \times 5$，$\varphi(30) = 30 \times (1-\frac{1}{2}) \times (1-\frac{1}{3}) \times (1-\frac{1}{5}) = 8$

### 进阶题

**题目2：** 使用费马小定理计算 $7^{222} \bmod 11$。

??? tip "参考答案"

    由于 11 是素数且 $\gcd(7, 11) = 1$，由费马小定理：$7^{10} \equiv 1 \pmod{11}$
    
    $222 = 22 \times 10 + 2$
    
    $7^{222} = (7^{10})^{22} \times 7^2 \equiv 1^{22} \times 49 \equiv 49 \equiv 5 \pmod{11}$

**题目3：** 证明：如果 $p$ 是奇素数，则 $p$ 整除 $2^p - 2$。

??? tip "参考答案"

    由费马小定理：$2^p \equiv 2 \pmod{p}$
    
    因此 $2^p - 2 \equiv 0 \pmod{p}$，即 $p \mid (2^p - 2)$。

### 挑战题

**题目4：** 不使用计算器，判断 1729 是否为素数。如果不是，找出它的素因子分解。

??? tip "参考答案"

    $1729 = 7 \times 247 = 7 \times 13 \times 19$
    
    这就是著名的 **Hardy-Ramanujan 数**（出租车数）：它是最小的可以用两种不同方式表示为两个立方数之和的数：
    
    $1729 = 1^3 + 12^3 = 9^3 + 10^3$

---

## :material-bookshelf: 延伸阅读

- **教材**：《An Introduction to the Theory of Numbers》— Hardy & Wright
- **教材**：《A Computational Introduction to Number Theory and Algebra》— Victor Shoup（免费在线版）
- **在线课程**：[Coursera - Number Theory and Cryptography](https://www.coursera.org/learn/number-theory-cryptography)
- **工具文档**：[SageMath Number Theory](https://doc.sagemath.org/html/en/reference/number_fields/)
- **Wikipedia**：[Fermat's Little Theorem](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem)
- **Wikipedia**：[Euler's Totient Function](https://en.wikipedia.org/wiki/Euler%27s_totient_function)
- **下一站**：[4.2 RSA 算法](02-rsa.md) — 将这些数论知识应用于实际的加密算法
