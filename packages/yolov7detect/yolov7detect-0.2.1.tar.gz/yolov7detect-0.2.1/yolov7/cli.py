# https://github.com/fcakyon/yolov5-pip/blob/main/yolov5/cli.py

import fire

from yolov7.detect import run as detect
from yolov7.export import run as export
from yolov7.train import run_cli as train
from yolov7.val import run as val


def app() -> None:
    """Cli app."""
    fire.Fire(
        {
            "train": train,
            "val": val,
            "detect": detect,
            "export": export,
        }
    )
