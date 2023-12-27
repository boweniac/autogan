# 计算1到n的整数和
def calculate_sum(n):
    total = 0
    for i in range(1, n+1):
        total += i
    return total

# 反转字符串
def reverse_string(s):
    return s[::-1]

# 输入整数n
n = int(input("请输入一个整数n："))
# 计算并输出1到n的整数和
print("1到{}的整数和为：{}".format(n, calculate_sum(n)))

# 输入字符串s
s = input("请输入一个字符串s：")
# 反转字符串并输出
print("反转后的字符串为：{}".format(reverse_string(s)))