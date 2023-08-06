from .pyinstaller import Pyinstaller as Pyinstaller
from _typeshed import Incomplete
from enum import IntEnum
from typing import Optional

class SmartAutoModuleCombineMode(IntEnum):
    DISABLE: Incomplete
    FOLDER_ONLY: Incomplete
    ALL_INTO_ONE: Incomplete

class Builder:
    @staticmethod
    def delete_file_if_exist(path: str) -> None: ...
    @staticmethod
    def copy(files: tuple, target_folder: str) -> None: ...
    @classmethod
    def compile(cls, source_folder: str, target_folder: str = ..., additional_files: tuple = ..., ignore_key_words: tuple = ..., smart_auto_module_combine: SmartAutoModuleCombineMode = ..., remove_building_cache: bool = ..., update_the_one_in_sitepackages: bool = ..., include_pyinstaller_program: bool = ..., options: dict = ...) -> None: ...
    @classmethod
    def upload_package(cls, python_ver: Optional[str] = ...) -> None: ...
