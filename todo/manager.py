from pathlib import Path
from datetime import datetime
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print
from todo.selector import Selector
import curses
import yaml

class ToDoManager:
    def __init__(self):
        self.path = Path.home() / "Documents" / "todo"
        self.config_path = Path.home() / ".config" / "todomanager"
        self.config_file = self.config_path / "config.yaml"
        self.date_format = "%Y-%m-%d"
        self.today = datetime.now().strftime(self.date_format)
        self.daylog_file = self.path / f"{self.today}.yaml"
        self.daylog_data = dict()

        if not self.path.is_dir or not self.daylog_file.exists():
            self.path.mkdir(exist_ok=1)

        if not self.config_path.is_dir or not self.config_file.exists():
            self.config_path.mkdir(exist_ok=1)
            self.config_file.touch(exist_ok=1)
            self._write_config()

        self._init_daylog()
        self._import_config()
        self._load_daylog()

    def _write_config(self):
        with open(self.config_file, "w") as f:
            f.write(yaml.dump({
                "daylog_file": str(self.daylog_file)
            }))

    def _import_config(self):
        if self.config_file.exists():
            with open(self.config_file) as f:
                config = yaml.safe_load(f)
                self.daylog_file = config["daylog_file"]

    def _init_daylog(self):
        if not self.daylog_file.exists():
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
        "Add a new task to the to-do list."
        
        self.daylog_data["tasks"].append({"status": False, "title": title})
        self._write_daylog()

    def check(self, items):
        "Check the item"
        
        if type(items) == tuple:
            for idx in items:
                self.daylog_data["tasks"][idx]["status"] = not self.daylog_data["tasks"][idx]["status"]
        else:
            idx = items
            self.daylog_data["tasks"][idx]["status"] = not self.daylog_data["tasks"][idx]["status"]
        self._write_daylog()

    def delete(self, items):
        "Delete the item"
        
        if type(items) == tuple:
            for idx in items:
                del self.daylog_data["tasks"][idx]
        else:
            idx = items
            del self.daylog_data["tasks"][idx]
        self._write_daylog()

    def list(self):
        "List all the tasks for the current day"
        
        display_content = str()
        for idx, task in enumerate(self.daylog_data["tasks"]):
            display_content += f"[bold]{idx}. ({'[green]x[/]' if task['status'] else '[red]=[/]'})[/] {task['title']}\n"

        print(Panel.fit(
                display_content,
                title=f"[bold yelllow]{self.daylog_data['date']}[/]",
                padding=(1, 5)
            ))

    def rename(self, item: int, name: str):
        "Rename the task title"

        self.daylog_data["tasks"][item]["title"] = name
        self._write_daylog()

    def select(self, identifier: str = ""):
        "Select any daylog from the journal"
        match identifier.lower():
            case "today":
                self.daylog_file = self.path / f"{self.today}.yaml"
            case "":
                self.daylog_file = Selector([f for f in self.path.iterdir()]).select()
                curses.endwin()
        self._write_config()
        print(f"[bold]Previously selected daylog was changed for:[bold] [red]{self.daylog_file.name}")

    def move(self, item: int, where: str = ""):
        "Move tasks between daylogs"
        destination_data = dict()
        destination_path = str()
        match where.lower():
            case "today":
                destination_path = self.path / f"{self.today}.yaml"
            case "":
                destination_path = self.path / Selector([f for f in self.path.iterdir()]).select()

        with open(destination_path, "r") as f:
            destination_data = yaml.safe_load(f)
            try:
                destination_data["tasks"].append(self.daylog_data["tasks"][item])
                self.delete(item)
            except IndexError:
                print("[bold red]You out of scope, specify existed items only")

        with open(destination_path, "w") as f:
            f.write(yaml.dump(destination_data))






