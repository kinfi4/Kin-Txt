import os
import csv


class Validator:
    _LABEL_COLUMN_NAME = "label"
    _TEXT_COLUMN_NAME = "text"
    _LABEL_MAPPING = {
        "s": "Shelling",
        "o": "Other",
        "e": "Economical",
        "p": "Political",
    }

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def start_labeling(self) -> None:
        with open(self._file_path, "r") as file, open(self._file_path.replace(".csv", "__labeled.csv"), "w") as labeled_file:
            reader = csv.DictReader(file)
            print(reader.fieldnames)
            writer = csv.DictWriter(labeled_file, fieldnames=[*reader.fieldnames, self._LABEL_COLUMN_NAME])
            writer.writerow({field: field for field in reader.fieldnames})

            row: dict[str, str]
            for row in reader:
                print(f"{row[self._TEXT_COLUMN_NAME]}")
                print()

                correct_label = input("Enter label: ")

                if correct_label == "q":
                    break

                while correct_label.lower() not in self._LABEL_MAPPING:
                    correct_label = input("This label is not valid. Enter valid label: ")
                    if correct_label == "q":
                        break

                if correct_label:
                    row[self._LABEL_COLUMN_NAME] = self._LABEL_MAPPING[correct_label.lower()]

                os.system("clear")

                writer.writerow(row)
