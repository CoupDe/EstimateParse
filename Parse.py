from pathlib import Path
import pandas as pd
import json

desktop_path = Path('~/Desktop').expanduser()
print(desktop_path)


class EstimateParser:
    """This is class parse estimate from program ABC, Bagira"""
    estimate_count = 0
    all_instances = []

    def __init__(self, full_path, folder_name, file_name, program_file):
        self.full_path = full_path
        self.folder_name = folder_name
        self.file_name = file_name
        self.program_file = program_file
        self.all_instances.append(self)
        EstimateParser.estimate_count += 1

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
        pack = []
        for i in read_file:
            x = EstimateParser.get_program_name(i[0])
            # Get all abc file in folder with readfile
            s = [z for z in list(Path(i[0].parent).glob("**/*.abc")) if x in str(z)]
            if not s:
                pack.append((i[0], i[1], None))
            else:
                pack.append((i[0], i[1], s[0]))
        return pack

    """Получение имени программного файла"""

    @classmethod
    def get_program_name(cls, name):
        file_name = name.stem[1:len(name.stem) - 1] + "3"
        return file_name

    """Проверка комплектности редактируемых файлов и программных файлов"""

    @classmethod
    def count_pack(cls):
        for instance in cls.all_instances:
            if instance.program_file is None:
                print(f"Program file is not found in folder {instance.folder_name}")
        print(f"Total editable estimates found: {len(cls.all_instances)}")


class ParseFile(EstimateParser):

    def get_rows(self):
        rows = []
        file = str(self.full_path)  # Почему приходится распаковывать Dataframe из List
        # Skiprows с методом range применяется для отсечения не нужных данных для сбора данных
        # !!!Как понять количество строк в файле???
        df = pd.read_html(file, skiprows=range(17, 10000), thousands="True")[0].dropna(axis='index', how='all')
        for s in df.index.tolist():  # """ !!! Почему я не могу указать self.get_indicators(
            rows.append(ParseFile.get_pure_row(df.loc[s]))  # хотя метод находится в кл, насколько вообще правильно
        return rows  # спользовать метод класса в классе.

    @staticmethod
    def get_pure_row(df):
        return sorted(list(set(df.dropna())))

    def get_indicators(self, row):
        pass
        # if switcher.items():
        #     return switcher.get(str(row), "invalid")


class Estimate(EstimateParser):
    construction_object = ""
    local_num = ""
    type_work = ""
    workdoc_code = ""
    total_price = ""
    inventory_num = ""

    def set_local_num(self, arg):
        self.local_num = arg.lower().split("ин")[0]
        if len(arg.lower().split("ин")) > 1:
            self.inventory_num = "ин" + arg.lower().split("ин")[1]

    def to_json(self):
        json.dumps(self.__dict__)

    switcher = {"локальн": set_local_num,               # !!!Почему я могу использовать вызов функции без аргумента??
                "основ": 1
                }

    @classmethod
    def search_data(cls, dt):
        for outer in dt:
            for inner in enumerate(outer):
                for switch in cls.switcher.keys():
                    if switch in inner[1].lower():
                        cls.switcher[switch](cls, outer[0])
                        print([outer[0]])
        pass


anotherPath = r"C:\Users\Вадим\Desktop\Estimate\Сметы\00.АС\Копия s955096311.xlsx"
estimatePath = r"C:\Users\Вадим\Desktop\Estimate\Сметы"
# ABC expansion
rf = EstimateParser.get_read_file(estimatePath)
pf = EstimateParser.get_program_file(rf)
# ep = [EstimateParser(full_path, folder_name, file_name, program_file) for full_path, folder_name, file_name,
# program_file in pf[x, y, z]]
for x, y, z in pf:
    EstimateParser(x, x.parent, x, z)
EstimateParser.count_pack()
pe = ParseFile

rows = pe.get_rows(EstimateParser.all_instances[1])
print(rows)
es = Estimate
es.search_data(rows)
