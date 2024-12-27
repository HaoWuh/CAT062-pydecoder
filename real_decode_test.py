import json
from tqdm import tqdm
from decode import byte_decoder

if __name__ == '__main__':

    path= rf"D:\Work\Shanghai\FloatingAI\CAT062\original_data.json"
    with open(path, "r") as file:
        data = json.load(file)
        
    results= []
    for i, data_dict in tqdm(enumerate(data)):
        data_list= [int(item, 16) for item in (data_dict['bytes_array'].replace(" ","")).strip("{}").split(",")]
        BD= byte_decoder(data= data_list)
        results.append(BD.process_byte_data())

    byte_decoder.save2json_static(results)