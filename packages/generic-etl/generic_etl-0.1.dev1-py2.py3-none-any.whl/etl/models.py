from dataclasses import dataclass, fields
from typing import Dict, List, Optional, Union


@dataclass
class SubStep:
    title: str = None
    app: str = None
    io: str = None

    csv_one: str = None
    csv_two: str = None
    csv_out: str = None
    on: str = None

    def __str__(self):
        return f"{self.title} - {self.app} {self.io}"

    @classmethod
    def from_dict(cls, title: str, data: dict):
        class_fields = {f.name for f in fields(cls)}
        data["title"] = title
        return cls(**{k: v for k, v in data.items() if k in class_fields})


@dataclass
class Step:
    title: str = None
    file_name: Optional[str] = None
    odbc: Optional[str] = None
    sql: Optional[str] = None
    function: Optional[str] = None
    file: Optional[str] = None
    func_input: Optional[str] = None
    sub_steps: Optional[List[SubStep]] = None
    connection: Optional[str] = None
    target_connection: Optional[str] = None
    schema: Optional[str] = "public"
    target_tables: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, title: str, data: dict):
        class_fields = {f.name for f in fields(cls)}
        # retain order pls
        substeps_ = {k: [] for k in set(data.keys()) - class_fields}
        for key in substeps_:
            substeps_[key] = SubStep.from_dict(key, data[key])

        data["sub_steps"] = substeps_
        return cls(**{k: v for k, v in data.items() if k in class_fields})

    @classmethod
    def multples_from_dict(cls, title: str, data: dict):
        steps_ = []
        for step in data:
            steps_.extend([Step.from_dict(k, v) for k, v in step.items()])
        return steps_


@dataclass
class Pipeline:
    out_type: Optional[str] = None
    steps: Dict[str, List[Step]] = None

    @classmethod
    def from_dict(cls, data: dict):
        class_fields = {f.name for f in fields(cls)}
        # retain order pls
        ks = set(data.keys()) - class_fields
        steps_ = {k: [] for k in ks}
        for key in steps_:
            steps_[key] = Step.multples_from_dict(key, data[key])

        data["steps"] = steps_
        return cls(**{k: v for k, v in data.items() if k in class_fields})


@dataclass
class ETL:
    cycle: str = "daily"
    pipeline: List[Union[Pipeline, dict]] = None
    secrets: Optional[dict] = None
    meta_output: Optional[str] = None

    def __post_init__(self):
        self.pipeline = Pipeline.from_dict(self.pipeline)

    @classmethod
    def from_dict(cls, data: dict):
        data.pop("parameters")
        [
            data.pop(key)
            for key in ["FIRST_DAY_MONTH", "LAST_DAY_MONTH", "YEAR", "MONTH", "DAY"]
        ]

        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in class_fields})
