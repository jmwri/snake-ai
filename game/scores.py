import csv
import os


class ScoreLogger:
    def __init__(self, base_path: str):
        if not base_path.endswith('/'):
            base_path += '/'
        self._base_path = base_path

    def _path_for_file(self, file_name: str) -> str:
        return f'{self._base_path}{file_name}.csv'

    def log_score(self, file_name: str, score: int):
        path = self._path_for_file(file_name)
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, "a+") as fh:
            writer = csv.writer(fh)
            writer.writerow([score])
