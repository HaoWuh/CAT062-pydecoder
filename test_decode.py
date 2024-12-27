from  decoder.decode import byte_decoder


BD= byte_decoder()
# print(BD.process_byte_data())
BD.process_byte_data()
BD.save2json()