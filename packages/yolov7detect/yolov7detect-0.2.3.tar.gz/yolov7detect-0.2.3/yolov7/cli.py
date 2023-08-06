# https://github.com/fcakyon/yolov5-pip/blob/main/yolov5/cli.py

import fire

from yolov7.detect import run as detect
from yolov7.export import run as export
from yolov7.train import run_cli as train
from yolov7.test import run as test


def app() -> None:
    """Cli app."""
    fire.Fire(
        {
            "train": train,
            "test": test,
            "detect": detect,
            "export": export,
        }
    )
    
if __name__ == '__main__':
    app()