import json
import pytest
from decoder.utils import *

@pytest.fixture(scope="module")
def object_file():
    return "./outputs/cat062check.json"

def test_extract_val2list(object_file):
    file= object_file
    try:
        with open(file, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
    
    assert extract_val2list is not None
    extracted_data= extract_val2list(data)
    assert extracted_data is not None
    print(extracted_data)


if __name__ == "__main__":
    test_extract_val2list()
    
    pass
    
    