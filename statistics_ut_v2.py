import inspect
import re
import json
import os

script_path = "root/script/"


def get_files_info(path):
    for root, dirs, files in os.walk(path):
        return root, dirs, files


def get_test_cases(object):
    testCaseName = []
    try:
        sourceLines = inspect.getsourcelines(object)
    except:
        return testCaseName

    if sourceLines:
        names = sourceLines[0]
        funName = [name for name in names if name.strip(" ").replace("\t", "").startswith("def")]
        object_info = dir(object)

        testCaseName = [info for info in object_info if any(True for name in funName if info in name)]

    return testCaseName


def IsValidTestCase(cls, fun):
    _fun = getattr(cls, fun, None)
    if _fun:
        try:
            sourceLines = inspect.getsourcelines(_fun)
        except:
            return False
        if sourceLines:
            for line in sourceLines[0]:
                if line.strip(" ").startswith("def"):
                    continue
                elif line.strip(" ").startswith("#"):
                    continue
                elif line.strip(" ").startswith("print"):
                    continue
                elif line.replace('\n', '').replace('\r', '').replace(' ', '') in ["", "pass"]:
                    continue
                return True
    return False


def check_module_unit_test(module):
    # print(inspect.getsourcelines(module))

    unitTest = getattr(module, 'UnitTest', None)

    if unitTest:
        test_cases = get_test_cases(unitTest)
        for caseName in test_cases:
            if IsValidTestCase(unitTest, caseName):
                return True

        return False

    unitText = getattr(module, 'UnitText', None)

    if unitText:
        test_cases = get_test_cases(unitText)
        for caseName in test_cases:
            if IsValidTestCase(unitText, caseName):
                return True

        return False

    return "not UnitTest Class"


def import_module(moduleName):
    try:
        moduleName = moduleName[:-3] if moduleName.endswith(".py") else moduleName
        module = __import__(moduleName, fromlist=True)
        return module
    except:
        return None


def run():
    root, dirs, files = get_files_info(script_path)
    test_unit_failed = {"not UnitTest Class": list(),
                        "test unit failed": list(),
                        "import error": list()}
    for moduleName in files:
        moduleName = moduleName[:-3] if moduleName.endswith(".py") else moduleName
        module = import_module(moduleName)
        if module:
            check_result = check_module_unit_test(module)
            if check_result == "not UnitTest Class":
                test_unit_failed["not UnitTest Class"].append(moduleName)
            if not check_result:
                test_unit_failed["test unit failed"].append(moduleName)
        else:
            test_unit_failed["import error"].append(moduleName)
    print(json.dumps(test_unit_failed, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    run()
