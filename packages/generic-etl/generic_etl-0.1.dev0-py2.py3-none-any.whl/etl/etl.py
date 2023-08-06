import sys
from pprint import pprint as print

from etl.functions.general import FUNCTIONS as FUNC
from etl.functions.general import SUBSET_FUNCTIONS
from etl.models import ETL
from etl.utils.utils import file_information, load_yaml

FUNCTIONS = {}
FUNCTIONS.update(FUNC)
FUNCTIONS.update(SUBSET_FUNCTIONS)


def run(conf: ETL):
    """Runs the ETL pipeline

    param :conf, ETL: ETL object to run
    """
    for k in conf.pipeline.steps:
        for step in conf.pipeline.steps[k]:
            try:
                if step.sub_steps:
                    for sub in step.sub_steps:
                        sub_ = step.sub_steps[sub]
                        FUNCTIONS[str(sub_.app).lower()](k, sub_)
                else:
                    FUNCTIONS[str(step.function).lower()](k, step, conf.secrets)

                    if step.file_name:
                        file_information(step.file_name, conf.meta_output)
            except KeyError as ex:
                print(ex)
                continue


def main():
    """Main function"""
    args = sys.argv
    if len(args) < 2:
        raise ValueError("Missing pipeline yaml target...")
    conf = load_yaml(args[1])
    conf = ETL.from_dict(conf)
    if conf.secrets:
        conf.secrets = load_yaml(conf.secrets, dynamic=False)
    else:
        conf.secrets = load_yaml(args[2], dynamic=False)
    run(conf)


if __name__ == "__main__":
    """Entrypoint"""
    main()
