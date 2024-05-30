from pathlib import Path
from typing import Any, Dict

import yaml

# Определение пути к файлу конфигурации config.yaml
path: Path = Path(__file__).resolve().parents[1] / "config.yaml"


def read_yaml() -> Dict[str, Any]:
    """
    Читает YAML файл и возвращает его содержимое в виде словаря.

    Returns:
        Dict[str, Any]: Содержимое YAML файла в виде словаря.
    """
    with open(path, "r") as file:
        return yaml.safe_load(file)


def super_admin_add() -> Dict[str, Any]:
    """
    Получает настройки супер-администратора из конфигурационного файла.

    Returns:
        Dict[str, Any]: Словарь с настройками супер-администратора.
    """
    return read_yaml()["super_admin_add"]


def get_name_db() -> str:
    """
    Получает название базы данных SQLite3

    Returns:
        str: Строку с названием базы данных
    """
    return read_yaml()["db_name"]
