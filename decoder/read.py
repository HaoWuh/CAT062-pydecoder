import asterix


class Reader:
    def __init__(self, filename):
        self.filename = filename
        self.data = None


class Raw_Reader(Reader):
    def __init__(self, filename):
        super().__init__(filename)
        self.data = self._raw2asterix()


    def _raw2asterix(self):
        if not (self.filename.endwith("raw")):
            print("Not .raw file!")
            return None
        
        with open(self.filename, "rb") as f:
            data = f.read()
            # Parse data description=True
            print('Items with description')
            print('----------------------')
            parsed = asterix.parse(data)
            for packet in parsed:
                for item in packet.items():
                    print(item)

            print('Items without description')
            print('----------------------')
            # Parse data description=False
            parsed = asterix.parse(data, verbose=False)
            for packet in parsed:
                for item in packet.items():
                    print(item)

            print('Textual description of data')
            print('----------------------')
            # describe Asterix data
            formatted = asterix.describe(parsed)
            # print(formatted)
            return formatted


if __name__ == '__main__':

    # print(asterix.__version__)

    # Read example file from packet resources
    sample_filename = asterix.get_sample_file('output.raw')
    raw_reader= Raw_Reader(sample_filename)
    raw_data= raw_reader.data
    print(raw_data)