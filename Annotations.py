# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 15:24:55 2019

@author: Sissss
"""

txt = '我们想去北京'
sign = '北京'
def GetResult(txt, sign):
    if not txt or not sign:
        return []
    result = []
    signlen = len(sign)
    txtlen = len(txt)
    suffixNum = 0
    for i in range(txtlen):
        if suffixNum:
            suffixNum -= 1
            result.append('%s AAAA' % txt[i])
            continue
        if i<= (txtlen - signlen):
            if txt[i: i+signlen] == sign:
                suffixNum = signlen - 1
                result.append('%s BBBB' % txt[i])
                continue
        result.append('%s CCCC' % txt[i])
    return result
r = GetResult(txt, sign)
for i in r:
    print(i)

#我 CCCC
#们 CCCC
#想 CCCC
#去 CCCC
#北 BBBB
#京 AAAA
