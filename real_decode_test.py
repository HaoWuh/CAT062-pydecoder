import json
from tqdm import tqdm
from decoder.decode import byte_decoder
from decoder.read import Raw_Reader
from decoder.utils import generate_check_json

if __name__ == '__main__':

    path= rf"data/binary_log.raw"
    RR= Raw_Reader(path)
    data_list= RR.preprocessed_data
    
    failed_data= []
        
    results= []
    for i, d in enumerate(tqdm(data_list)):
        try:
            BD= byte_decoder(data= d)
            results.append(BD.process_byte_data())
        except:
            print("data ", i, " failed")
            print("Info:")
            print(d)
            print("len: ", len(d))
            failed_data.append(d)

    byte_decoder.save2json_static(results)
    generate_check_json(results)
    print("Saved!")
    
    print("######################")
    
    print("Failed data:")
    for i, fd in enumerate(failed_data):
        print("No. ", i)
        print("length: ", len(fd))
        print(fd)