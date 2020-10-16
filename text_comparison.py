import difflib
import json

f = open("text1.json", "r")  # 设置文件对象
text1 = f.read()
f = open("text2.json", "r")  # 设置文件对象
text2 = f.read()

text1_lines = text1.splitlines()  # 分别以行进行分割
text2_lines = text2.splitlines()

# d = difflib.Differ()                # 创建Differ对象
# diff = d.compare(text1_lines, text2_lines)
# print('\n'.join(list(diff)))

d = difflib.HtmlDiff()
html = d.make_file(text1_lines, text2_lines)
html = html.encode()
fp = open("Text.html", "w+b")
fp.write(html)
fp.close()
print(html)
