import hashlib
from pathlib import Path
import pandas as pd
import json


"""This is class parse estimate from program ABC, Bagira"""


class Estimate:
    id_estimate = ""
    estimate_count = 0
    all_instances = []

    def __init__(self, readfile, ext):
        self.estimate_path = {"folder_path": readfile.parent,
                              "read_file_path": readfile,
                              "estimate_type": ext,
                              "program_file": self.get_program_file(readfile)}
        self.id_estimate = str(hash(self.estimate_path["program_file"]))[1:7]
        self.all_instances.append(self)  # Почему я вижу список из инстансов в каждои инстансе, но при выводе
        # __dict__ я не вижу их в каждом инстансе
        self.__class__.estimate_count += 1

    def get_path_estimate(self):
        pass

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
        pass

    """Проверка комплектности редактируемых файлов и программных файлов"""

    @classmethod
    def count_pack(cls):
        for instance in cls.all_instances:
            if instance.estimate_path["program_file"] is None:
                print(f"Program file is not found in folder {instance.estimate_path['read_file_path']}")
        print(f"Total editable estimates found: {len(cls.all_instances)}")


class EstimateABC(Estimate):

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
        try:
            df = pd.read_html(file, skiprows=range(20, 10000), thousands="True")[0].dropna(axis='index', how='all')
        except ImportError:
            df = pd.read_excel(file, skiprows=range(20, 10000), thousands="True", header=None).dropna(axis='index',
                                                                                                      how='all')
        for s in df.index.tolist():  # """ !!! Почему я не могу указать self.get_indicators(
            rows.append(self.get_pure_row(df.loc[s]))  # хотя метод находится в кл, насколько вообще правильно
        self.row = rows  # Инстанс уже создан почему он предлагет его инициализисровать по новой?
        print(self.row)  # спользовать метод класса в классе. Результат прикрепляется к инстансу

    @staticmethod
    def get_pure_row(df):
        return sorted(list(set(df.dropna())))

    def set_local_num(self, arg):
        if "(" and ")" not in arg[0] or "взам" in arg[0].lower():
            self.local_num = arg[0].lower().split("ин")[0].strip()
            if len(arg[0].lower().split("ин")) > 1:
                self.inventory_num = "ин" + arg[0].lower().replace("\n", " ").split("ин", maxsplit=1)[1].strip()

    def set_workdoc_code(self, arg):
        self.workdoc_code = arg[0].strip()  # !!! Почему он предалагает перенести в конструктор, когда я не
        # инициализирую эти данные при создании экземпляра, а в процессе обработки

    def set_total_price(self, arg):
        if "N" not in arg[0]:
            self.total_price = float(arg[0].replace(",", ".").strip()), arg[2]

    def set_price_year(self, arg):
        self.price_year = arg[0].strip()

    def set_type_work(self, arg):
        self.type_work = arg.strip()

    def set_construction_object(self, arg):
        self.construction_object = arg.strip()

    def set_date_parse(self, arg):
        self.date_parse = arg.strip()

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

    def search_data(self):
        lrow = self.row
        for outer in lrow:
            for inner in enumerate(outer):
                for switch in self.switcher.keys():
                    if switch in inner[1].lower():
                        self.switcher[switch](self, outer)  # Почему pycharm выдаёт тут замечание? Неопредлена функция?
        if "наименов" in lrow[2]:
            self.set_construction_object(self, lrow[1])
        if "на" == lrow[5]:
            self.set_type_work(self, lrow[5])
        del self.row
