import re


def findFirst(pattern, text):  # 找第一個
    return re.compile((r"{}").format(pattern)).search(text).group()


def findAll(pattern, text):  # 找全部 包含空白
    return re.findall((r"{}").format(pattern), text)


def findPrecise(pattern, text):  # 精確找全部
    DATA = {}
    for clo, pa in pattern.items():
        DATA[clo] = [i.group() for i in re.finditer(pa, text)]
    return DATA

text = "https://www.facebook.com/%E5%A4%A7%E5%90%8C3c%E7%89%B9%E8%B3%A3%E6%9C%83-%E9%AB%98%E9%9B%84%E5%8D%80-308891219757346/"
if "z" in  text:
    print("ok")

