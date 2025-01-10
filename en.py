# aes_encrypt.py

import os

# AES S-box
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# 轮常量
RCON = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a
]

def sub_bytes(state):
    """
    通过S-box替换状态矩阵中的每个字节
    """
    for i in range(4):
        for j in range(4):
            state[i][j] = SBOX[state[i][j]]
    return state

def shift_rows(state):
    """
    对状态矩阵进行行移位操作
    第一行不移动
    第二行循环左移1位
    第三行循环左移2位
    第四行循环左移3位
    """
    # 第二行左移1位
    state[1] = state[1][1:] + state[1][:1]
    # 第三行左移2位
    state[2] = state[2][2:] + state[2][:2]
    # 第四行左移3位
    state[3] = state[3][3:] + state[3][:3]
    return state

def xtime(a):
    """
    在GF(2^8)域上的乘法运算
    """
    if a & 0x80:
        return ((a << 1) ^ 0x1B) & 0xFF
    return a << 1

def mix_single_column(col):
    """
    对状态矩阵的单列进行列混合操作
    """
    t = col[0] ^ col[1] ^ col[2] ^ col[3]
    u = col[0]
    col[0] ^= t ^ xtime(col[0] ^ col[1])
    col[1] ^= t ^ xtime(col[1] ^ col[2])
    col[2] ^= t ^ xtime(col[2] ^ col[3])
    col[3] ^= t ^ xtime(col[3] ^ u)
    return col

def mix_columns(state):
    """
    对状态矩阵进行列混合操作
    """
    for i in range(4):
        column = [state[j][i] for j in range(4)]
        column = mix_single_column(column)
        for j in range(4):
            state[j][i] = column[j]
    return state

def add_round_key(state, round_key):
    """
    将轮密钥与状态矩阵进行异或操作
    """
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state

def key_expansion(key):
    """
    密钥扩展函数，生成轮密钥
    """
    # 初始化扩展密钥数组
    w = [[0] * 4 for _ in range(44)]
    
    # 复制初始密钥到w的前4个字
    for i in range(4):
        w[i] = [key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]]
    
    # 生成剩余的字
    for i in range(4, 44):
        temp = w[i-1][:]
        
        if i % 4 == 0:
            # 循环左移
            temp = temp[1:] + temp[:1]
            # S-box替换
            temp = [SBOX[b] for b in temp]
            # 与轮常量异或
            temp[0] ^= RCON[i//4]
        
        for j in range(4):
            w[i][j] = w[i-4][j] ^ temp[j]
            
    return w

def create_state_matrix(block):
    """
    将16字节的数据块转换为4x4状态矩阵
    """
    return [[block[i + 4*j] for j in range(4)] for i in range(4)]

def state_matrix_to_bytes(state):
    """
    将状态矩阵转换回字节序列
    """
    return bytes(state[i][j] for j in range(4) for i in range(4))

def pad_data(data):
    """
    使用PKCS7填充方案对数据进行填充
    """
    pad_length = 16 - (len(data) % 16)
    padding = bytes([pad_length] * pad_length)
    return data + padding

def encrypt_block(block, expanded_key):
    """
    加密单个16字节数据块
    """
    state = create_state_matrix(block)
    
    # 初始轮密钥加
    state = add_round_key(state, [expanded_key[i] for i in range(4)])
    
    # 9个标准轮
    for round in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, [expanded_key[4*round + i] for i in range(4)])
    
    # 最后一轮（无列混合）
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, [expanded_key[40 + i] for i in range(4)])
    
    return state_matrix_to_bytes(state)

def generate_key():
    """
    生成一个随机的16字节（128位）密钥
    """
    return os.urandom(16)

def encrypt_file(input_path, output_path, key=None):
    """
    加密文件的主函数
    如果未提供密钥，则生成一个新的随机密钥并保存
    """
    # 如果没有提供密钥，生成新密钥
    if key is None:
        key = generate_key()
        # 保存密钥到文件
        with open(input_path + '.key', 'wb') as f:
            f.write(key)
        print(f"密钥已保存到: {input_path}.key")
    
    # 扩展密钥
    expanded_key = key_expansion(list(key))
    
    # 读取输入文件
    with open(input_path, 'rb') as f:
        data = f.read()
    
    # 填充数据
    padded_data = pad_data(data)
    
    # 加密
    encrypted_data = bytearray()
    for i in range(0, len(padded_data), 16):
        block = padded_data[i:i+16]
        encrypted_block = encrypt_block(block, expanded_key)
        encrypted_data.extend(encrypted_block)
    
    # 写入加密后的数据
    with open(output_path, 'wb') as f:
        f.write(encrypted_data)
    
    print(f"文件已加密并保存到: {output_path}")

if __name__ == "__main__":
    # 使用示例
    input_file = "原文.txt"
    output_file = "加密后.txt"
    
    # 不提供密钥，程序会自动生成并保存密钥
    encrypt_file(input_file, output_file)
    
    # 或者提供自己的密钥
    # with open('my_key.txt', 'rb') as f:
    #     key = f.read(16)
    # encrypt_file(input_file, output_file, key)