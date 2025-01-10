# AES 文件加密解密程序 / AES File Encryption and Decryption Program

[English Version](#english-version)

## 中文说明

### 项目简介
这是一个使用 Python 实现的 AES-128 文件加密解密程序。程序完全手动实现了 AES 算法，不依赖任何第三方加密库，适合学习和研究 AES 加密算法的原理。

### 功能特点
- 实现完整的 AES-128 加密解密算法
- 支持任意大小文件的加密和解密
- 自动生成和管理密钥
- 使用 PKCS7 填充方案
- 完整的错误处理机制
- 详细的代码注释

### 文件说明
- `encrypt.py`: 加密程序
- `decrypt.py`: 解密程序
- `README.md`: 使用说明文档

### 环境要求
- Python 3.6 或更高版本
- 不需要额外的依赖包

### 安装方法
直接下载或克隆项目文件即可使用：
```bash
git clone [项目地址]
cd AES-python
```

### 使用方法

#### 加密文件
```python
# 方法1：自动生成密钥
python encrypt.py

```

#### 解密文件
```python

python decrypt.py


```

### 注意事项
1. 请务必安全保管密钥文件，密钥丢失将无法解密文件
2. 默认生成的密钥文件名为 `[输入文件名].key`
3. 加密文件的大小会略大于原文件（因为填充）
4. 请确保有足够的磁盘空间

### 开发说明
程序实现了 AES 加密的所有核心组件：
- SubBytes/InvSubBytes (字节替换)
- ShiftRows/InvShiftRows (行移位)
- MixColumns/InvMixColumns (列混合)
- AddRoundKey (轮密钥加)
- KeyExpansion (密钥扩展)

---

## English Version

### Project Overview
This is an AES-128 file encryption and decryption program implemented in Python. The program manually implements the AES algorithm without relying on any third-party encryption libraries, making it suitable for learning and studying AES encryption principles.

### Features
- Complete implementation of AES-128 encryption/decryption algorithm
- Support for files of any size
- Automatic key generation and management
- PKCS7 padding scheme
- Comprehensive error handling
- Detailed code comments

### Files
- `encrypt.py`: Encryption program
- `decrypt.py`: Decryption program
- `README.md`: Documentation

### Requirements
- Python 3.6 or higher
- No additional packages required

### Installation
Simply download or clone the project files:
```bash
git clone [project-url]
cd AES-python
```

### Usage

#### Encrypting Files
```python

python encrypt.py


```

#### Decrypting Files
```python

python decrypt.py

```

### Important Notes
1. Keep the key file secure - files cannot be decrypted without the correct key
2. Default key file name is `[input-filename].key`
3. Encrypted files will be slightly larger than original files (due to padding)
4. Ensure sufficient disk space is available

### Technical Details
The program implements all core components of AES encryption:
- SubBytes/InvSubBytes
- ShiftRows/InvShiftRows
- MixColumns/InvMixColumns
- AddRoundKey
- KeyExpansion

### License
This project is open source and available under the MIT License.
