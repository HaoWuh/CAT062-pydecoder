import pytest
from decoder.decode import *
from decoder.read import Raw_Reader



@pytest.fixture(scope="module")
def reader():
    raw_file= "./data/sample.raw"
    try:
        RR= Raw_Reader(raw_file, preprocess= True)
        return RR
    except:
        raise Exception("Error reading raw file")
    


def test_decode(reader):
    
    assert reader is not None
    data= reader.preprocessed_data[0]

    assert data is not None
    
    assert byte_decoder is not None

    BB= byte_decoder(data)
    assert BB is not None

    result= BB.process_byte_data()

    assert result is not None

    # for checking
    print(result)
