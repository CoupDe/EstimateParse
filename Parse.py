from pathlib import Path
import pandas as pd

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
    full_price = None
    switcher = {"локальна": 11, "основан": 8, "метная": 11}


    def get_file(self):
        rows = []
        file = str(self.full_path)
        # Почему приходится распаковывать Dataframe из List
        # Skiprows с методом range применяется для отсечения не нужных данных для сбора данных
        # !!!Как понять количество строк в файле???
        df = pd.read_html(file, skiprows=range(30, 10000), thousands="True")[0].dropna(axis='index', how='all')
        df.to_csv("2.csv")
        for s in df.index.tolist():
            rows.append(ParseFile.get_pure_rows(self, df.loc[s]))
        print(rows)
        row = sorted(list(set(df.loc[12].dropna())))  # Delete rows with all val nan from pd.series
        for s in row:
            for p in ParseFile.switcher.keys():
                if p in str(s):
                    print(ParseFile.switcher[p])
            # !!! Почему я не могу указать self.get_indicators(f) хотя метод находится в
            # кл, насколько вообще правильно спользовать метод класса в классе.
        print(df.shape, row)
        df.to_csv("1.csv")
        values_list = df.values.tolist()
        # Как сделать перебор искомых ывражений
        local_num = [i[s[0] + 1] for i in values_list[:15] for s in enumerate(i) if "локальна" in str(s[1]).lower()]
        # df.to_excel('any.xlsx')
        local_num += [i[s[0] + 2] for i in values_list[:15] for s in enumerate(i) if "основан" in str(s[1]).lower()]
        local_num += [i[s[0] + 2] for i in values_list[7:9] for s in enumerate(i) if
                      "на" in str(s[1]).lower() and len(s) == 2]

    def get_pure_rows(self, df):
        return sorted(list(set(df.dropna())))

    def get_indicators(self, row):
        pass
        # if switcher.items():
        #     return switcher.get(str(row), "invalid")


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
pe.get_file(EstimateParser.all_instances[1])