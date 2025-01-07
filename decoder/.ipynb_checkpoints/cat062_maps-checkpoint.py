fspec_mapping = {
    1: ["I062_010", 2],
    2: [None, 0],
    3: ["I062_015", 1],
    4: ["I062_070", 3],
    5: ["I062_105", 8],
    6: ["I062_100", 6],
    7: ["I062_185", 4],

    8: ["I062_210", 2],
    9: ["I062_060", 2],
    10: ["I062_245", 7],
    11: ["I062_380","1+"],
    12: ["I062_040", 2],
    13: ["I062_080", "1+"],
    14: ["I062_290", "1+"],

    15: ["I062_200", 1],
    16: ["I062_295", "1+"],
    17: ["I062_136", 2],
    18: ["I062_130", 2],
    19: ["I062_135", 2],
    20: ["I062_220", 2],
    21: ["I062_390", "1+"],

    22: ["I062_270", "1+"],
    23: ["I062_300", 1],
    24: ["I062_110", "1+"],
    25: ["I062_120", 2],
    26: ["I062_510", "3+"],
    27: ["I062_500", "1+"],
    28: ["I062_340", "1+"],

    29: [None, 0],
    30: [None, 0],
    31: [None, 0],
    32: [None, 0],
    33: [None, 0],
    34: ["RE", "1+"],
    35: ["SP", "1+"]
}



I062_380_mapping = {
    "(ADR)": 3,  # bit-32
    "(ID)": 6,  # bit-31
    "(MHG)": 2,  # bit-30
    "(IAS)": 2,  # bit-29
    "(TAS)": 2,  # bit-28
    "(SAL)": 2,  # bit-27
    "(FSS)": 2,  # bit-26
    "(FX) 1": None,  # bit-25
    "(TIS)": 1,  # bit-24
    "(TID)": 16,  # bit-23
    "(COM)": 2,  # bit-22
    "(SAB)": 2,  # bit-21
    "(ACS)": 7,  # bit-20
    "(BVR)": 2,  # bit-19
    "(GVR)": 2,  # bit-18
    "(FX) 2": None,  # bit-17
    "(RAN)": 2,  # bit-16
    "(TAR)": 2,  # bit-15
    "(TAN)": 2,  # bit-14
    "(GSP)": 2,  # bit-13
    "(VUN)": 1,  # bit-12
    "(MET)": 8,  # bit-11
    "(EMC)": 1,  # bit-10
    "(FX) 3": None,  # bit-9
    "(POS)": 6,  # bit-8
    "(GAL)": 2,  # bit-7
    "(PUN)": 1,  # bit-6
    "(MB)": 9,  # bit-5
    "(IAR)": 2,  # bit-4
    "(MAC)": 2,  # bit-3
    "(BPS)": 2,  # bit-2
    "(FX) 4": None  # bit-1
}




