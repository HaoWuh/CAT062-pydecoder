from injector import singleton



def apply_func(func_name, *args):

    functions= decode_functions()

    try:
        method = getattr(functions, func_name)
    except:
        raise Exception(func_name, " Method not found")

    return method(*args)


@singleton
class decode_functions:

    @staticmethod
    def test_func():
        print("Test!")
        return True
    

    @staticmethod
    def invert_binary_if_negative(binary_str):
        if binary_str[0] == '1':  
            inverted_binary = ''.join('1' if b == '0' else '0' for b in binary_str)
            return "-"+inverted_binary
        else:
            return binary_str  
    


    @staticmethod
    def binary_to_decimal(binary_str):
        if binary_str[0] == '1':  

            inverted_binary = ''.join('1' if b == '0' else '0' for b in binary_str)  
            decimal_value = -(int(inverted_binary, 2) + 1)  

        else:  
            
            decimal_value = int(binary_str, 2)

        return decimal_value
    


    @staticmethod
    def flight_number_decode(byte_number):
        if byte_number >= 1 and byte_number <= 26:
            return chr(ord('A')+byte_number-1)
        elif byte_number == 32:
            return " "
        elif byte_number >= 48 and byte_number <= 57:
            return chr(ord('0')+byte_number-48)
        else:
            return ""
        
        
    @staticmethod
    def des2val_des(des, des_list):
        return {'val': des_list.index(des), 'meaning': des}
    
    
    
    @staticmethod
    def clean_str2val(obj):
        if isinstance(obj, list):
            for ob in obj:
                ob= decode_functions.clean_str2val(ob)
            return obj
        
        elif isinstance(obj, dict):
            ks= [k for k in obj.keys()]
            for key in ks:
                if (key[0] == '(' and key[-1] == ')'):
                    obj[key[1:-1]]= decode_functions.clean_str2val(obj.pop(key))
                else:
                    obj[key]= decode_functions.clean_str2val(obj[key])
            return obj
                
        elif isinstance(obj, str):
            val= obj
            try:
                val= int(obj)
            except:
                try:
                    val= float(obj)
                except:
                    if " " in obj:
                        try:
                            val= float(obj[:obj.rfind(" ")])
                        except:
                            pass
                    else:
                        pass
            return val
        else:
            return obj
    


    @staticmethod
    def I062_380_ADR(b_data):
        out=dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        out["Target address"]= hex(int(binary_str,2))

        return out
    

    @staticmethod
    def I062_380_ID(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])

        out["Target identity"]= ""
        
        for i in range(int(len(binary_str)/6)):
            out["Target identity"]+= decode_functions.flight_number_decode(int(binary_str[6*i: 6*(i+1)],2))
  
        return out
    


    @staticmethod
    def I062_380_MHG(b_data):
        out=dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["Megnetic heading"]= str(int(binary_str,2)*(360.0/2**16))+" "+"o"
        return out


    
    @staticmethod
    def I062_380_IAS(b_data):
        out=dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        type= None
        if int(binary_str[0]) == 0:
            type= "IAS"
            out= type+ " "+ str(int(decode_functions.invert_binary_if_negative(binary_str[1:],2))*2**(-14))+" "+"NM/s"
        else:
            type= "MACH"
            out= type+ " "+ str(int(decode_functions.invert_binary_if_negative(binary_str[1:],2))*0.001)
            pass
        
        return out



    @staticmethod
    def I062_380_TAS(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["True airspeed"]= str(int(binary_str,2))+" "+"knots"
        return out
    


    @staticmethod
    def I062_380_SAL(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        alttitude_str= decode_functions.invert_binary_if_negative(binary_str[3:16])
        out["SAS"]= "provided" if int(binary_str[0]) == 1 else "not provided"
        source_list= ["Unknown","Aircraft alttitude","FCU/MCP selected alttitude","FMS selected alttitude"]
        out["Source"]= source_list[int(binary_str[1:3],2)]
        out["Source"]= decode_functions.des2val_des(out["Source"], source_list)
        out["Alttitude"]= str(int(alttitude_str,2)*25)+" "+"ft"

        return out
    


    @staticmethod
    def I062_380_FSS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        alttitude_str= decode_functions.invert_binary_if_negative(binary_str[3:16])
        out["Manage vertical mode"]= "Active" if int(binary_str[0]) == 1 else "Not active"
        out["Alttitude hold"]= "Active" if int(binary_str[1]) == 1 else "Not active"
        out["Approach mode"]= "Active" if int(binary_str[2]) == 1 else "Not active"
        out["Alttitude"]= str(int(alttitude_str,2)*25)+" "+"ft"
        return out
    



    @staticmethod
    def I062_380_TIS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        out["NAV"]= "available" if int(binary_str[0]) == 0 else "not available"
        out["NAV"]= decode_functions.des2val_des(out["NAV"], ["available","not available"])
        out["NVB"]= "valid" if int(binary_str[1]) == 0 else "not valid"
        out["NVB"]= decode_functions.des2val_des(out["NVB"], ["valid","not valid"])
        return out
    


    @staticmethod
    def I062_380_TID(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        out["REP"]= str(int(binary_str[:8],2))
        
        count_rep= 0
        out["rep_content"]= []
        pos= 8
        
        while count_rep < int(out["REP"]):
            rep_dict= dict()
            
            rep_dict["TCA"]= binary_str[pos]
            pos+= 1
            rep_dict["NC"]= binary_str[pos]
            pos+= 1
            rop_dict["TCP"]= hex(int(binary_str[pos:pos+6],2))
            pos+= 6

            alttitude_str= decode_functions.invert_binary_if_negative(binary_str[pos:pos+16])
            rep_dict["Altitude"]= str(int(alttitude_str,2)*10)+" "+"ft"
            pos+= 16

            latitude_str= decode_functions.invert_binary_if_negative(binary_str[pos:pos+24])
            rep_dict["Latitude"]= str(int(latitude_str,2)*(180.0/2**23))+" "+"deg"
            pos+= 24

            longitude_str= decode_functions.invert_binary_if_negative(binary_str[pos:pos+36])
            rep_dict["Longitude"]= str(int(longitude_str,2)*(180.0/2**23))+" "+"deg"
            pos+= 36

            point_list=[
                        "Unknown",
                        "Fly by waypoint (LT)",
                        "Fly over waypoint (LT)",
                        "Hold pattern (LT)",
                        "Procedure hold (LT)",
                        "Procedure turn (LT)",
                        "RF leg (LT)",
                        "Top of climb (VT)",
                        "Top of descent (VT)",
                        "Start of level (VT)",
                        "Cross-over altitude (VT)",
                        "Transition altitude (VT)"
                    ]
            rep_dict["Point type"]= point_list[int(binary_str[pos:pos+4],2)]
            rep_dict["Point type"]= decode_functions.des2val_des(rep_dict["Point type"], point_list)
            pos+=4

            td_list= [
                        "N/A",
                        "Turn right",
                        "Turn left",
                        "No turn"
                    ]
            rep_dict["TD"]= td_list[int(binary_str[pos:pos+2],2)]
            rep_dict["TD"]= decode_functions.des2val_des(rep_dict["TD"], td_list)
            pos+= 2

            rep_dict["TRA"]= "TTR not available" if int(binary_str[pos]) == 0 else "TTR available"
            rep_dict["TRA"]= decode_functions.des2val_des(rep_dict["TRA"], ["TTR not available","TTR available"])
            pos+= 1
            rep_dict["TOA"]= "TOV available" if int(binary_str[pos]) == 0 else "TOV not available"
            rep_dict["TOA"]= decode_functions.des2val_des(rep_dict["TOA"], ["TOV available","TOV not available"])
            pos+= 1

            tov_str= decode_functions.invert_binary_if_negative(binary_str[pos:pos+24])
            rep_dict["TOV"]= str(int(tov_str,2)*1)+" "+"second"
            pos+= 24

            ttr_str= decode_functions.invert_binary_if_negative(binary_str[pos:pos+16])
            rep_dict["TTR"]= str(int(ttr_str,2)*0.01)+" "+"Nm"
            pos+= 16
            
            out["rep_content"].append(rep_dict)
            count_rep+= 1


        return out
    


    @staticmethod
    def I062_380_COM(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        
        com_list= [
                    "No communications capability (surveillance only)",
                    "Comm. A and Comm. B capability",
                    "Comm. A, Comm. B and Uplink ELM",
                    "Comm. A, Comm. B, Uplink ELM and Downlink ELM",
                    "Level 5 Transponder capability"
                ]
        out["COM"]= com_list[int(binary_str[0:3],2)]
        out["COM"]= decode_functions.des2val_des(out["COM"], com_list)

        stat_list= [
                    "No alert, no SPI, aircraft airborne",
                    "No alert, no SPI, aircraft on ground",
                    "Alert, no SPI, aircraft airborne",
                    "Alert, no SPI, aircraft on ground",
                    "Alert, SPI, aircraft airborne or on ground",
                    "No alert, SPI, aircraft airborne or on ground",
                    "Not defined",
                    "Unknown or not yet extracted"
                ]
        out["STAT"]= stat_list[int(binary_str[3:6],2)]
        out["STAT"]= decode_functions.des2val_des(out["STAT"], stat_list)
        assert binary_str[6:8] == "00", "bits must be 00"

        out["SSC"]= "No" if int(binary_str[8]) == 0 else "Yes"
        out["SSC"]= decode_functions.des2val_des(out["SSC"], ["No","Yes"])
        out["ARC"]= ("100" if int(binary_str[9]) == 0 else "25") + " ft resolution"
        out["ARC"]= decode_functions.des2val_des(out["ARC"], ["100 ft resolution","25 ft resolution"])
        out["AIC"]= "No" if int(binary_str[10]) == 0 else "Yes"
        out["AIC"]= decode_functions.des2val_des(out["AIC"], ["No","Yes"])
        out["B1A"]= binary_str[11]
        out["B1B"]= binary_str[12:16]


        return out
    



    @staticmethod
    def I062_380_SAB(b_data):

        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        ac_list= [
                    "unknown",
                    "ACAS not operational",
                    "ACAS operational",
                    "invalid"
                ]
        out["AC"]= ac_list[int(binary_str[0:2],2)]
        out["AC"]= decode_functions.des2val_des(out["AC"], ac_list)

        mn_list= [
                    "unknown",
                    "Multiple navigational aids not operating",
                    "Multiple navigational aids operating",
                    "invalid"
                ]
        out["MN"]= mn_list[int(binary_str[2:4],2)]
        out["MN"]= decode_functions.des2val_des(out["MN"], mn_list)

        dc_list= [
                    "unknown",
                    "Differential correction",
                    "No differential correction",
                    "invalid"
                ]
        out["DC"]= dc_list[int(binary_str[4:6],2)]
        out["DC"]= decode_functions.des2val_des(out["DC"], dc_list)

        out["GBS"]= "Transponder Ground Bit "+ ("not set or unknown" if int(binary_str[6]) == 0 else "set")
        out["GBS"]= decode_functions.des2val_des(out["GBS"], ["Transponder Ground Bit not set or unknown","Transponder Ground Bit set"])
        assert binary_str[7:13] == "000000", "bits must be 000000"

        stat_list=[
                    "No emergency",
                    "General emergency",
                    "Lifeguard / medical",
                    "Minimum fuel",
                    "No communications",
                    "Unlawful interference",
                    "Downed Aircraft",
                    "Unknown"
                ]
        out["STAT"]= stat_list[int(binary_str[13:16],2)]
        out["STAT"]= decode_functions.des2val_des(out["STAT"], stat_list)

        return out
    


    @staticmethod
    def I062_380_ACS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        out["ACAS"]= binary_str
        return out
    


    @staticmethod
    def I062_380_BVR(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["BVR"]= str(int(binary_str,2)*6.25)+" "+"feet/minute"

        return out
    


    @staticmethod
    def I062_380_GVR(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["GVR"]= str(int(binary_str,2)*6.25)+" "+"feet/minute"

        return out
    


    @staticmethod
    def I062_380_RAN(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["RA"]= str(int(binary_str,2)*0.01)+" "+"deg"

        return out
    


    @staticmethod
    def I062_380_TAR(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        ti_list= [
                    "Not available",
                    "Left",
                    "Right",
                    "Straight"
                ]
        out["TI"]= ti_list[int(binary_str[0:2],2)]
        out["TI"]= decode_functions.des2val_des(out["TI"], ti_list)
        assert binary_str[2:8] == "000000", "bits must be 000000"
        rt_str= decode_functions.invert_binary_if_negative(binary_str[8:15])
        out["Rate of turn"]= str(int(rt_str,2)*0.25)+" "+"deg/s"
        assert binary_str[15] == "0", "bit must be 0"
        return out
    



    @staticmethod
    def I062_380_TAN(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["TA"]= str(int(binary_str,2)*(360.0/2**16))+" "+"deg"

        return out
    



    @staticmethod
    def I062_380_GSP(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["GS"]= str(int(binary_str,2)*(1.0/2**14))+" "+"NM/s"

        return out
    



    @staticmethod
    def I062_380_VUN(b_data):
        out =dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        out["Velocity uncertainty category"]= hex(int(binary_str,2))

        return out
    



    @staticmethod
    def I062_380_MET(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        out["WS"]= ("Not valid" if int(binary_str[0]) == 0 else "Valid") + " wind speed"
        out["WS"]= decode_functions.des2val_des(out["WS"], ["Not valid wind speed","Valid wind speed"])
        out["WD"]= ("Not valid" if int(binary_str[1]) == 0 else "Valid") + " wind direction"
        out["WD"]= decode_functions.des2val_des(out["WD"], ["Not valid wind direction","Valid wind direction"])
        out["TMP"]= ("Not valid" if int(binary_str[2]) == 0 else "Valid") + " temperature"
        out["TMP"]= decode_functions.des2val_des(out["TMP"], ["Not valid temperature","Valid temperature"])
        out["TRB"]= ("Not valid" if int(binary_str[3]) == 0 else "Valid") + " turbulence"
        out["TRB"]= decode_functions.des2val_des(out["TRB"], ["Not valid turbulence","Valid turbulence"])

        assert binary_str[4:8] == "0000", "bits must be 0000"

        ws_str= decode_functions.invert_binary_if_negative(binary_str[8:24])
        out["Wind speed"]= str(int(ws_str,2)*1)+" "+"knots"

        wd_str= decode_functions.invert_binary_if_negative(binary_str[24:40])
        out["Wind direction"]= str(int(wd_str,2)*1)+" "+"deg"

        t_str= decode_functions.invert_binary_if_negative(binary_str[40:56])
        out["Temperature"]= str(int(t_str,2)*0.25)+" "+"deg C"

        out["Turbulence"]= str(int(binary_str[56:64],2))

        return out
    



    @staticmethod
    def I062_380_EMC(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        out["ECAT"]= binary_str

        return out
    



    @staticmethod
    def I062_380_POS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        lattitude_str= decode_functions.invert_binary_if_negative(binary_str[0:24])
        out["Latitude"]= str(int(lattitude_str,2)*(180.0/2**23))+" "+"deg"

        longitude_str= decode_functions.invert_binary_if_negative(binary_str[24:48])
        out["Longitude"]= str(int(longitude_str,2)*(180.0/2**23))+" "+"deg"


        return out
    



    @staticmethod
    def I062_380_GAL(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        alttitude_str= decode_functions.invert_binary_if_negative(binary_str)

        out["Altitude"]= str(int(alttitude_str,2)*6.25)+" "+"ft"

        return out
    



    @staticmethod
    def I062_380_PUN(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        assert binary_str[:4] == "0000", "bits must be 0000"


        out["PUN"]= str(int(binary_str[4:8],2))

        return out
    


    @staticmethod
    def I062_380_MB(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        rep_str= binary_str[0:8]
        out["REP"]= str(int(rep_str,2))
        
        count_rep= 0
        out["rep_content"]= []
        pos= 8
        
        while count_rep < int(out["REP"]):
            rep_dict= dict()

            rep_dict["MSB"]= binary_str[pos:pos+56]
            pos+= 56

            rep_dict["BDS1"]= hex(int(binary_str[pos:pos+4],2))
            pos+= 4
            rep_dict["BDS2"]= hex(int(binary_str[pos:pos+4],2))
            pos+= 4
            
            out["rep_content"].append(rep_dict)
            count_rep+= 1

        return out
    


    
    @staticmethod
    def I062_380_IAR(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        ia_str= decode_functions.invert_binary_if_negative(binary_str)

        out["INdecated airspeed"]= str(int(ia_str,2)*1)+" "+"Kt"

        return out
    


    @staticmethod
    def I062_380_MAC(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        ma_str= decode_functions.invert_binary_if_negative(binary_str)

        out["Mach number"]= "Mach "+str(int(ma_str,2)*0.008)

        return out
    


    @staticmethod
    def I062_380_BPS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        assert binary_str[0:4] == "0000", "bits must be 0000"

        bps_str= decode_functions.invert_binary_if_negative(binary_str[4:])

        out["BPS"]= str(int(bps_str,2)*0.1)+" "+"mb"

        return out
    




    @staticmethod
    def I062_290_TRK(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        trk_str= decode_functions.invert_binary_if_negative(binary_str)

        out["TRK"]= str(int(trk_str,2)*(0.25))+" "+"s"
        return out
    



    @staticmethod
    def I062_290_PSR(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        psr_str= decode_functions.invert_binary_if_negative(binary_str)

        out["PSR"]= str(int(psr_str,2)*0.25)+" "+"s"
        return out
    



    @staticmethod
    def I062_290_SSR(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        ssr_str= decode_functions.invert_binary_if_negative(binary_str)

        out["SSR"]= str(int(ssr_str,2)*0.25)+" "+"s"
        return out
    



    @staticmethod
    def I062_290_MDS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        mds_str= decode_functions.invert_binary_if_negative(binary_str)

        out["MDS"]= str(int(mds_str,2)*0.25)+" "+"s"
        return out
    



    @staticmethod
    def I062_290_ADS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        ads_str= decode_functions.invert_binary_if_negative(binary_str)

        out["ADS"]= str(int(ads_str,2)*0.25)+" "+"s"
        return out
    



    @staticmethod
    def I062_290_ES(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        es_str= decode_functions.invert_binary_if_negative(binary_str)

        out["ES"]= str(int(es_str,2)*0.25)+" "+"s"
        return out
    



    @staticmethod
    def I062_290_VDL(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        vdl_str= decode_functions.invert_binary_if_negative(binary_str)

        out["VDL"]= str(int(vdl_str,2)*0.25)+" "+"s"
        return out
    




    @staticmethod
    def I062_290_UAT(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        uat_str= decode_functions.invert_binary_if_negative(binary_str)

        out["UAT"]= str(int(uat_str,2)*0.25)+" "+"s"
        return out
    



    @staticmethod
    def I062_290_LOP(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        lop_str= decode_functions.invert_binary_if_negative(binary_str)

        out["LOP"]= str(int(lop_str,2)*0.25)+" "+"s"
        return out
    



    @staticmethod
    def I062_290_MLT(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        mlt_str= decode_functions.invert_binary_if_negative(binary_str)

        out["MLT"]= str(int(mlt_str,2)*0.25)+" "+"s"
        return out
    




    @staticmethod
    def I062_295_age(b_data, key):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        key_str= decode_functions.invert_binary_if_negative(binary_str)

        out[key]= str(int(key_str,2)*0.25)+" "+"s"
        return out
    



    @staticmethod
    def I062_390_TAG(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        
        sac_str= binary_str[0:8]
        out["SAC"]= str(int(sac_str,2))

        sic_str= binary_str[8:16]
        out["SIC"]= str(int(sic_str,2))

        return out
    




    @staticmethod
    def I062_390_CSN(b_data):
        out= dict()

        out["Callsign"]= "".join([chr(int(b)) for b in b_data])
        return out
    




    @staticmethod
    def I062_390_IFI(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        typ_list= ["Plan Number", "Unit 1 internal flight number", "Unit 2 internal flight number", "Unit 3 internal flight number"]
        out["TYP"]= typ_list[int(binary_str[0:2],2)]
        out["TYP"]= decode_functions.des2val_des(out["TYP"], typ_list)

        assert binary_str[2:5] == "000", "bit must be 000"

        out["NBR"]= str(int(binary_str[5:32],2))

        return out
    


    @staticmethod
    def I062_390_FCT(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        gatoat_list= ["Unknown", "General Air Traffic", "Operational Air Traffic", "Not applicable"]
        out["GAT/OAT"]= gatoat_list[int(binary_str[0:2],2)]
        out["GAT/OAT"]= decode_functions.des2val_des(out["GAT/OAT"], gatoat_list)

        fr1fr2_list= ["Instrument Flight Rules", "Visual Flight Rules", "Not applicable", "Controlled Visual Flight Rules"]
        out["FR1/FR2"]= fr1fr2_list[int(binary_str[2:4],2)]
        out["FR1/FR2"]= decode_functions.des2val_des(out["FR1/FR2"], fr1fr2_list)

        rvsm_list= ["Unknown", "Approved", "Exempt", "Not Approved"]
        out["RVSM"]= rvsm_list[int(binary_str[4:6],2)]
        out["RVSM"]= decode_functions.des2val_des(out["RVSM"], rvsm_list)

        hpr_list= ["Normal Priority Flight", "High Priority Flight"]
        out["HPR"]= hpr_list[int(binary_str[6:7],2)]
        out["HPR"]= decode_functions.des2val_des(out["HPR"], hpr_list)

        if not binary_str[7] == "0":
            print("warning: detect unexpected non-zero bit!")

        return out
    


    @staticmethod
    def I062_390_TAC(b_data):
        out= dict()

        out["Type of aircraft"]= "".join([chr(int(b)) for b in b_data])
        return out
    


    @staticmethod
    def I062_390_WTC(b_data):
        out= dict()

        out["Wake turbulence category"]= "".join([chr(int(b)) for b in b_data])
        return out
    



    @staticmethod
    def I062_390_DEP(b_data):
        out= dict()

        out["Departure airport"]= "".join([chr(int(b)) for b in b_data])
        return out
    



    @staticmethod
    def I062_390_DST(b_data):
        out= dict()

        out["Destination airport"]= "".join([chr(int(b)) for b in b_data])
        return out
    



    @staticmethod
    def I062_390_RDS(b_data):

        out= dict()

        out["NU1"]= "".join([chr(int(b_data[0]))])
        out["NU2"]= "".join([chr(int(b_data[1]))])
        out["LTR"]= "".join([chr(int(b_data[2]))])

        return out
    



    @staticmethod
    def I062_390_CFL(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        cfl_str= decode_functions.invert_binary_if_negative(binary_str)

        out["CFL"]= str(int(cfl_str,2)*0.25)+" "+"FL"

        return out
    



    @staticmethod
    def I062_390_CTL(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        cen_str= decode_functions.invert_binary_if_negative(binary_str[0:8])

        out["Centre"]= hex(int(cen_str,2))

        pos_str= decode_functions.invert_binary_if_negative(binary_str[8:16])

        out["Position"]= hex(int(pos_str,2))

        return out
    



    @staticmethod
    def I062_390_TOD(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        
        rep_str= binary_str[0:8]
        out["REP"]= str(int(rep_str,2))
        
        count_rep= 0
        out["rep_content"]= []
        pos= 8
        
        while count_rep < int(out["REP"]):
            rep_dict= dict()
            typ_list= ["Scheduled off-block time", "Estimated off-block time", "Estimated take-off time", "Actual off-block time", 
     "Predicted time at runway hold", "Actual time at runway hold", "Actual line-up time", "Actual take-off time", 
     "Estimated time of arrival", "Predicted landing time", "Actual landing time", "Actual time off runway", 
     "Predicted time to gate", "Actual on-block time"]
            rep_dict["TYP"]= typ_list[int(binary_str[pos:pos+5],2)]
            rep_dict["TYP"]= decode_functions.des2val_des(rep_dict["TYP"], typ_list)
            pos+= 5
            
            day_list= ["Today", "Yesterday", "Tomorrow", "Invalid"]
            rep_dict["DAY"]= day_list[int(binary_str[pos:pos+2],2)]
            rep_dict["DAY"]= decode_functions.des2val_des(rep_dict["DAY"], day_list)
            pos+= 2

            assert binary_str[pos] == "0", "bit must be 0"
            assert binary_str[pos+1:pos+4] == "000", "bit must be 000"
            pos+= 4

            hor_str= binary_str[pos:pos+5]
            rep_dict["HOR"]= str(int(hor_str,2))
            pos+= 5

            assert binary_str[pos:pos+2] == "00", "bit must be 00"
            pos+= 2

            min_str= binary_str[pos:pos+6]
            rep_dict["MIN"]= str(int(min_str,2))
            pos+=6

            rep_dict["AVS"]= binary_str[pos]
            pos+=1
            assert binary_str[pos] == "0", "bit must be 0"
            pos+=1

            sec_str= binary_str[pos:pos+6]
            rep_dict["SEC"]= str(int(sec_str,2))
            pos+= 6
            
            out["rep_content"].append(rep_dict)
            count_rep+= 1


        return out




    @staticmethod
    def I062_390_AST(b_data):
        out= dict()

        out["Aircraft stand"]= "".join([chr(int(b)) for b in b_data])
        return out
    



    @staticmethod
    def I062_390_STS(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])

        emp_list= ["Empty", "Occupied", "Unknown", "Invalid"]
        out["EMP"]= emp_list(int(binary_str[0:2],2))
        out["EMP"]= decode_functions.des2val_des(out["EMP"], emp_list)

        avl_list= ["Available", "Not available", "Unknown", "Invalid"]
        out["AVL"]= avl_list(int(binary_str[2:4],2))
        out["AVL"]= decode_functions.des2val_des(out["AVL"], avl_list)

        return out
    



    @staticmethod
    def I062_390_STD(b_data):
        out= dict()

        out["Standard instrument departure"]= "".join([chr(int(b)) for b in b_data])
        return out
    



    @staticmethod
    def I062_390_STA(b_data):
        out= dict()

        out["Standard instrument arrival"]= "".join([chr(int(b)) for b in b_data])
        return out
    



    @staticmethod
    def I062_390_PEM(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])

        assert binary_str[0:3] == "000", "bit must be 000"

        out["VA"]= binary_str[3]

        if int(out["VA"]) == 1:
            out["mode-3/A"]= oct(int(binary_str[4:],2))

        return out
    




    @staticmethod
    def I062_390_PEC(b_data):
        out= dict()

        out["Pre-emergency callsign"]= "".join([chr(int(b)) for b in b_data])
        return out
    



    @staticmethod
    def I062_270_LENGTH(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        length_str= binary_str[0:7]
        out["Length"]= str(int(length_str,2)*(1))+ " "+"m"
        return out
    



    @staticmethod
    def I062_270_ORIENTATION(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        orientation_str= binary_str[0:7]
        out["Orientation"]= str(int(orientation_str,2)*(360.0/128))+ " "+"deg"
        return out
    



    @staticmethod
    def I062_270_WIDTH(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        width_str= binary_str[0:7]
        out["Width"]= str(int(width_str,2)*(1))+ " "+"m"
        return out


    @staticmethod
    def I062_110_SUM(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])

        m5_list= ["No Mode 5 interrogation", "Mode 5 interrogation"]
        out["M5"]= m5_list[int(binary_str[0:1],2)]
        out["M5"]= decode_functions.des2val_des(out["M5"], m5_list)

        id_list= ["No authenticated Mode 5 ID reply", "Authenticated Mode 5 ID reply"]
        out["ID"]= id_list[int(binary_str[1:2],2)]
        out["ID"]= decode_functions.des2val_des(out["ID"], id_list)

        da_list= ["No authenticated Mode 5 Data reply or Report", "Authenticated Mode 5 Data reply or Report (i.e any valid Mode 5 reply type other than ID)"]
        out["DA"]= da_list[int(binary_str[2:3],2)]
        out["DA"]= decode_functions.des2val_des(out["DA"], da_list)

        m1_list= ["Mode 1 code not present or not from Mode 5 reply", "Mode 1 code from Mode 5 reply"]
        out["M1"]= m1_list[int(binary_str[3:4],2)]
        out["M1"]= decode_functions.des2val_des(out["M1"], m1_list)

        m2_list=["Mode 2 code not present or not from Mode 5 reply", "Mode 2 code from Mode 5 reply"]
        out["M2"]= m2_list[int(binary_str[4:5],2)]
        out["M2"]= decode_functions.des2val_des(out["M2"], m2_list)

        m3_list=["Mode 3 code not present or not from Mode 5 reply", "Mode 3 code from Mode 5 reply"]
        out["M3"]= m3_list[int(binary_str[5:6],2)]
        out["M3"]= decode_functions.des2val_des(out["M3"], m3_list)

        mc_list=["Mode C code not present or not from Mode 5 reply", "Mode C code from Mode 5 reply"]
        out["MC"]= mc_list[int(binary_str[6:7],2)]
        out["MC"]= decode_functions.des2val_des(out["MC"], mc_list)

        x_list= ["X-pulse set to zero or no authenticated Data reply or Report received", "X-pulse set to one"]
        out["X"]= x_list[int(binary_str[7:8],2)]
        out["X"]= decode_functions.des2val_des(out["X"], x_list)

        return out


    @staticmethod
    def I062_110_PMN(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        assert binary_str[0:2] == "00", "bit must be 00"

        pin_str= binary_str[2:16]
        out["PIN"]= str(int(pin_str,2))

        assert binary_str[16:19] == "000", "bit must be 000"

        nat_str= binary_str[19:24]
        out["NAT"]= str(int(nat_str,2))

        assert binary_str[24:26] == "00", "bit must be 00"
        
        min_str= binary_str[26:32]
        out["MIN"]= str(int(min_str,2))

        return out
    


    @staticmethod
    def I062_110_POS(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        lattitude_str= decode_functions.invert_binary_if_negative(binary_str[0:24])
        longitude_str= decode_functions.invert_binary_if_negative(binary_str[24:48])

        out["Latitude"]= str(int(lattitude_str,2)*(180.0/2**23))+" "+"deg"
        out["Longitude"]= str(int(longitude_str,2)*(180.0/2**23))+" "+"deg"

        return out


    @staticmethod
    def I062_110_GA(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])
        assert binary_str[0:1] == "0", "bit must be 0"

        out["RES"]= "GA reported in 100 ft increments" if int(binary_str[1]) == 0 else "GA reported in 25 ft increments"
        out["RES"]= decode_functions.des2val_des(out["RES"], ["GA reported in 100 ft increments","GA reported in 25 ft increments"])

        ga_str= binary_str[2:16]
        out["GA"]= str(int(ga_str,2)*100.0)+" "+"ft" if int(binary_str[1]) == 0 else str(int(ga_str,2)*25.0)+" "+"ft"

        return out


    @staticmethod
    def I062_110_EM1(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        assert binary_str[0:4] == "0000", "bit must be 0000"

        out["EM1"]= oct(int(binary_str[4:],2))


        return out
    


    @staticmethod
    def I062_110_TOS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        
        tos_str= decode_functions.invert_binary_if_negative(binary_str)
        out["TOS"]= str(int(tos_str,2)*(1.0/128))+" "+"s"
        return out
    


    @staticmethod
    def I062_110_XP(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        assert binary_str[0:3] == "000", "bit must be 000"

        out["X5"]= binary_str[3]
        out["XC"]= binary_str[4]
        out["X3"]= binary_str[5]
        out["X2"]= binary_str[6]
        out["X1"]= binary_str[7]


        return out



    @staticmethod
    def I062_510_composed(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        id_str= binary_str[0:8]
        out["System unit ID"]= hex(int(id_str,2))

        num_str= binary_str[8:23]
        out["System track number"]= str(int(num_str,2))

        return out
    
    








    @staticmethod
    def I062_500_APC(b_data):

        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        first_str= decode_functions.invert_binary_if_negative(binary_str[0:16])
        second_str= decode_functions.invert_binary_if_negative(binary_str[16:32])
        out["APC-X"]= str(int(first_str,2)*0.5)+" "+"m"
        out["APC-Y"]= str(int(second_str,2)*0.5)+" "+"m"

        return out

    
    @staticmethod
    def I062_500_COV(b_data):
        out=dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["COV XY"]= str(int(binary_str,2)*0.5)
        return out
    
    @staticmethod
    def I062_500_APW(b_data):
        
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        first_str= decode_functions.invert_binary_if_negative(binary_str[0:16])
        second_str= decode_functions.invert_binary_if_negative(binary_str[16:32])
        out["APW-Latitude"]= str(int(first_str,2)*(180.0/2**25))+" "+"deg"
        out["APW-Longitude"]= str(int(second_str,2)*(180.0/2**25))+" "+"deg"

        return out
    
    @staticmethod
    def I062_500_AGA(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["AGA"]= str(int(binary_str,2)*6.25)+" "+"ft"
        return out
        
    
    @staticmethod
    def I062_500_ABA(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["ABA"]= str(int(binary_str,2)*0.25)+" "+"FL"
        return out
    
    @staticmethod
    def I062_500_ATV(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        first_str= decode_functions.invert_binary_if_negative(binary_str[0:8])
        second_str= decode_functions.invert_binary_if_negative(binary_str[8:16])
        out["ATV-X"]= str(int(first_str,2)*0.25)+" "+"m/s"
        out["ATV-Y"]= str(int(second_str,2)*0.25)+" "+"m/s"

        return out
    
    @staticmethod
    def I062_500_AA(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        first_str= decode_functions.invert_binary_if_negative(binary_str[0:8])
        second_str= decode_functions.invert_binary_if_negative(binary_str[8:16])
        out["AA-X"]= str(int(first_str,2)*0.25)+" "+"m/s2"
        out["AA-Y"]= str(int(second_str,2)*0.25)+" "+"m/s2"

        return out
    
    @staticmethod
    def I062_500_ARC(b_data):
        out= dict()
        binary_str= decode_functions.invert_binary_if_negative("".join([format(b, '08b') for b in b_data]))
        out["ARC"]= str(int(binary_str,2)*6.25)+" "+"feet/minute"
        return out
    



    @staticmethod
    def I062_340_SID(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        sac_str= binary_str[0:8]
        out["SAC"]= str(int(sac_str,2))

        sic_str= binary_str[8:16]
        out["SIC"]= str(int(sic_str,2))
        return out
    


    @staticmethod
    def I062_340_POS(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        rho_str= decode_functions.invert_binary_if_negative(binary_str[0:16])
        theta_str= decode_functions.invert_binary_if_negative(binary_str[16:32])

        out["RHO"]= str(int(rho_str,2)*(1.0/256))+" "+"NM"
        out["THETA"]= str(int(theta_str,2)*(360.0/2**16))+" "+"deg"

        return out
    


    @staticmethod
    def I062_340_HEI(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        hei_str= decode_functions.invert_binary_if_negative(binary_str)
        out["HEI"]= str(int(hei_str,2)*25)+" "+"feet"
        return out
    


    @staticmethod
    def I062_340_MDC(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])
        
        out["V"]= "Code validated" if int(binary_str[0]) == 0 else "Code not validated"
        out["V"]= decode_functions.des2val_des(out["V"], ["Code validated","Code not validated"])
        out["G"]= "Default" if int(binary_str[1]) == 0 else "Garbled code"
        out["G"]= decode_functions.des2val_des(out["G"], ["Default","Garbled code"])

        lmmc_str= binary_str[2]
        out["Last Measured Mode C Code"]= str(int(lmmc_str,2)*0.25) + " "+"FL"

        return out
    

    @staticmethod
    def I062_340_MDA(b_data):
        out= dict()

        binary_str= "".join([format(b, '08b') for b in b_data])

        out["V"]= "Code validated" if int(binary_str[0]) == 0 else "Code not validated"
        out["V"]= decode_functions.des2val_des(out["V"], ["Code validated","Code not validated"])
        out["G"]= "Default" if int(binary_str[1]) == 0 else "Garbled code"
        out["G"]= decode_functions.des2val_des(out["G"], ["Default","Garbled code"])
        l_list= ["MODE 3/A code as derived from the reply of the transponder", "Smoothed MODE 3/A code as provided by a sensor local tracker"]
        out["L"]= l_list[int(binary_str[2])]
        out["L"]= decode_functions.des2val_des(out["L"], l_list)

        assert binary_str[3] == "0", "Reserved bit must be 0"

        out["Mode-3/A reply"]= oct(int(binary_str[4:],2))

        return out


    @staticmethod
    def I062_340_TYP(b_data):
        out= dict()
        binary_str= "".join([format(b, '08b') for b in b_data])

        typ_list= ["No detection", "Single PSR detection", "Single SSR detection", "SSR + PSR detection", 
 "Single ModeS All-Call", "Single ModeS Roll-Call", "ModeS All-Call + PSR", "ModeS Roll-Call + PSR"]
        out["TYP"]= typ_list[int(binary_str[:3],2)]
        out["TYP"]= decode_functions.des2val_des(out["TYP"], typ_list)

        sim_list= ["Actual target report", "Simulated target report"]
        out["SIM"]= sim_list[int(binary_str[3])]
        out["SIM"]= decode_functions.des2val_des(out["SIM"], sim_list)

        rab_list= ["Report from target transponder", "Report from field monitor (fixed transponder)"]
        out["RAB"]= rab_list[int(binary_str[4])]
        out["RAB"]= decode_functions.des2val_des(out["RAB"], rab_list)

        tst_list= ["Real target report", "Test target report"]
        out["TST"]= tst_list[int(binary_str[5])]
        out["TST"]= decode_functions.des2val_des(out["TST"], tst_list)

        if binary_str[6:] == "00":
            pass
        else:
            print("warning detect unexpected non-zero bit(s)")

        return out

