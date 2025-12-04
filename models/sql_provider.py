import os
import glob

class SQLProvider:
    """
    Загружает .sql-файлы из указанной папки в словарь {имя_файла: текст_sql}.
    Шаблон SQL — это файл с плейсхолдерами вида %(param)s для безопасной
    подстановки через параметризацию DB-API.
    """

    def __init__(self, folder: str):
        self.folder = folder
        self.sql: dict[str, str] = {}
        self._init()

    def _init(self):
        for path in glob.glob(os.path.join(self.folder, '*.sql')):
            name = os.path.splitext(os.path.basename(path))[0]
            with open(path, 'r', encoding='utf-8') as f:  # ✅ теперь внутри цикла
                self.sql[name] = f.read()

    def get(self, name: str) -> str | None:
        return self.sql.get(name)
