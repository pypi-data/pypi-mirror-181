# @Time    : 2022/11/28 11:07
# @Author  : WeiDai
# @FileName: __init__.py
from pathlib import Path
from typing import Union

DOLA_PROJECT_PATH = Path("../../..")
DOLA_SUI_PATH = DOLA_PROJECT_PATH.joinpath("sui")


def set_dola_project_path(path: Union[Path, str]):
    global DOLA_PROJECT_PATH
    global DOLA_SUI_PATH
    if isinstance(path, str):
        path = Path(path)
    DOLA_PROJECT_PATH = path
    DOLA_SUI_PATH = DOLA_PROJECT_PATH.joinpath("sui")
    assert DOLA_SUI_PATH.exists(), f"Path error:{DOLA_SUI_PATH.absolute()}!"
