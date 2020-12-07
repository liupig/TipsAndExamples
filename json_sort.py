def json_sort(input_data):
    def dict_sort_by_key(data):
        data = sorted(data.items(), key=lambda item: item[0])
        return {i[0]: i[1] for i in data}

    if isinstance(input_data, dict):
        input_data = dict_sort_by_key(input_data)
        for k in input_data:
            if isinstance(input_data[k], dict):
                input_data[k] = dict_sort_by_key(input_data[k])
                input_data[k] = json_sort(input_data[k])
            if isinstance(input_data[k], list):
                input_data[k] = json_sort(input_data[k])

    if isinstance(input_data, list):
        for i in range(len(input_data)):
            input_data[i] = json_sort(input_data[i])

    return input_data
    
#  功能介绍: 处理json数据对比中字段顺序不一致的问题。
#  json数据通过此处理再配合Beyond Compare 4 做数据对比，可降低大量的人工成本和时间。

#或者直接使用web：http://cc-z.com:9099/textc
#或者直接部署https://github.com/yang521/bing_etl_server
