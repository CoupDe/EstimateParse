from pathlib import Path
import pandas as pd
import json

desktop_path = Path('~/Desktop').expanduser()
print(desktop_path)

"""This is class parse estimate from program ABC, Bagira"""


class Estimate:
    estimate_count = 0
    all_instances = []

    def __init__(self, readfile, type):
        self.estimate_path = {"folder_path": readfile.parent,
                              "read_file_path": readfile,
                              "estimate_type": type,
                              "program_file": self.get_program_file(readfile)}

        self.all_instances.append(self)
        self.__class__.estimate_count += 1

    pass

    def get_path_estimate(self):
        pass

    #  Наверно правильнее создавать не каждый экземпляр с параметрами, а один экземпляр со списками под каждое поле
    # def __init__(self, full_path, folder_name, file_name, program_file, **estimate_path):
    #     self.full_path = full_path
    #     self.folder_name = folder_name 111
    #     self.file_name = file_name 11
    #     self.program_file = program_file

    @staticmethod  # Get reading file
    def get_read_file(path):
        #  Скорее всего правильнее вынести переменную abc_exp на уровень класса создать свойство класса
        abc_exp = {"abc": ("**/s*.htm*", "**/s*.xl*"), "smt": ("**/*.smt",)}  # No example *smt* to process
        abc_gen = [(Path(path).glob(s), k) for k, v in abc_exp.items() for s in v if s != ""]
        # !!!Разобраться как изменить 2ю переменную в кортеже при использовании генератора
        readfile = list(((x, y[1]) for y in abc_gen for x in y[0]))  # Unpacking generators with editable file formats
        return readfile

    @staticmethod
    def get_program_file(read_file):
        pass

    """Получение имени программного файла"""

    @classmethod
    def get_program_name(cls, name):
        file_name = name.stem[1:len(name.stem) - 1] + "3"
        return file_name

    """Проверка комплектности редактируемых файлов и программных файлов"""

    @classmethod
    def count_pack(cls):
        for instance in cls.all_instances:
            if instance.estimate_path["program_file"] is None:
                print(f"Program file is not found in folder {instance.estimate_path['read_file_path']}")
        print(f"Total editable estimates found: {len(cls.all_instances)}")


class EstimateABC(Estimate):
    construction_object = None
    local_num = None
    type_work = None
    workdoc_code = None
    total_price = (0, "")
    inventory_num = None
    price_year = 0
    all_instances_estimate = []

    def __init__(self, rd):
        super().__init__(rd, "abc")  # Этот класс вызывается в 1-ю очередь и из него формируется родитель, можно ли
        # указать в конструкторе базового класса, что если я передаю аргумент от дочернего класса присвоить тив "abc"
        self.price_year = Estimate.estimate_count  # Почему не передаются данные из базового класса

    """Получение очишеных от nan строк с помощью Pandas \\ Обрабатывается 2 формата html и Excel"""

    def get_rows(self):
        rows = []
        file = str(self.estimate_path["read_file_path"])  # Почему приходится распаковывать Dataframe из List
        # Skiprows с методом range применяется для отсечения не нужных данных для сбора данных
        # !!!Как понять количество строк в файле???
        # if "xls" in file:
        #     df = pd.read_excel(file, nrows=17, thousands="True")
        # else:
        try:
            df = pd.read_html(file, skiprows=range(17, 10000), thousands="True")[0].dropna(axis='index', how='all')
        except ImportError:
            df = pd.read_excel(file, nrows=17, thousands="True")
        print(df)

        for s in df.index.tolist():  # """ !!! Почему я не могу указать self.get_indicators(
            rows.append(self.get_pure_row(df.loc[s]))  # хотя метод находится в кл, насколько вообще правильно
        return rows, Estimate.all_instances[1]  # спользовать метод класса в классе.

    @staticmethod
    def get_pure_row(df):
        return sorted(list(set(df.dropna())))

    def set_local_num(self, arg):
        if "(" and ")" not in arg[0]:
            self.local_num = arg[0].lower().split("ин")[0]
            if len(arg[0].lower().split("ин")) > 1:
                self.inventory_num = "ин" + arg[0].lower().split("ин")[1]

    def set_workdoc_code(self, arg):
        self.workdoc_code = arg[0]

    def set_total_price(self, arg):
        if "N" not in arg[0]:
            self.total_price = float(arg[0].replace(",", ".")), arg[2]

    def set_price_year(self, arg):
        self.price_year = arg[0]

    def set_type_work(self, arg):
        self.type_work = arg

    def set_construction_object(self, arg):
        self.construction_object = arg

    def to_json(self):
        json.dumps(self.__dict__)

    switcher = {"локальн": set_local_num,  # !!!Почему я могу использовать вызов функции без аргумента??
                "основ": set_workdoc_code,
                "стоим": set_total_price,
                "цена": set_price_year
                }

    @classmethod
    def get_program_file(cls, readfile):
        pack = []
        x = cls.get_program_name(readfile)
        # Get all abc file in folder with readfile
        s = [z for z in list(Path(readfile.parent).glob("**/*.abc")) if x in str(z)]
        if not s:
            return None
        else:
            return s[0]

    @classmethod
    def get_program_name(cls, name):
        return name.stem[1:len(name.stem) - 1] + "3"

    @classmethod
    def search_data(cls, dt):
        lrow = dt[0]
        for outer in lrow:
            for inner in enumerate(outer):
                for switch in cls.switcher.keys():
                    if switch in inner[1].lower():
                        cls.switcher[switch](cls, outer)  # Почему pycharm выдаёт тут замечание? Неопредлена функция?
                        print([outer[0]])
        if "наименов" in lrow[2][0]:
            cls.set_construction_object(cls, lrow[1][0])
        if "на" == lrow[5][1]:
            cls.set_type_work(cls, lrow[5][0])
        return cls, dt[1]
