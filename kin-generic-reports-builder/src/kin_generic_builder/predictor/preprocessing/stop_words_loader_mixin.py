import csv
import json
import logging
from json import JSONDecodeError

_logger = logging.getLogger(__name__)


class StopWordsLoaderMixin:
    def load_stop_words(self, stop_words_file_path: str) -> tuple[bool, list[str]]:
        try:
            for loader in [self._load_json, self._load_csv, self._load_txt]:
                success, words_list = loader(stop_words_file_path)
                if success:
                    return True, words_list
        except Exception as ex:
            _logger.warning(f"Stop words file {stop_words_file_path} is not valid: {ex}")
            return False, []

        return False, []

    def _load_json(self, stop_words_file_path: str) -> tuple[bool, list[str]]:
        try:
            with open(stop_words_file_path, "r") as stop_words_file:
                json_data = json.load(stop_words_file)

                if isinstance(json_data, list):
                    return True, json_data

                if isinstance(json_data, dict) and len(json_data) == 1:
                    return True, list(json_data.values())[0]

                return False, []
        except JSONDecodeError as ex:
            return False, []

    def _load_csv(self, stop_words_file_path: str) -> tuple[bool, list[str]]:
        try:
            with open(stop_words_file_path, newline='') as file:
                reader = csv.reader(file)
                words = [row[0] for row in reader if row]
                return True, words
        except Exception:
            return False, []

    def _load_txt(self, stop_words_file_path: str) -> tuple[bool, list[str]]:
        try:
            with open(stop_words_file_path, "r") as file:
                return True, file.readlines()
        except Exception:
            return False, []
