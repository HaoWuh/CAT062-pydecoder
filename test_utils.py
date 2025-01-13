import json
from decoder.utils import *


def test_extract_val2list():
    file= "./outputs/cat062check.json"
    try:
        with open(file, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
    
    extracted_data= extract_val2list(data)
    print(extracted_data)


if __name__ == "__main__":
    test_extract_val2list()
    
    pass
    
    