import os
import csv


class Validator:
    _LABEL_COLUMN_NAME = "label"
    _TEXT_COLUMN_NAME = "text"

    def __init__(self, file_path: str, correct_label: str) -> None:
        self._file_path = file_path
        self._correct_label = correct_label

    def validate(self) -> None:
        with open(self._file_path, "r") as file, open(self._file_path.replace(".csv", "__validated.csv"), "w") as validated_file:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(validated_file, fieldnames=reader.fieldnames)

            row: dict[str, str]
            for row in reader:
                if not row[self._LABEL_COLUMN_NAME] == self._correct_label:
                    print(f"{row[self._TEXT_COLUMN_NAME]} |||| {row[self._LABEL_COLUMN_NAME]}")
                    correct_label = input("Enter correct label: ")
                    row[self._LABEL_COLUMN_NAME] = correct_label

                    os.system("clear")

                writer.writerow(row)
