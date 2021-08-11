import datetime as dt
import json
import shutil
from pathlib import Path

from pydantic import BaseModel

from Parse import EstimateABC

desktop_path = Path('~/Desktop').expanduser() / "Estimates" / dt.date.today().strftime("%d-%m-%y")
print(desktop_path)
Path.mkdir(desktop_path, exist_ok=True)


class EstimateModel(BaseModel):
    id_estimate: int
    local_num: str
    workdoc_code: str
    type_work: str
    total_price: tuple[float, str]
    construction_object: str
    price_year: str
    inventory_num: str
    date_parse: str
    estimate_path: dict


class EstimateExport:

    @staticmethod
    def export_json(estimate_path, obj):
        es = EstimateModel(**obj.__dict__)
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

    @staticmethod
    def import_json(file):
        s = json.load(file)
        estimate = EstimateModel(**s)
        print(type(estimate))
        return estimate
