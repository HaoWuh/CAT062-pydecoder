import asterix


class Reader:
    def __init__(self, filename, detailed= False):
        self.filename = filename
        self.detailed= detailed
        self.data = None
        self.asterix= None


class Raw_Reader(Reader):
    def __init__(self, filename, detailed):
        super().__init__(filename, detailed)
        self.data= self._raw2data()
        self.asterix = self._raw2asterix()

        
    def _raw2data(self):
        if not (self.filename.endswith("raw")):
            print("Not .raw file!")
            return None
        
        with open(self.filename, "rb") as f:
            data = f.read()
            return data
    

    def _raw2asterix(self):
        if not (self.filename.endswith("raw")):
            print("Not .raw file!")
            return None
        
        with open(self.filename, "rb") as f:
            data = f.read()
            # Parse data description=True
            if self.detailed:
                print('Items with description')
                print('----------------------')
                
            parsed = asterix.parse(data)
            if self.detailed:
                for packet in parsed:
                    for item in packet.items():
                        print(item)
            if self.detailed:
                print('Items without description')
                print('----------------------')
            # Parse data description=False
            parsed = asterix.parse(data, verbose=False)
            if self.detailed:
                for packet in parsed:
                    for item in packet.items():
                        print(item)
            if self.detailed:
                print('Textual description of data')
                print('----------------------')
            # describe Asterix data
            formatted = asterix.describe(parsed)
            # print(formatted)
            return formatted


if __name__ == '__main__':

    # print(asterix.__version__)

    # Read example file from packet resources
    sample_filename = "../data/sample.raw"
    print(sample_filename)
    raw_reader= Raw_Reader(sample_filename, detailed= False)
    raw_data= raw_reader.data
    raw_asterix= raw_reader.asterix
    print(raw_data)