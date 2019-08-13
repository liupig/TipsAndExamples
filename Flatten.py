result = {}
def GetFlatten(sign, keysign= ''):
    global result
    for k,v in sign.items():
        if isinstance(v, list):
            for i in range(len(v)):
                if isinstance(v[i], dict):
                    GetFlatten(v[i], keysign= keysign+ '.'+ k+'.'+str(i))
                else:
                    if isinstance(v, list):
                        for i in range(len(v)):
                            if isinstance(v[i], dict):
                                GetFlatten(v[i], keysign= keysign + '.' + k+'.'+str(i))
                            else:
                                result[keysign+ '.' +k+'.'+str(i) if keysign else k+'.'+str(i)] = v[i]   
                    else:
                        result[(keysign+'.'+k+ '.' + str(i)) if keysign else (k+'.'+str(i)) ] = v[i]
        else:
            result[keysign+"."+k if keysign else k] = v


def flatten(sign):
    global result
    result = {}
    GetFlatten(sign)
    return result


 nested_json = {
    "a": 1,
    "b": [35, 26],
    "c": [{
            "d": [2, 3, 4],
            "e": [
                {
                    "f": 1,
                    "g": 2
                    }
                ]
        }],
    "h": {}
    }

flattened_json = flatten(nested_json)

print(flattened_json)