I062_080_mapping= {

    # 0
    "(MON)": ["Multisensor track", "Monosensor track"],  # bit-8
    "(SPI)": ["default value", "SPI present in the last report received from a sensor capable of decoding this data"],  # bit-7
    "Most Reliable Height (MRH)": ["Barometric altitude (Mode C) more reliable", "Geometric altitude more reliable"],  # bit-6
    "Source of calculated track altitude for I062/130 (SRC)": [
        "no source",
        "GNSS",
        "3D radar",
        "triangulation",
        "height from coverage",
        "speed look-up table",
        "default height",
        "multilateration",
    ],  # bits 5/3
    "(SRC)_copy1": None,
    "(SRC)_copy2": None,
    "(CNF)": ["Confirmed track", "Tentative track"],  # bit-2
    "(FX) 0": ["end of data item", "extension into first extent"],  # bit-1


    # 1
    "(SIM)": ["Actual track", "Simulated track"],  # bit-8
    "(TSE)": ["default value", "last message transmitted to the user for the track"],  # bit-7
    "(TSB)": ["default value", "first message transmitted to the user for the track"],  # bit-6
    "(FPC)": ["Not flight-plan correlated", "Flight plan correlated"],  # bit-5
    "(AFF)": ["default value", "ADS-B data inconsistent with other surveillance information"],  # bit-4
    "(STP)": ["default value", "Slave Track Promotion"],  # bit-3
    "(KOS)": ["Complementary service used", "Background service used"],  # bit-2
    "(FX) 1": ["End of data item", "Extension into next extent"],  # bit-1
    
    # 2
    "(AMA)": ["track not resulting from amalgamation process", "track resulting from amalgamation process"],  # bit-8
    "(MD4)": ["No Mode 4 interrogation", "Friendly target", "Unknown target", "No reply"],  # bits 7/6
    "(MD4)_copy1": ["No Mode 4 interrogation", "Friendly target", "Unknown target", "No reply"],  # bits 7/6
    "(ME)": ["default value", "Military Emergency present in the last report received from a sensor capable of decoding this data"],  # bit-5
    "(MI)": ["default value", "Military Identification present in the last report received from a sensor capable of decoding this data"],  # bit-4
    "(MD5)": ["No Mode 5 interrogation", "Friendly target", "Unknown target", "No reply"],  # bits 3/2
    "(MD5)_copy1": ["No Mode 5 interrogation", "Friendly target", "Unknown target", "No reply"],  # bits 3/2
    "(FX) 2": ["End of data item", "Extension into next extent"],  # bit-1
    
    # 3
    "(CST)": ["Default value", "Age of the last received track update is higher than system dependent threshold (coasting)"],  # bit-8
    "(PSR)": ["Default value", "Age of the last received PSR track update is higher than system dependent threshold"],  # bit-7
    "(SSR)": ["Default value", "Age of the last received SSR track update is higher than system dependent threshold"],  # bit-6
    "(MDS)": ["Default value", "Age of the last received Mode S track update is higher than system dependent threshold"],  # bit-5
    "(ADS)": ["Default value", "Age of the last received ADS-B track update is higher than system dependent threshold"],  # bit-4
    "(SUC)": ["Default value", "Special Used Code (Mode A codes to be defined in the system to mark a track with special interest)"],  # bit-3
    "(AAC)": ["Default value", "Assigned Mode A Code Conflict (same discrete Mode A Code assigned to another track)"],  # bit-2
    "(FX) 3": ["End of data item", "Extension into next extent"],  # bit-1
    
    # 4
    "Surveillance Data Status  (SDS)": ["Combined", "Co-operative only", "Non-Cooperative only", "Not defined"],  # bits-8/7
    "Surveillance Data Status  (SDS)_copy1": ["Combined", "Co-operative only", "Non-Cooperative only", "Not defined"],  # bits-8/7
    "Emergency Status Indication (EMS)": ["No emergency", "General emergency", "Lifeguard / medical", "Minimum fuel", "No communications", "Unlawful interference", "“Downed” Aircraft", "Undefined"],  # bits-6/4
    "Emergency Status Indication (EMS)_copy1": ["No emergency", "General emergency", "Lifeguard / medical", "Minimum fuel", "No communications", "Unlawful interference", "“Downed” Aircraft", "Undefined"],  # bits-6/4
    "Emergency Status Indication (EMS)_copy2": ["No emergency", "General emergency", "Lifeguard / medical", "Minimum fuel", "No communications", "Unlawful interference", "“Downed” Aircraft", "Undefined"],  # bits-6/4
    "(PFT)": ["No indication", "Potential False Track Indication"],  # bit-3
    "(FPLT)": ["Default value", "Track created / updated with FPL data"],  # bit-2
    "(FX) 4": ["End of data item", "Extension into next extent"],  # bit-1


    # 5
    "(DUPT)": ["Default value", "Duplicate Mode 3/A Code"],  # bit-8
    "(DUPF)": ["Default value", "Duplicate Flight Plan"],  # bit-7
    "(DUPM)": ["Default value", "Duplicate Flight Plan due to manual correlation"],  # bit-6
    "(SFC)": ["Default value", "Surface target"],  # bit-5
    "(IDD)": ["No indication", "Duplicate Flight-ID"],  # bit-4
    "(IEC)": ["Default value", "Inconsistent Emergency Code"],  # bit-3
    "(FX) 5": ["Spare bit, set to 0", "End of data item", "Extension into next extent"],  # bit-1

}





