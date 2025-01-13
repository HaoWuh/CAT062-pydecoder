from decoder.decode import byte_decoder
from decoder.decode_func import decode_functions


def generate_check_json(result, s_name= "check"):
    if isinstance(result, dict):
        check_list= make_check_list(result)
                
    elif isinstance(result, list):
        check_list=[]
        for res in result:
            check_list.append(make_check_list(res))
    
    else:
        return
            
    byte_decoder.save2json_static(check_list, save_name= s_name)
    print("check saved!")


def get_val(item):
    if isinstance(item, list):
        for it in item:
            it= get_val(it)
        return item
    
    elif isinstance(item, dict):
        ks= [k for k in item.keys()]
        if "val" in ks:
            tmp_dict= dict()
            tmp_dict["val"]= item["val"]
            
            return tmp_dict
        else:
            for k in ks:
                item[k]= get_val(item[k])
            return item

    elif isinstance(item, int) or isinstance(item, float):
        return {"val": item}
    
    elif isinstance(item, str):
        return {"val": item}
    else:
        return item 
    

def make_check_list(result):
    check_list= []
    result= decode_functions.clean_str2val(result)
    result= get_val(result)
    for key in result.keys():
        if 'block' in key:
            block_dict= dict()
            for key1 in result[key].keys():
                if 'I062' in key1:
                    block_dict[key1[:8]]= dict()
                    for key2, item in result[key][key1].items():
                        # block_dict[key1[:8]][key2]= get_val(item)
                        block_dict[key1[:8]][key2]= item


            check_list.append(block_dict)
                
    return check_list
   
    
    
def extract_val2list(result):
    final_list= []
    if isinstance(result, list):
        for res in result:
            r_list= extract_val2list(res)
            for r in r_list:
                final_list.append(r)
                    
    elif isinstance(result, dict):
        ks= [k for k in result.keys()]
        
        if "val" in ks:   
            if "desc" in ks:
                if "Spare" in result["desc"] or "spare" in result["desc"]:
                    return []
            else:
                pass
            return [result["val"]]
        else:
            for k in ks:
                if "FX" in k or "REP" in k:
                    continue
                r_list= extract_val2list(result[k])
                for r in r_list:
                    final_list.append(r)
                    
    else:
        pass
    
    return final_list
            