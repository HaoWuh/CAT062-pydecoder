import json
import pytest
from decoder.utils import *


@pytest.fixture(scope="module")
def original_file():
    return "./outputs/cat062.json"



@pytest.fixture(scope="module")
def object_file():
    return "./outputs/cat062check.json"




def test_make_check_list(original_file):
    file= original_file
    try:
        with open(file, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        
    assert make_check_list is not None
    checked_list= make_check_list(data)
    assert checked_list is not None
    # use pytest -s to check
    print(checked_list)




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
    # use pytest -s to check
    print(extracted_data)

    
    