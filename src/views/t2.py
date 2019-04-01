# def hcf(x, y):
#     """该函数返回两个数的最大公约数"""
#     # 获取最小值
#     if x > y:
#         smaller = y
#     else:
#         smaller = x
#     for i in range(1, smaller + 1):
#         if ((x % i == 0) and (y % i == 0)):
#             hcf = i
#     return hcf
# # 用户输入两个数字
# num1 = int(input("输入第一个数字: "))
# num2 = int(input("输入第二个数字: "))
# print(num1, "和", num2, "的最大公约数为", hcf(num1, num2))

#
# # 定义函数
# def lcm(x, y):
#     #  获取最大的数
#     greater = x if x>y else y
#     while (True):
#         if ((greater % x == 0) and (greater % y == 0)):
#             lcm = greater
#             break
#         greater += 1
#     return lcm
#
# # 获取用户输入
# num1 = int(input("输入第一个数字: "))
# num2 = int(input("输入第二个数字: "))
# print(num1, "和", num2, "的最小公倍数为", lcm(num1, num2))
#
# import datetime
#
#
# def getYesterday():
#     today = datetime.date.today()
#     oneday = datetime.timedelta(days=1)
#     yesterday = today - oneday
#     return yesterday
# print(getYesterday())
# import json

# d1 = {'redis_data': [('1276383', {u'restriction': [], u'settlement_event': None,})]}
# str1 = json.dumps(d1)
# print(json.loads(str1))
# import json
# with open("1.log") as f:
#     fd = f.read()
#     tem = json.loads(fd)
#     print(tem)
import time
today = time.strftime("%Y%m%d %M:%H:%S", time.localtime(time.time()))
print(today)