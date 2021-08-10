import datetime as dt
from pathlib import Path
import shutil

from Parse import Estimate, EstimateABC

desktop_path = Path('~/Desktop').expanduser() / "Estimates"
print(desktop_path)
Path.mkdir(desktop_path, exist_ok=True)


class EstimateExport:

    @staticmethod
    def get_path(obj):
        fp = Path(obj.estimate_path["folder_path"]).glob("*.*")
        estimate_path = desktop_path / (obj.local_num + "_" +
                                        EstimateABC.get_program_name(obj.estimate_path["read_file_path"]))
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
        EstimateABC.set_date_parse(obj, dt.date.today().strftime("%d-%m-%y"))
