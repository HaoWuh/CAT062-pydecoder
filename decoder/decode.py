import json
import os
import inspect
from datetime import datetime

from decoder.cat062_maps import *
from decoder.decode_func import *

class byte_decoder:

    def __init__(self, data= None, save_name= ""):
        if isinstance(data, str):
            pass
        elif isinstance(data, bytes):
            self.byte_data = list(data)
        elif isinstance(data, list):
            self.byte_data = data
        else:
            # test_data
            # self.byte_data = [62, 0, 52, 187, 125, 37, 4, 2, 3, 0, 14, 88, 79, 0, 56, 6, 229, 1, 70, 6, 65, 253, 38, 1, 183, 13, 74, 0, 13, 51, 179, 195, 126, 32, 128, 120, 12, 203, 0, 6, 1, 0, 5, 80, 0, 0, 40, 0, 42, 0, 62, 4]
            self.byte_data= [0x3E ,0x00 ,0xB7,0xBF,0xDF,0xFF,0x02,0x19,0x64,0x04,0x3C,0x5F,0xEA,0x00,0x81,0x23,0xDC,0x00,0x2B,
                                    0x0B,0xA6,0xFD,0xC9,0x17,0xFE,0xE5,0xEB,0x02,0x36,0xFD,0x55,0x00,0x00,0x05,0x5D,
                                    0xC1,0x20,0x3C,0x0A,0x55,0x4D,0x81,0x34,0xDF,0x2C,0xE0,0x20,0xF6,0x1F,0x29,0x0D,
                                    0x13,0x01,0x08,0x70,0x04,0x00,0x00,0x00,0x90,0x00,0x00,0x05,0x78,0x16,0x12,0x05,
                                    0x78,0x00,0x00,0xFF,0xE1,0x00,0x19,0x64,0x53,0x58,0x44,0x34,0x37,0x32,0x33,0x41,
                                    0xBE,0x12,0x2D,0x44,0x42,0x37,0x33,0x38,0x4D,0x45,0x44,0x44,0x4C,0x48,0x45,0x4C,
                                    0x58,0x20,0x00,0x20,0x05,0x78,0xDC,0x19,0x0D,0x5D,0x32,0xC1,0x0B,0x05,0x78,0x05,
                                    0x5D,0xA0
]
        self.result= None
        self.index_position= 0
        self.save_name= save_name


    def process_byte_data(self):
        # 1. 判断第1个字节是否为 062
        if self.byte_data[0] != 62:
            raise ValueError("第一个字节不是 062，报错！")
        cat_version= f"0x{self.byte_data[0]:02X}"
        self.index_position+= 1

        # 2. 读取第2个字节为报文起始位置
        start_position = self.byte_data[1]
        self.index_position+= 1
        
        # 3. 读取第3个字节为报文长度
        message_length = int(self.byte_data[2])
        self.index_position+= 1
        
        # 4. 读取之后字节作为 FSPEC 字段
        fspec_field= []
        fspec_field, self.index_position= self.fspec_decode(self.index_position)        
        
        # 结果以字典形式返回
        self.result = {
            "cat version:": int(cat_version, 16),
            "start_position": start_position,
            "message_length": message_length,
            # "fspec_field": fspec_field
        }


        self.index_position+= start_position

        self.final_fspec_field=dict()
        for fspec in fspec_field:
            self.final_fspec_field[fspec[0]]= fspec[1]

        for fspec in fspec_field:
            index_plus= 0
            assert self.index_position < len(self.byte_data), "Conflict: index_position >= len(byte_data)!"
            if isinstance(fspec[1], int) or isinstance(fspec[1], float):
                self.result[fspec[0]], index_plus= getattr(self, fspec[0])(self.index_position, self.index_position+int(fspec[1]))
            elif isinstance(fspec[1], str):
                self.result[fspec[0]], index_plus= getattr(self, fspec[0])(self.index_position, self.index_position+int(fspec[1][0]))
            else:
                pass
            # try:
            #     if isinstance(fspec[1], int) or isinstance(fspec[1], float):
            #         self.result[fspec[0]], index_plus= getattr(self, fspec[0])(self.index_position, self.index_position+int(fspec[1]))
            #     elif isinstance(fspec[1], str):
            #         self.result[fspec[0]], index_plus= getattr(self, fspec[0])(self.index_position, self.index_position+int(fspec[1][0]))
            #     else:
            #         pass
            # except:
            #     print("Meet errors or skip some Info! ", fspec)

            self.final_fspec_field[fspec[0]]= [f"0x{byte:02X} " for byte in self.byte_data[self.index_position: self.index_position+index_plus]]
            self.index_position+= index_plus
        
        if self.final_fspec_field:
            for key in self.final_fspec_field.keys():
                try:
                    self.result[key+":|"+ "".join(self.final_fspec_field[key])+"|"]= self.result.pop(key)
                except:
                    print(key, " not found")
                    pass
        
        # 返回解析结果
        return self.result
    
    def fspec_decode(self, position= 3):
        field= []
        count= 0
        X= False
        while position < len(self.byte_data) and not X:
            temp_byte= self.byte_data[position]
            # print(format(temp_byte, '08b'))
            for i, bit in enumerate(format(temp_byte, '08b')):
                if i == 7:
                    position+= 1
                    count+= 1
                    if bit == "1":
                        pass
                    else:
                        X= True
                    break
                        
                if bit == "1":
                    if fspec_mapping[7*count+i+1][0]:
                        field.append(fspec_mapping[7*count+i+1])
                        # print(fspec_mapping[7*count+i+1])

        return field, position
    


    
    def I062_010(self, index_start, index_end):
        """
        return SAC and SIC nmber

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out= dict()
        out["SAC"]= str(int(self.byte_data[index_start]))
        out["SIC"]= str(int(self.byte_data[index_start+1]))
        return out, index_end-index_start
    


    
    def I062_015(self, index_start, index_end):
        """
        return Service Identification

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out= dict()
        out["Service Identification"]= self.byte_data[index_start]
        return out, index_end-index_start
    


    
    def I062_070(self, index_start, index_end):
        """
        Absolute time stamping of the information provided in the track 
        message, in the form of elapsed time since last midnight, expressed 
        as UTC.

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """

        out= dict()
        # 将几个独立字节合并为一个字节
        rhs = (self.byte_data[index_start] << 16) + (self.byte_data[index_start+1] << 8) + self.byte_data[index_start+2]
        
        # 总秒数
        value0 = rhs // 128
        
        # 小时数
        value1 = value0 // 3600
        
        # 分钟数
        value2 = (value0 - value1 * 3600) // 60
        
        # 秒数
        value3 = (value0 - value1 * 3600) % 60
        
        # 毫秒数
        value4 = ((rhs % 128) * 1000) // 128
        
        # 获取当前日期
        current_date = datetime.now().strftime("%m/%d/%Y")  # 格式化当前日期
        # out['Time Stamp']= f"{current_date} {value1}:{value2}:{value3}.{value4}"
        out['Time Stemp']= str(value0)+" "+"s"
   
        return out, index_end-index_start
    

    def I062_105(self, index_start, index_end):
        """
        Calculated Position in WGS-84 Co-ordinates with a resolution of 
        180/2^25. degrees 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out= dict()
        out["WGS-84 Latitude"]= str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start:index_start+4])),2)*(180.0/2**25))+ " " + "deg"
        out["WGS-84 Longitude"]= str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start+4:index_start+8])),2)*(180.0/2**25))+ " " + "deg"
        return out, index_end-index_start
    



    def I062_100(self, index_start, index_end):
        """
        Calculated position in Cartesian co-ordinates with a resolution of 
        0.5m, in two’s complement form. 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out= dict()
        binary_str= "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        X_str= decode_functions.invert_binary_if_negative(binary_str[0:24])
        Y_str= decode_functions.invert_binary_if_negative(binary_str[24:48])
        out["X"]= str(int(X_str, 2)*0.5)+ " " + "m"
        out["Y"]= str(int(Y_str, 2)*0.5)+ " " + "m"
        return out, index_end-index_start

   

    def I062_185(self, index_start, index_end):
        """               
        Calculated track velocity expressed in Cartesian co-ordinates, 
        in two’s complement form. 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out =dict()
        out["Vx"]= str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start:index_start+2])),2)*0.25)+ " " + "m/s"
        out["Vy"]= str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start+2:index_start+4])),2)*0.25)+ " " + "m/s"
        return out, index_end-index_start
    




    def I062_210(self, index_start, index_end):
        """               
        Calculated Acceleration of the target expressed in Cartesian co
        ordinates, in two’s complement form.

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        out["Ax"]= str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start:index_start+1])),2)*0.25)+ " " + "m/s^2"
        out["Ay"]= str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start+1:index_start+2])),2)*0.25)+ " " + "m/s^2"
        return out, index_end-index_start
    



    def I062_060(self, index_start, index_end):
        """
        Mode-3/A code converted into octal representation. 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out= dict()
        first_byte= bin(self.byte_data[index_start])[2:].zfill(8)
        out["V"]= "validated" if int(first_byte[0]) == 0 else "not validated"
        out["G"]= "Default" if int(first_byte[1]) == 0 else "Garbled"
        out["Change in Mode 3/A"]= "No change" if first_byte[2] == 0 else "Mode 3/A has Changed"
        assert int(first_byte[3]) == 0, "I062_060 error: bit must be 0!"
        second_byte= bin(self.byte_data[index_start+1])[2:].zfill(8)
        combined_byte= (first_byte[4:] + second_byte).zfill(16)

        # 将二进制字符串转换为十进制整数
        decimal_value = int(str(combined_byte), 2)

        # 将十进制整数转换为八进制字符串
        octal_value = oct(decimal_value)[2:]  # 去掉 '0o' 前缀
        out["octal Mode 3/A"]= octal_value
        return out, index_end-index_start
    

    
    

    def I062_245(self, index_start, index_end):
        """
        Target (aircraft or vehicle) identification in 8 characters. 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        # 把第一位去掉
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start+1:index_end])

        flno2_binary_str = ""
        result = ""

        # 遍历二进制字符串并按每6位处理
        for i, char in enumerate(binary_str):
            flno2_binary_str += char
            if (i + 1) % 6 == 0:
                flight_number_value = decode_functions.flight_number_decode(int(flno2_binary_str,2))
                if flight_number_value:
                    result += flight_number_value
                flno2_binary_str = ""
        out["Target Identification"]= result
        return out, index_end-index_start
  



    def I062_380(self, index_start, index_end):
        """
        Data derived directly by the aircraft.

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        for ik, key in enumerate(I062_380_mapping.keys()):
            if "(FX)" in key:
                if int(binary_str[ik]) == 0:
                    break
                else:
                    continue
            else:
                out[key]= "Presence" if int(binary_str[ik]) == 1 else "Absence"

        function_name = inspect.currentframe().f_code.co_name

        for ik, key in enumerate(out.keys()):
            if out[key] == "Presence":
                out[key]= apply_func(function_name+"_"+key[1:-1], self.byte_data[index_end:index_end+I062_380_mapping[key]])
                index_end+= I062_380_mapping[key]
            else:
                pass

        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
        return out, index_end-index_start
    
    




    def I062_040(self, index_start, index_end):
        """
        Identification of a track  

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        out["Track number"]= str((self.byte_data[index_start] << 8)+ self.byte_data[index_start+1])
        return out, index_end-index_start
    



    def I062_080(self, index_start, index_end):
        """
        Track status. 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end],'08b'))
            index_end+= 1


        for ik, key in enumerate(I062_080_mapping.keys()):
            if "(FX)" in key:
                if int(binary_str[ik]) == 0:
                    break
                else:
                    continue

            elif "copy" in key:
                continue

            elif any(item in key for item in ["(SRC)","EMS"]):
                out[key]= I062_080_mapping[key][int(binary_str[ik:ik+3],2)]

            elif any(item in key for item in ["(MD4)", "(MD5)", "SDS"]):
                out[key]= I062_080_mapping[key][int(binary_str[ik:ik+2],2)]
            else:
                out[key]= I062_080_mapping[key][int(binary_str[ik])]

        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
        return out, index_end-index_start
    


    def I062_290(self, index_start, index_end):
        """
        System Track Update Ages 
        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        for ik, key in enumerate(I062_290_mapping.keys()):
            if "(FX)" in key:
                if int(binary_str[ik]) == 0:
                    break
                else:
                    continue
            else:
                out[key]= "Presence" if int(binary_str[ik]) == 1 else "Absence"

        function_name = inspect.currentframe().f_code.co_name

        for ik, key in enumerate(out.keys()):
            if out[key] == "Presence":
                out[key]= apply_func(function_name+"_"+key[1:-1], self.byte_data[index_end:index_end+I062_290_mapping[key]])
                index_end+= I062_290_mapping[key]
            else:
                pass


        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
        return out, index_end-index_start
    



    def I062_200(self, index_start, index_end):
        """
        Mode of Movement  
        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out =dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        assert int(binary_str[-1]) == 0, "binary_str[-1] should be 0"
        for ik, key in enumerate(I062_200_mapping.keys()):
            if ik < 3:
                out[key]= I062_200_mapping[key][int(binary_str[ik*2:ik*2+1],2)]
            else:
                if "Spare" not in key:
                    out[key]= I062_200_mapping[key][int(binary_str[ik],2)]
        return out, index_end-index_start
    



    def I062_295(self, index_start, index_end):
        """
        Track Data Ages
        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        for ik, key in enumerate(I062_295_mapping.keys()):
            if "(FX)" in key:
                if int(binary_str[ik]) == 0:
                    break
                else:
                    continue
            else:
                out[key]= "Presence" if int(binary_str[ik]) == 1 else "Absence"

        function_name = inspect.currentframe().f_code.co_name

        for ik, key in enumerate(out.keys()):
            if out[key] == "Presence":
                out[key]= apply_func(function_name+"_"+"age", self.byte_data[index_end:index_end+I062_295_mapping[key]],key[1:-1])
                index_end+= I062_295_mapping[key]
            else:
                pass


        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
        return out, index_end-index_start


        


    def I062_136(self, index_start, index_end):
        """
        Last valid and credible flight level used to update the track, in two’s 
        complement form. 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        out["Flight level"] = str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])),2)*0.25) + " "+ "FL"
        return out, index_end-index_start
    

    

    def I062_130(self, index_start, index_end):
        """
        Calculated Track Geometric Altitude

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        out["vertical distance"]= str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])),2)*6.25) + " "+ "ft"
        return out, index_end-index_start
    



    def I062_135(self, index_start, index_end):
        """
        Calculated Track Barometric Altitude

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        out["QNH"]= "No QNH correction applied" if int(binary_str[0]) == 0 else "QNH correction applied"
        out["Barometric altitude"]= str(float(int(decode_functions.invert_binary_if_negative(binary_str[1:]),2))*0.25) + " "+ "FL"
        return out, index_end-index_start

    



    def I062_220(self, index_start, index_end):
        """
        Calculated rate of Climb/Descent of an aircraft in two’s complement 
        form. 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        out["Rate of climb/descent"]= str(int(decode_functions.invert_binary_if_negative("".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])),2)*6.25) + " "+ "feet/minute"
        return out, index_end-index_start
    



    def I062_390(self, index_start, index_end):
        """
        Flight Plan Related Data 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        for ik, key in enumerate(I062_390_mapping.keys()):
            if "(FX)" in key:
                if int(binary_str[ik]) == 0:
                    break
                else:
                    continue
            else:
                out[key]= "Presence" if int(binary_str[ik]) == 1 else "Absence"

        function_name = inspect.currentframe().f_code.co_name

        for ik, key in enumerate(out.keys()):
            if out[key] == "Presence":
                out[key]= apply_func(function_name+"_"+key[1:-1], self.byte_data[index_end:index_end+I062_390_mapping[key]])
                index_end+= I062_390_mapping[key]
            else:
                pass


        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
        return out, index_end-index_start
    



    def I062_270(self, index_start, index_end):
        """
        Target Size & Orientation

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1


        structure_level= 0

        function_name = inspect.currentframe().f_code.co_name

        while (8*(structure_level+1)) <= len(binary_str):
            out[I062_270_list[structure_level]]= apply_func(function_name+"_"+I062_270_list[structure_level], self.byte_data[8*structure_level:8*(structure_level+1)])
            structure_level+= 1
    
        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)

        return out, index_end-index_start
    

    
    




    def I062_300(self, index_start, index_end):
        """
        Vehicle Fleet Identification

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        vfi_list= ["Unknown", "ATC equipment maintenance", "Airport maintenance", "Fire", "Bird scarer", "Snow plough", "Runway sweeper", 
 "Emergency", "Police", "Bus", "Tug (push/tow)", "Grass cutter", "Fuel", "Baggage", "Catering", "Aircraft maintenance", "Flyco (follow me)"]
        out["VFI"]= vfi_list[int("".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end]),2)]

        return out, index_end-index_start
    




    def I062_110(self, index_start, index_end):
        """
        Mode 5 Data reports & Extended Mode 1 Code

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        for ik, key in enumerate(I062_110_mapping.keys()):
            if "(FX)" in key:
                if int(binary_str[ik]) == 0:
                    break
                else:
                    continue
            else:
                out[key]= "Presence" if int(binary_str[ik]) == 1 else "Absence"

        function_name = inspect.currentframe().f_code.co_name

        for ik, key in enumerate(out.keys()):
            if out[key] == "Presence":
                out[key]= apply_func(function_name+"_"+key[1:-1], self.byte_data[index_end:index_end+I062_110_mapping[key]])
                index_end+= I062_110_mapping[key]
            else:
                pass


        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
        return out, index_end-index_start
    




    def I062_120(self, index_start, index_end):
        """
        Track Mode 2 Code  

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str= "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])

        assert binary_str[:4] == "0000", "I062_120: binary_str[:4] != '0000'"

        out["Track Mode 2 Code"]= oct(int(binary_str[4:],2))
        
        return out, index_end-index_start
    



    def I062_510(self, index_start, index_end):
        """
        Composed Track Number 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end+2], '08b'))
            index_end+= 1+2

        structure_level= 0

        function_name = inspect.currentframe().f_code.co_name

        while (24*(structure_level+1)) <= len(binary_str):
            out["Composed Track Number "+ str(structure_level)]= apply_func(function_name+"_"+"composed", self.byte_data[24*structure_level:24*(structure_level+1)])
            structure_level+= 1


        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
    

        return out, index_end-index_start
    



    def I062_500(self, index_start, index_end):
        """
        Overview of all important accuracies

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        for ik, key in enumerate(I062_500_mapping.keys()):
            if "(FX)" in key:
                if int(binary_str[ik]) == 0:
                    break
                else:
                    continue
            else:
                out[key]= "Presence" if int(binary_str[ik]) == 1 else "Absence"

        function_name = inspect.currentframe().f_code.co_name

        for ik, key in enumerate(out.keys()):
            if out[key] == "Presence":
                out[key]= apply_func(function_name+"_"+key[1:-1], self.byte_data[index_end:index_end+I062_500_mapping[key]])
                index_end+= I062_500_mapping[key]
            else:
                pass


        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
        return out, index_end-index_start
    



    def I062_340(self, index_start, index_end):
        """
        Measured Information

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        for ik, key in enumerate(I062_340_mapping.keys()):
            if "(FX)" in key :
                if int(binary_str[ik]) == 0:
                    break
                else:
                    continue

            elif "(spare)" in key:
                continue
            else:
                out[key]= "Presence" if int(binary_str[ik]) == 1 else "Absence"

        function_name = inspect.currentframe().f_code.co_name

        for ik, key in enumerate(out.keys()):
            if out[key] == "Presence":
                out[key]= apply_func(function_name+"_"+key[1:-1], self.byte_data[index_end:index_end+I062_340_mapping[key]])
                index_end+= I062_340_mapping[key]
            else:
                pass


        pop_key_list=[]
        for ik, key in enumerate(out.keys()):
            if out[key] == "Absence":
                pop_key_list.append(key)
        for key in pop_key_list:
            out.pop(key)
        return out, index_end-index_start
    




    def RE(self, index_start, index_end):
        """
        Reserved Expansion Field

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        structure_level= 0

        while (8*(structure_level+1)) <= len(binary_str):
            out["RE "+ str(structure_level)]= binary_str[8*(structure_level):8*(structure_level+1)]
            structure_level+= 1

        return out, index_end-index_start


    




    def SP(self, index_start, index_end):
        """
        Reserved For Special Purpose Indicator 

        Args:
            index_start (_type_): int
            index_end (_type_): int

        Returns:
            _type_: dictionary, int
        """
        out=dict()
        binary_str = "".join(format(byte, '08b') for byte in self.byte_data[index_start:index_end])
        while int(binary_str[-1]) == 1:
            binary_str += str(format(self.byte_data[index_end], '08b'))
            index_end+= 1

        structure_level= 0

        while (8*(structure_level+1)) <= len(binary_str):
            out["SP "+ str(structure_level)]= binary_str[8*(structure_level):8*(structure_level+1)]
            structure_level+= 1

        return out, index_end-index_start




    def save2json(self, output_path= rf"outputs"):
        # 调用函数处理并输出 JSON 文件
        try:
            # 将解析结果输出到 JSON 文件
            with open(output_path+"/"+"cat062"+self.save_name+".json", "w", encoding="utf-8") as json_file:
                json.dump(self.result, json_file, ensure_ascii=False, indent=4)
        except ValueError as e:
            print(e)

    @staticmethod
    def save2json_static(result, output_path= rf"outputs", save_name= ""):
        # 调用函数处理并输出 JSON 文件
        try:
            # 将解析结果输出到 JSON 文件
            with open(output_path+"/"+"cat062"+save_name+".json", "w", encoding="utf-8") as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)
        except ValueError as e:
            print(e)


# 测试数据
# TEST!
BD= byte_decoder()
print(BD.process_byte_data())
BD.save2json()