import pandas as pd
import numpy as np
import random


def process_text(text, title):
    def inner_process(text, title):
        return str(title) + str(text)

    speedup = np.frompyfunc(inner_process, 2, 1)  # 2：  几个参数, 1： 几个返回值

    return speedup(text, title)


def process_fee(x):
    if not x:
        return None
    park_fee = ""
    return park_fee


df = pd.read_csv("Train_Data.csv", encoding="utf8")
df["text"] = process_text(df["text"], df["title"])
# df["pText"] = df["Fee"].apply(lambda x: x if x else None)
# df["pFee"] = df["PFee"].apply(process_fee)

df = df.where(df.notnull(), None)

result = df[["text", "negative"]]

result = result.to_dict(orient="records")
random.shuffle(result)

result_len = len(result)
head = int(result_len * 0.8)
pd.DataFrame(result[:head]).to_csv("head.csv", encoding="utf8")
pd.DataFrame(result[head:]).to_csv("tail.csv", encoding="utf8")

#
# result.head(int(result_len * 0.8)).to_csv("head.csv", encoding="utf8")
#
# result.tail(result_len - head).to_csv("tail.csv", encoding="utf8")

# 按列明第一个字母分类
import pandas as pd
df=pd.DataFrame({'name':['a40','b23','c22','c123'],'val':[100,110,120,130]})
a=df.groupby([x[0] for x in df['name']])['val'].sum()
print(a)

