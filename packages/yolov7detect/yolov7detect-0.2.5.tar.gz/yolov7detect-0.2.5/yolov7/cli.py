# https://github.com/fcakyon/yolov5-pip/blob/main/yolov5/cli.py

import fire

from yolov7 import __version__


def version() -> None:
    """Print version."""
    from yolov7 import __version__

    print(__version__)

def app() -> None:
    """Main function."""
    fire.Fire({"version": version})

if __name__ == "__main__":
    app()
