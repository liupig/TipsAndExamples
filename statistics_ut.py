import json
import os
import re

script_path = "root/script/"


def get_files_info(path):
    for root, dirs, files in os.walk(path):
        return root, dirs, files


def GetTestCaseText(text):
    class_info = re.findall("^(?!#)(\s*)?class .*?[(]unittest.TestCase[)]", text) or []
    testCaseText = []
    if class_info:
        spacesNum = len(class_info[0].split("\n")[-1].split(" ")) - 1
        flag = False
        for line in text.split("\n"):
            if line.strip().startswith("#") or line.strip().startswith("__VNEXT__ = True") or line.strip().startswith("execfile") or line.strip().startswith("import"):
                continue
            lineSpacesNum = len(re.findall("(^\s*)?", line)[0])
            if not flag and line.replace(" ", "") and lineSpacesNum == spacesNum:
                flag = True
            elif flag and line.replace(" ", "") and lineSpacesNum <= spacesNum:
                break
            if flag:
                testCaseText.append(line)

    return "\n".join(testCaseText)


def checkTestCase(testCaseClassText):
    begin = False
    num = 0
    for text in testCaseClassText.split("\n"):
        text = text.replace("\n", "").strip()
        if begin:
            if text and (not text.startswith("#") and not text.startswith("pass") and not text.startswith(
                    "print") and not text.startswith("def")):
                num += 1
        else:
            if text.startswith("def"):
                begin = True

    return num


def run():
    root, dirs, files = get_files_info(script_path)
    check_result = dict()
    for moduleName in files:
        with open(root + moduleName, 'r') as f:
            module_text = f.read()
            result_list = re.findall("#?\s*?class .*?[(]unittest.TestCase[)]", module_text) or []
            for item in result_list:
                r1 = re.findall(item.replace("(", "\(").replace(")", "\)") + ".*(?:.|\n)", module_text, re.DOTALL) or []
                if r1:
                    testCaseClassText = GetTestCaseText(r1[0])
                    if testCaseClassText:
                        result = checkTestCase(testCaseClassText)
                        check_result[moduleName] = str(result)

    print(json.dumps(check_result, indent=4, sort_keys=True))


if __name__ == "__main__":
    run()
