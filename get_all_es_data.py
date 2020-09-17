from elasticsearch import Elasticsearch

ES_FULL_CONFIG = [
    {
        "host": str("127.0.0.1"),
        "port": int(8888)
    }
]

ES_CLIENT = Elasticsearch(ES_FULL_CONFIG)


def get_all_es_data(domain, cp, index, size=1000):
    body = {
        "query": {
            "match": {
                "Field": cp
            }
        }
    }

    result = []
    queryData = ES_CLIENT.search(index=index, doc_type=f"{domain}_domain_info", scroll='5m',
                                 size=size, body=body)
    hits = queryData.get("hits").get("hits")

    if hits:
        result += hits

    scroll_id = queryData["_scroll_id"]
    total = queryData["hits"]["total"]
    for i in range(int(total / size) + 1):
        res = ES_CLIENT.scroll(scroll_id=scroll_id, scroll='5m')  # scroll参数必须指定否则会报错
        result += res["hits"]["hits"]
    result = [i["_source"] for i in result]

    return result
