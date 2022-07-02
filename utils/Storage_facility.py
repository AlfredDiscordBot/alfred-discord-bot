import pickle
import os

class Variables:
    def __init__(self, filename):        
        self.filename = filename+".dat"
        self.data = {}
        if self.filename in os.listdir():
            with open(self.filename, mode = 'rb') as file:
                self.data = pickle.load(file)
        else:
            with open(self.filename, mode = 'wb') as file:
                pickle.dump(self.data, file)

    def edit(self, **variables):
        for i in variables:
            self.data[i] = variables[i]
        return True

    def pass_all(self, **variables):
        self.data = variables
        return True

    def save(self):
        with open(self.filename, mode = 'wb') as file:
            pickle.dump(self.data, file)
            return True

    def show_data(self):
        return self.data

    def show_all_variables(self):
        return list(self.data.keys())

    