I062_290_mapping= {
    "(TRK)": 1,
    "(PSR)": 1,
    "(SSR)": 1,
    "(MDS)": 1,
    "(ADS)": 2,
    "(ES)": 1,
    "(VDL)": 1,
    "(FX) 1": None,
    "(UAT)": 1,
    "(LOP)": 1,
    "(MLT)": 1,
}


I062_200_mapping = {
    "Transversal Acceleration (TRANS)": [
        "Constant Course",   # 00
        "Right Turn",        # 01
        "Left Turn",         # 10
        "Undetermined"       # 11
    ],
    "Longitudinal Acceleration (LONG)": [
        "Constant Groundspeed",    # 00
        "Increasing Groundspeed",  # 01
        "Decreasing Groundspeed",  # 10
        "Undetermined"             # 11
    ],
    "Vertical Rate (VERT)": [
        "Level",      # 00
        "Climb",      # 01
        "Descent",    # 10
        "Undetermined"  # 11
    ],
    "Altitude Discrepancy Flag (ADF)": [
        "No altitude discrepancy",  # 0
        "Altitude discrepancy"      # 1
    ],
    "Spare bit": [
        "Set to zero"  # 0
    ]
}




I062_295_mapping= {
    "(MFL)": 1,
    "(MD1)": 1,
    "(MD2)": 1,
    "(MDA)": 1,
    "(MD4)": 1,
    "(MD5)": 1,
    "(MHG)": 1,
    "(FX) 1": None,
    "(IAS)": 1,
    "(TAS)": 1,
    "(SAL)": 1,
    "(FSS)": 1,
    "(TID)": 1,
    "(COM)": 1,
    "(SAB)": 1,
    "(FX) 2": None,
    "(ACS)": 1,
    "(BVR)": 1,
    "(GVR)": 1,
    "(RAN)": 1,
    "(TAR)": 1,
    "(TAN)": 1,
    "(GSP)": 1,
    "(FX) 3": None,
    "(VUN)": 1,
    "(MET)": 1,
    "(EMC)": 1,
    "(POS)": 1,
    "(GAL)": 1,
    "(PUN)": 1,
    "(MB)": 1,
    "(FX) 4": None,
    "(IAR)": 1,
    "(MAC)": 1,
    "(BPS)": 1
}




I062_390_mapping= {
    "(TAG)": 2,
    "(CSN)": 7,
    "(IFI)": 4,
    "(FCT)": 1,
    "(TAC)": 4,
    "(WTC)": 1,
    "(DEP)": 4,
    "(FX) 1": None,
    "(DST)": 4,
    "(RDS)": 3,
    "(CFL)": 2,
    "(CTL)": 2,
    "(TOD)": "5"+"rep"+"4",
    "(AST)": 6,
    "(STS)": 1,
    "(FX) 2": None,
    "(STD)": 7,
    "(STA)": 7,
    "(PEM)": 2,
    "(PEC)": 7
}




I062_270_list= [
    "LENGTH",
    "ORIENTATION",
    "WIDTH"
]



I062_110_mapping= {
    "(SUM)": 1,
    "(PMN)": 4,
    "(POS)": 6,
    "(GA)": 2,
    "(EM1)": 2,
    "(TOS)": 1,
    "(XP)": 1,
    "(FX) 1": 1
}








I062_500_mapping = {
    "(APC)": 4,
    "(COV)": 2,
    "(APW)": 4,
    "(AGA)": 1,
    "(ABA)": 1,
    "(ATV)": 2,
    "(AA)": 2,
    "(FX) 1": None,

    "(ARC)": 1
}





I062_340_mapping = {
    "(SID)": 2,
    "(POS)": 4,
    "(HEI)": 2,
    "(MDC)": 2,
    "(MDA)": 2,
    "(TYP)": 1,
    "(spare)": None,
    "(FX) 1": None,
}


