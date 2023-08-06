import os
import subprocess
from pathlib import Path

import pandas as pd
from sqlalchemy.exc import OperationalError, ProgrammingError

from etl.models import Step, SubStep
from etl.utils.database import Database
from etl.utils.exceptions import NotSupported


def execute_sql(title: str, step: Step, secrets: dict, output: str = "csv") -> None:
    """Execute SQL

    param :title, str: Title about to be ran
    param :step, Step: Step object
    param :secrets, dict: Connection information
    param :output, str, 'csv': Output file type
    """
    print(f"Running {title}...")
    df = None

    with Database(secrets, step.connection) as database:
        df = database.execute(step.sql)

    save_frame(df, step.file_name, output)


def save_frame(df: pd.DataFrame, filename: str, output_type: str = "csv"):
    if df is not None:
        p = Path(filename)
        p.parent.mkdir(parents=True, exist_ok=True)
        print(f"\t\tSaving too: {filename}")

        if output_type == "csv":
            df.to_csv(filename)
        elif output_type == "hdfs":
            df.to_hdf(filename)
        elif output_type == "parquet":
            df.to_parquet(filename)
        else:
            raise NotSupported(f"{output_type}")


def merge_csv(title: str, step: SubStep) -> None:
    """Merges based on the item"""

    print(f"Running {title}...")
    one: pd.DataFrame = pd.read_csv(step.csv_one)
    two: pd.DataFrame = pd.read_csv(step.csv_two)
    out: pd.DataFrame = pd.merge(one, two, on=step.on)
    save_frame(out, step.csv_out, "csv")

    # chunk_container: pd.DataFrame = pd.read_csv("filename", chunksize=5000)
    # for chunk in chunk_container:
    #     chunk.to_csv("output", mode="a", index=False)


def move_frame(title: str, step: Step, secrets: dict) -> None:
    """Moves data from one table to other tables

    param :title, str: Title about to be ran
    param :step, Step: Step object
    param :secrets, dict: Connection information
    """
    print(f"Running {title}...")
    sql = step.sql

    with Database(secrets, step.connection) as source:
        with Database(secrets, step.target_connection) as target:
            for df_chunk in pd.read_sql_query(sql, source.engine, chunksize=10):
                for table in step.target_tables:
                    inital = True
                    if inital:
                        target.execute(basic="delete")
                        inital = False

                    df_chunk.to_sql(
                        table,
                        target.engine,
                        schema=step.schema,
                        method="multi",
                        index=False,
                        if_exists="append",
                    )


def sub_run(title: str, step: SubStep, output: str = "csv") -> None:
    """Runs command on a subprocess

    param :title, str: Title about to be ran
    param :step, Step: Step object
    param :output, str, 'csv': Output file type
    """
    print(f"Running {title}: \n\t\t{step}")
    print(subprocess.call([step.app, step.io]))


FUNCTIONS = {"sql": execute_sql, "pandas_push": move_frame}
SUBSET_FUNCTIONS = {"cat": sub_run, "python": sub_run, "merge_csv": merge_csv}
