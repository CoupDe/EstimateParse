import datetime as dt
from pathlib import Path
import shutil

desktop_path = Path('~/Desktop').expanduser() / "Estimates"
print(desktop_path)
Path.mkdir(desktop_path, exist_ok=True)


class EstimateExport:
    pass

    @staticmethod
    def get_path(obj):
        fp = Path(obj.estimate_path["folder_path"]).glob("*.*")
        Path.mkdir(desktop_path / obj.estimate_path[""], exist_ok=True)
        [shutil.copy(s, desktop_path) for s in fp]
        print(fp)
