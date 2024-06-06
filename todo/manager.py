from pathlib import Path
from datetime import datetime
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print
import yaml

class ToDoManager:
    def __init__(self):
        self.path = Path.home() / "Documents" / "todo"
        self.date_format = "%Y-%m-%d"
        self.today = datetime.now().strftime(self.date_format)
        self.daylog_file = self.path / f"{self.today}.yaml"
        self.daylog_data = dict()
        self._init_daylog()

        if not self.path.is_dir:
            self.path.mkdir(exist_ok=1)

    def _init_daylog(self):
        if not self.daylog_file.exists():
            self.daylog_file.touch()
            with open(self.daylog_file, "w") as f:
                f.write(yaml.dump({
                    "date": self.today,
                    "tasks": [{"title": "wake up", "status": True}]
                }))
                print(f"Daylog {self.daylog_file.name} has been created")

    def _load_daylog(self):
        with open(self.daylog_file, "r") as f:
            self.daylog_data = yaml.safe_load(f)

    def _write_daylog(self):
        with open(self.daylog_file, "w") as f:
            f.write(yaml.dump(self.daylog_data))

    def add(self, title: str):
        self._load_daylog()
        self.daylog_data["tasks"].append({"status": False, "title": title})
        self._write_daylog()

    def check(self, items):
        self._load_daylog()
        if type(items) == tuple:
            for idx in items:
                self.daylog_data["tasks"][idx]["status"] = not self.daylog_data["tasks"][idx]["status"]
        else:
            idx = items
            self.daylog_data["tasks"][idx]["status"] = not self.daylog_data["tasks"][idx]["status"]
        self._write_daylog()

    def delete(self, items):
        self._load_daylog()
        if type(items) == tuple:
            for idx in items:
                del self.daylog_data["tasks"][idx]
        else:
            idx = items
            del self.daylog_data["tasks"][idx]
        self._write_daylog()

    def list(self):
        self._load_daylog()
        display_content = str()
        #print(f"\n\t[bold yelllow]{self.daylog_data['date']}[/]")
        for idx, task in enumerate(self.daylog_data["tasks"]):
            display_content += f"[bold]{idx}. ({'[green]x[/]' if task['status'] else '[red]=[/]'})[/] {task['title']}\n"

        print(Panel.fit(
                display_content,
                title=f"[bold yelllow]{self.daylog_data['date']}[/]",
                padding=(1, 5)
            ))

