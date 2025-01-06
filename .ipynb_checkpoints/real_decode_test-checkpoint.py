import json
from tqdm import tqdm
from decoder.decode import byte_decoder
from decoder.read import Raw_Reader

if __name__ == '__main__':

    path= rf"data/binary.raw"
    RR= Raw_Reader(path)
    data_list= RR.preprocessed_data
        
    results= []
    for i, d in tqdm(enumerate(data_list)):
        BD= byte_decoder(data= d)
        results.append(BD.process_byte_data())

    byte_decoder.save2json_static(results)