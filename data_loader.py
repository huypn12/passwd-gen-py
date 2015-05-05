import json


class DataLoader(object):
    def __init__(self):
        self.metadata_file  = 'data/metadata.json'
        self.structure_file = 'data/structure.json'
        self.metadata       = None
        self.structure      = {}
        self.acc_list       = []

    def load_structure(self):
        with open(self.structure_file) as structure_file:
            structure_content = json.load(structure_file)
        self.structure = structure_content

    def load_metadata(self):
        with open(self.metadata_file) as metadata_file:
            metadata = json.load(metadata_file)
        self.metadata = metadata

    def load_acc(self):
        for entry in self.metadata:
            data_file = "data/" + entry['file']
            with open(data_file) as data_file:
                entry_data = json.load(data_file)
                entry_data['name'] = entry['account']
                self.acc_list.append(entry_data)

    def get_acc(self, acc_name):
        for acc in self.acc_list:
            if acc['name'] == acc_name:
                return acc

    def load(self):
        self.load_structure()
        self.load_metadata()
        self.load_acc()


if __name__ == '__main__':
    data_loader = DataLoader()
    data_loader.load()
    print data_loader.get_acc("la_hoang")

