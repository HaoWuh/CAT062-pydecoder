import os
import pytest
from decoder.read import *



@pytest.fixture(scope="module")
def raw_file():
    return "./data/sample.raw"


bytes= '9F7D0902010136121500589233015A794A000AE4FFFACE000000000A03400C54F9DF6C2080780E7E001601018080000440'
bytes = [62, 0, 49]+[int(bytes[i:i+2], 16) for i in range(0, len(bytes), 2)]
@pytest.mark.parametrize(
    "byte_data",
    [
        (bytes,),
    ],
)



def test_raw_reader(raw_file, byte_data):
    assert Raw_Reader is not None
    assert os.path.exists(raw_file)

    RR= Raw_Reader(raw_file, preprocess= True)
    assert RR is not None
    # for check
    print(RR.data)
    print(RR.preprocessed_data)

    RR.import_data(byte_data, preprocess= True)
    assert RR is not None
    # for check
    print(RR.data)
    print(RR.preprocessed_data)