from decoder.decode import byte_decoder
from decoder.read import Raw_Reader
from decoder.decode_func import decode_functions
from decoder.utils import *

###
        


if __name__ == "__main__":
    bytes= '9F7D0902010136121500589233015A794A000AE4FFFACE000000000A03400C54F9DF6C2080780E7E001601018080000440'
    
    bytes = [62, 0, 49]+[int(bytes[i:i+2], 16) for i in range(0, len(bytes), 2)]



    # bytes=[0x3e, 0x00, 0xc7, 0x81, 0x01, 0x02, 0x19, 0x19, 0xef, 0xcc, 0x19, 0x19, 0x43, 0x43, 0x41, 0x31, 0x35, 0x31, 0x37, 0x00, 0x00, 0x20, 0x8e, 0x41, 0x33, 0x32, 0x31, 0x4d, 0x5a, 0x42, 0x41, 0x41, 0x5a, 0x53, 0x53, 0x53, 0x33, 0x36, 0x52, 0x02, 0x40, 0x07, 0x18, 0x00, 0x50, 0x07, 0x16, 0x00, 0x32, 0x32, 0x37, 0x20, 0x20, 0x20, 0x81, 0x01, 0x02, 0x19, 0x19, 0xef, 0xcc, 0x19, 0x19, 0x43, 0x53, 0x4e, 0x36, 0x39, 0x38, 0x31, 0x00, 0x00, 0x1d, 0x12, 0x42, 0x37, 0x33, 0x38, 0x4d, 0x5a, 0x57, 0x57, 0x57, 0x5a, 0x53, 0x53, 0x53, 0x33, 0x36, 0x52, 0x01, 0x40, 0x07, 0x35, 0x00, 0x32, 0x36, 0x36, 0x20, 0x20, 0x20, 0x81, 0x01, 0x02, 0x19, 0x19, 0xef, 0xcc, 0x19, 0x19, 0x43, 0x45, 0x53, 0x32, 0x31, 0x35, 0x39, 0x00, 0x00, 0x21, 0x7c, 0x41, 0x32, 0x30, 0x4e, 0x4d, 0x5a, 0x4c, 0x58, 0x59, 0x5a, 0x53, 0x53, 0x53, 0x33, 0x36, 0x52, 0x02, 0x40, 0x07, 0x2d, 0x00, 0x50, 0x07, 0x2b, 0x00, 0x34, 0x31, 0x32, 0x20, 0x20, 0x20, 0x81, 0x01, 0x02, 0x19, 0x19, 0xef, 0xcc, 0x19, 0x19, 0x43, 0x45, 0x53, 0x35, 0x31, 0x31, 0x34, 0x00, 0x00, 0x14, 0x3d, 0x41, 0x33, 0x33, 0x32, 0x48, 0x5a, 0x42, 0x41, 0x41, 0x5a, 0x53, 0x53, 0x53, 0x33, 0x36, 0x52, 0x01, 0x40, 0x07, 0x32, 0x00, 0x32, 0x33, 0x30, 0x20, 0x20, 0x20]


    # test process_byte_data!
    # BD= byte_decoder(data= bytes)
    # print(BD.process_byte_data())

    # test Raw_Reader!
    # RR= Raw_Reader("data/sample.raw")
    # bytes= RR.data

    # generate a ckeck.json!
    BD= byte_decoder(data= bytes)
    generate_check_json(BD.process_byte_data(), s_name= "singlecheck")
    BD.save2json()
###