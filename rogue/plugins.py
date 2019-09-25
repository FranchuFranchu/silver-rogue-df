import os
import yaml
from shutil import copyfile

class PluginFeature:

    def init_data(self):
        self.data = {}        
        def _data_recursive_function(currdir = 'data'):
            for i in self.listdir(currdir):
                if self.path_isfile(currdir + '/' + i) and i.endswith('.yml'):
                    datanode = (currdir + '/' + i.split('.yml')[0]).replace('/', '.')
                    f = self.get_file(currdir + '/' + i)
                    self.set_data(datanode, yaml.load(f))
                    f.close()
                elif self.path_exists(currdir + '/' + i):
                    _data_recursive_function(currdir + '/' + i)
        _data_recursive_function()

    def set_data(self, datanode, data):

        def _recursive(traversed_dict, datanode, data):
            l = datanode.split('.', 1)
            if len(l) == 1: # No dots in datanode
                traversed_dict[datanode] = data
                return

            if traversed_dict.get(l[0]) == None:
                traversed_dict[l[0]] = {}
            _recursive(traversed_dict[l[0]], l[1], data)

        _recursive(self.data, datanode, data)


    def generate_example_plugin(self):
        def try_to_create(loc):
            try:
                os.mkdir(self.saveLocation + loc)
                return True
            except FileExistsError:
                return False
        try_to_create('/plugins')
        try_to_create('/plugins/example')
        try_to_create('/plugins/example/resource')
        try_to_create('/plugins/example/resource/fonts')

        try:
            copyfile('../data/example_plugin/12x12_Alloy.png',  self.saveLocation + '/plugins/example/resource/fonts/12x12_Alloy.png')
        except FileExistsError:
            pass

    def list_plugins(self):
        if os.path.exists(self.saveLocation + '/plugins'):
            return os.listdir(self.saveLocation + '/plugins')
        return []

    def path_exists(self, path):
        # Like os.path.exists
        return self.path_check(path, os.path.exists)

    def path_isfile(self, path):
        # Like os.path.isfile
        return self.path_check(path, os.path.isfile)

    def path_check(self, path, func):
        # Func is a function like os.path.isfile or so
        for i in self.list_plugins():
            if func(self.saveLocation + '/plugins/' + i + '/' + path):
                return True
        for i in os.listdir('..'):
            if func('../' + path):
                return True

    def listdir(self, path):
        # Like os.listdir
        k = []
        for i in self.list_plugins():
            if os.path.isdir(self.saveLocation + '/plugins/' + i + '/' + path):
                k.extend(os.listdir(self.saveLocation + '/plugins/' + i + '/' + path))
        

        if os.path.isdir('../' + path):
            k.extend(os.listdir('../' + path))
        return list(set(k))
        
    def get_file(self, filename):
        for i in self.list_plugins():
            if os.path.isfile(self.saveLocation + '/plugins/' + i + '/' + filename):
                return open(self.saveLocation + '/plugins/' + i + '/' + filename)
        if os.path.isfile('../' + filename):
            return open('../' + filename)
    
    def data(self, datanode, currdir = '.'):
        raise NotImplementedError

    def _data_file_found(self, datanode, filed):
        raise NotImplementedError

