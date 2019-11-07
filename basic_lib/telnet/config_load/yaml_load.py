


import yaml


class yml_load:
    def __init__(self, yml_data=None):
        if yml_data is None:
            yml_data = '''
                student1:
                    name: James
                    age: 20
                student2:
                    name: Lily
                    age: 19
                '''
        aproject = {'name': 'Silenthand Olleander',
                    'race': 'Human',
                    'traits': ['ONE_HAND', 'ONE_EYE']
                    }

        obj1 = {"name": "James", "age": 20}
        obj2 = ["Lily", 19]
        # self.load(yml_data)
        # self.dump(obj1, obj2)

    def load(self, f):
        y = yaml.load_all(f, Loader=yaml.FullLoader)
        for data in y:
            print('yml data:', data)
            return data

        # f = open(r'config.yml', 'w')
        # print(yaml.dump(aproject, f))

    def dump(self, obj1, obj2=None):
        with open(r'config.yml', 'w') as f:
            dump_data = yaml.dump_all([obj1, obj2], f)
            return dump_data


if __name__ == "__main__":
    pass
# yml_load()

# class Person(yaml.YAMLObject):
#     # yaml_tag = '!person'
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def __repr__(self):
#         return '%s(name=%s, age=%d)' % (self.__class__.__name__, self.name, self.age)
#
#
# james = Person('James', 20)
# yaml.dump(james)  # Python对象实例转为yaml
#
# ff = open('config.yml', 'r', encoding='utf-8')
#
# lily = yaml.load_all(ff.read(), Loader=yaml.FullLoader)
# print(lily)  # yaml转为Python对象实例