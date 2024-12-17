# Configuration file for directory paths and file paths used throughout the project
from mailbox import Message
import os
from pathlib import Path
from typing import List, Dict, Optional

from helper_script.json_helper import read_json


CONFIG_STRUCTURE = """{
    "path": {
        "cached_dir": "caches",
        "dataset_dir": "dataset",
        "output_dir": "caches/processed_output"
    },
    "parameters": {
        "calculation_threshold": 1e-5,
        "max_calculation_iteration": 200,
        "max_summarize_length": 20
    },
    "options": {
        "use_pagerank_library": false,
        "output_graph": true,
        "show_graph": false
    },
    "target_data_key": [
        "full_text"
    ]
}"""


def check_and_get_config(file_path: str) -> dict:
    def raise_missing_key_error(missing_keys: List[str]):
        if len(missing_keys) > 0:
            message = f"Missing keys: {missing_keys} in {file_path}"
            print(f"{message}\n\nDefault config.json structure:\n{CONFIG_STRUCTURE}\n")
            raise KeyError(message)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    config = read_json(file_path)

    needed_keys = ["path", "options", "parameters", "target_data_key"]
    missing_keys = [f"'{key}'" for key in needed_keys if key not in config]
    raise_missing_key_error(missing_keys)


    missing_keys.extend([f"path.{key}" for key in ["cached_dir", "dataset_dir", "output_dir"] if key not in config["path"]])
    missing_keys.extend([f"parameters.{key}" for key in ["calculation_threshold", "max_calculation_iteration", "max_summarize_length"] if key not in config["parameters"]])
    missing_keys.extend([f"options.{key}" for key in ["use_pagerank_library", "output_graph", "show_graph"] if key not in config["options"]])
    raise_missing_key_error(missing_keys)


    return config


def correct_path(path: str) -> Path:
    return Path(*Path(path.replace("\\","/")).parts)


CONFIG: dict = check_and_get_config("config.json")
CONFIG_CACHE_NAME: str = correct_path(CONFIG["path"]["cached_dir"])
CONFIG_DATA_DIR: str = correct_path(CONFIG["path"]["dataset_dir"])
CONFIG_OUTPUT_DIR: str = correct_path(CONFIG["path"]["output_dir"])

BASED_DIR: Path = Path(__file__).resolve().parent
CACHE_DIR: Path = BASED_DIR / CONFIG_CACHE_NAME

NLTK_PATH: Path = BASED_DIR / CONFIG_CACHE_NAME / "nltk_data"

DATA_DIR: Path = BASED_DIR / CONFIG_DATA_DIR
OUTPUT_DIR: Path = BASED_DIR / CONFIG_OUTPUT_DIR


# Settings
USE_PAGERANK_LIBRARY: bool = CONFIG["options"]["use_pagerank_library"]
OUTPUT_GRAPH: bool = CONFIG["options"]["output_graph"]
SHOW_GRAPH: bool = CONFIG["options"]["show_graph"]

# Calculation Config
TARGET_DATA_KEY: Optional[list] = CONFIG["target_data_key"]
if len(TARGET_DATA_KEY) == 0: TARGET_DATA_KEY = None

CALCULATION_THRESHOLD: float = CONFIG["parameters"]["calculation_threshold"]
MAX_CALCULATION_ITERATION: int = CONFIG["parameters"]["max_calculation_iteration"]
TRUST_RANK_BIAS_AMOUNT: int = CONFIG["parameters"]["trustrank_bias_amount"]
MAX_TRUST_RANK_ITERATION: int = CONFIG["parameters"]["max_summarize_length"] # Equivalent to max number of summarized words
