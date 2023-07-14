import os
import csv


class Validator:
    _LABEL_COLUMN_NAME = "label"
    _TEXT_COLUMN_NAME = "text"
    _VALIDATION_MAPPING = {
        "s": "Shelling",
        "o": "Other",
        "e": "Economical",
        "p": "Political",
    }

    def __init__(self, file_path: str, correct_label: str) -> None:
        self._file_path = file_path
        self._correct_label = correct_label

    def validate(self) -> None:
        with open(self._file_path, "r") as file, open(self._file_path.replace(".csv", "__validated.csv"), "w") as validated_file:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(validated_file, fieldnames=reader.fieldnames)

            row: dict[str, str]
            for row in reader:
                print(f"{row[self._TEXT_COLUMN_NAME]}")
                print()
                print(row[self._LABEL_COLUMN_NAME])

                correct_label = input("Enter correct label: ")
                if correct_label:
                    row[self._LABEL_COLUMN_NAME] = self._VALIDATION_MAPPING[correct_label.lower()]

                os.system("clear")

                writer.writerow(row)
