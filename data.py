import sys
import json

#TODO:  read account list from metadata file

class Data(object):
    def __init__(self):
        self.metadata_file = 'info/metadata.json'
        self.metadata = None
        self.data = []

    def load_metadata(self):
        with open(self.metadata_file) as metadata_file:
            metadata = json.load(metadata_file)
            return metadata

    def load_data(self):
        for entry in self.metadata:
            data_file = entry['file']
            with open(data_file) as data_file:
                entry_data = json.load(data_file)
                self.data.append(entry_data)
