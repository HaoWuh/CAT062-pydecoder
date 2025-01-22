class Reader:
    def __init__(self, filename):
        """initialize the reader

        Args:
            filename (_type_): name of the file
        """
        self.filename = filename
        self.data = None   # data
        self.preprocessed_data= None    # preprocessed_data


class Raw_Reader(Reader):
    def __init__(self, filename, preprocess= True):
        """initialize the reader

        Args:
            filename (_type_): name of the file
            preprocess (bool, optional): Defaults to True.
        """
        super().__init__(filename)
        if filename is not None:
            self.data= self._raw2data()
            if preprocess:
                self.preprocessed_data= self.preprocess(self.data)
        else:
            # for asterix processing part
            # It is not needed at present
            pass
            
    def import_data(self, data, preprocess= True):
        """import data into the reader

        Args:
            data (_type_): list
            preprocess (bool, optional):  Defaults to True.
        """
        self.data= data
    
        if preprocess:
            self.preprocessed_data= self.preprocess(self.data)

        
    def _raw2data(self):
        if not (self.filename.endswith("raw")):
            print("Not .raw file!")
            return None
        with open(self.filename, "rb") as f:
            data = f.read()
            hex_list = [(int(byte)) for byte in data]
            return hex_list
    
#     need import asterix package to using the following functions

#     def _raw2asterix(self):
#         if not (self.filename.endswith("raw")):
#             print("Not .raw file!")
#             return None
        
#         with open(self.filename, "rb") as f:
#             data = f.read()
#             # Parse data description=True
#             if self.detailed:
#                 print('Items with description')
#                 print('----------------------')
                
#             parsed = asterix.parse(data)
#             if self.detailed:
#                 for packet in parsed:
#                     for item in packet.items():
#                         print(item)
#                 print('Items without description')
#                 print('----------------------')
#             # Parse data description=False
#             parsed = asterix.parse(data, verbose=False)
#             if self.detailed:
#                 for packet in parsed:
#                     for item in packet.items():
#                         print(item)
#                 print('Textual description of data')
#                 print('----------------------')
#             # describe Asterix data
#             formatted = asterix.describe(parsed)
#             # print(formatted)
#             return formatted
        
#     def _data2asterix(self):
#         if self.detailed:
#             print('Items with description')
#             print('----------------------')

#         parsed = asterix.parse(self.data)
#         if self.detailed:
#             for packet in parsed:
#                 for item in packet.items():
#                     print(item)
#             print('Items without description')
#             print('----------------------')
#         parsed = asterix.parse(self.data, verbose=False)
#         if self.detailed:
#             for packet in parsed:
#                 for item in packet.items():
#                     print(item)
#             print('Textual description of data')
#             print('----------------------')
#         return parsed
#         # formatted = asterix.describe(parsed)
#         # return formatted
        
    @staticmethod
    def preprocess(data):
        """preprocess data

        Args:
            data (_type_): data to be preprocessed

        Returns:
            _type_: preprocessed data
        """

        assert isinstance(data, list), "Data must be a list"
        
        data_list= []

        
        i = 0
        while i < len(data):
            byte= data[i]
            if byte == 62:           
                temp_len= (data[i+1] << 8)+int(data[i+2])
                data_list.append(data[i:i+temp_len])
                i+= temp_len
                
            else:
                i+= 1

                      
        return data_list


if __name__ == '__main__':

    # Read example file from packet resources
    sample_filename = "../data/binary.raw"
    print(sample_filename)
    raw_reader= Raw_Reader(sample_filename)
    raw_data= raw_reader.data
    preprocessed_data= raw_reader.preprocessed_data
    print(len(raw_data))
    print(len(preprocessed_data))
    
    