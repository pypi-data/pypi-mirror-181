
import base64
import json
import os
from pathlib import Path
from typing import Callable, Dict, List, Optional
import uuid


def pymbda_print(*args, **kwargs):
    print("[Pymbda]", *args, **kwargs)


def explore_aws_cfg(paths: List[Path]):
    for path in paths:
        cfg_path = path / "aws.cfg"
        if os.path.exists(cfg_path):
            os.environ["AWS_CONFIG_FILE"] = str(cfg_path.absolute())
            pymbda_print(f"Using AWS cfg file at '{cfg_path.absolute()}'")
            break


def history_append(path: Path, group: str, data):
    if not os.path.exists(path):
        with open(path, "w+") as f:
            json.dump({}, f)
    with open(path, "r+") as f:
        history_data = json.load(f)
        if group not in history_data:
            history_data[group] = []
        history_data[group].insert(0, data)
        f.seek(0)
        json.dump(history_data, f, indent=4)
        f.truncate()


def history_set(path: Path, group: str, data):
    if not os.path.exists(path):
        with open(path, "w+") as f:
            json.dump({}, f)
    with open(path, "r+") as f:
        history_data = json.load(f)
        history_data[group] = data
        f.seek(0)
        json.dump(history_data, f, indent=4)
        f.truncate()


def get_dir_size(path: str):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def profile_items_tops(items: Dict, item_name, item_value, *, top_amount=10, reverse=True):
    items[item_name] = item_value
    return dict(sorted(items.items(), key=lambda x: x[1], reverse=reverse)[:top_amount])


def profile_dir_size(path: str, file_sizes: Optional[Dict] = None):
    is_top_level = file_sizes is None
    file_sizes = file_sizes or {}
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                file_sizes = profile_items_tops(file_sizes, entry.path, entry.stat().st_size, top_amount=20)
            elif entry.is_dir():
                for file_name, file_size in profile_dir_size(entry.path, file_sizes).items():
                    file_sizes = profile_items_tops(file_sizes, file_name, file_size, top_amount=20)
    if is_top_level:
        for file_path, file_size in sorted(file_sizes.items(), key=lambda x: x[1], reverse=True)[:20]:
            print("\t", file_path, file_size)
    return file_sizes


def replace_template_vars(template: str, variables: Dict[str, str]):
    for variable_name, variable_value in variables.items():
        template = template.replace("{{" + variable_name + "}}", str(variable_value))
    return template


def is_valid_module_name(text: str):
    return text.replace('_', '').isalnum() and text.isascii() and not text[0].isdigit()


def is_valid_handler(text: str):
    return text.replace('.', '', 1).isalnum() and text.isascii() and not text[0].isdigit()


def input_choice(prompt: str, choices: List[str]):
    value = None
    while value not in choices:
        value = input(prompt)
    return value


def input_validated(prompt: str, validator: Callable[[str], bool]):
    value = None
    while value is None or validator(value):
        value = input(prompt)
    return value


def input_int(prompt: str, min: int = float("-inf"), max: int = float("inf"), default: int = None):
    value = None
    while value is None or min >= value >= max:
        try:
            pre_value = input(prompt)
            if default is not None and pre_value == "":
                return default
            value = int(pre_value)
        except ValueError:
            continue
    return value


def input_float(prompt: str, min: int = float("-inf"), max: int = float("inf"), default: int = None):
    value = None
    while value is None or min >= value >= max:
        try:
            pre_value = input(prompt)
            if default is not None and pre_value == "":
                return default
            value = float(pre_value)
        except ValueError:
            continue
    return value
