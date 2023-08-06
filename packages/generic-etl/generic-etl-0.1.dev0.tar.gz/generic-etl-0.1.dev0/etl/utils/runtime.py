import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

class Runtime:
    source_data: dict = {}
    target_data: dict = {}
    source: Union[str, Path] = ""
    target: Optional[Union[str, Path]] = None

    def __init__(self, source: str, target: Optional[str] = None):
        """Init function"""
        self.source = Path(source)
        self.target = target
        self.source_data = {}
        self.target_data = {}

    def __enter__(self):
        """Entry context, loads the file"""

        if self.source.exists():
            with open(self.source, "r") as source_file:
                self.source_data = json.load(source_file)

        if not self.target and self.source:
            self.target = self.source
        
        if not self.target:
            today = datetime.today()
            file_name = f"{today.day}-{today.month}-{today.hour}-{today.minute}-{today.second}.json"
            self.target = Path(f"{self.source.parent}/{file_name}")

        return self

    def __exit__(self, type, value, traceback) -> None:
        """Exit context, saves target_data"""

        with open(self.target, "w") as target_file:
            json.dump(self.target_data, target_file, indent=4)
