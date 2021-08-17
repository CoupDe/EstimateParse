import datetime as dt
import json
import shutil
from pathlib import Path
import pandas as pd
from pandas.io.json import json_normalize
from pydantic import BaseModel
import numpy as np
from Parse import EstimateABC

desktop_path = Path('~/Desktop').expanduser() / "Estimates" / dt.date.today().strftime("%d-%m-%y")
print(desktop_path)
Path.mkdir(desktop_path, exist_ok=True)


class EstimateModel(BaseModel):
    local_num: str
    workdoc_code: str
    type_work: str
    total_price: tuple[float, str]
    construction_object: str
    price_year: str
    inventory_num: str
    date_parse: str
    estimate_path: dict
    id_estimate: int
    new_path: str = None


class EstimateExport:

    @staticmethod
    def export_json(estimate_path, obj):
        es = EstimateModel(**obj.__dict__)
        es.new_path = estimate_path / obj.estimate_path["read_file_path"].name
        json_file = Path(estimate_path / (es.estimate_path["machine_num"] + ".json"))
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json.loads(es.json()), f, indent=4, ensure_ascii=False)

    @staticmethod
    def get_path(obj):
        fp = Path(obj.estimate_path["folder_path"]).glob("*.*")
        estimate_path = desktop_path / (obj.local_num + "_" +
                                        obj.estimate_path["machine_num"])
        EstimateABC.set_date_parse(obj, dt.date.today().strftime("%d-%m-%y"))
        if Path.exists(estimate_path):  # Если существует присвоить дату
            estimate_path = estimate_path.parent / Path(estimate_path.name + "_" +
                                                        str(dt.date.today().strftime("%d-%m-%y")))
            print(estimate_path, type(estimate_path))
            try:
                Path.mkdir(estimate_path)
            except FileExistsError:
                print(f"Существует несколько копий папок со сметой: {obj.local_num}")
        else:
            Path.mkdir(estimate_path)
        [shutil.copy(s, estimate_path) for s in fp]
        EstimateExport.export_json(estimate_path, obj)


class ImportEstimate:

    @staticmethod
    def read_json(path):
        return [z for z in list(Path(path).glob("**/*.json"))]

    # @staticmethod
    # def import_json(file):
    #     with open(file, "r", encoding="utf-8") as f:
    #         data = json.load(f)     # Загрузка JSON
    #         estimate = EstimateModel(**data)  # Создание модели pydantic
    #         print(type(estimate), estimate)
    #         estimates = pd.DataFrame(estimate)
    #         # print(estimates)
    #     # return estimate

    @staticmethod
    def import_json(file):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)  # Загрузка JSON
            # estimate = EstimateModel(**data)  # Создание модели pydantic
            # print(type(estimate), estimate)
            estimate = pd.json_normalize(data)
        return estimate

    @staticmethod
    def make_hyperlink(x, y):
        return '=HYPERLINK("%s", "%s")' % (x, y)

    @staticmethod  # Объединение сметв в один datafraame
    def create_df(df):
        estimates = pd.concat(df)
        estimates.reset_index(drop=True, inplace=True)
        print(estimates["new_path"])
        estimates.rename(columns={"id_estimate": "id"}, inplace=True)
        estimates["local_num"] = estimates.apply(lambda x: ImportEstimate.make_hyperlink(x["new_path"], x["local_num"]),
                                                 axis=1)  # Создать гиперссылку
        estimates.style.set_properties(**{'background-color': 'yellow'})
        estimates.style.applymap(lambda x: "background-color: red" if x != "" else "background-color: white")
        print(estimates.new_path)
        estimates.to_excel("x.xlsx", engine='openpyxl')
