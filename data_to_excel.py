# https://www.cnblogs.com/keeptg/p/10609222.html

# 创建一个空的excel文件
nan_excle = pd.DataFrame()
nan_excel.to_excel(path + filename)

# 打开excel
writer = pd.ExcelWriter(path + filename)
#sheets是要写入的excel工作簿名称列表
for sheet in sheets:
　　output.to_excel(writer, sheet_name=sheet)

# 保存writer中的数据至excel
# 如果省略该语句，则数据不会写入到上边创建的excel文件中
writer.save()
