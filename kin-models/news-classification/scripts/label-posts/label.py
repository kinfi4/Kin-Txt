import os
import csv


class Validator:
    _LABEL_COLUMN_NAME = "label"
    _TEXT_COLUMN_NAME = "text"
    _LABEL_MAPPING = {
        "c": "Crisis",
        "o": "Other",
        "e": "Economical",
        "p": "Political",
        "cr": "Corruption",
    }

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def start_labeling(self) -> None:
        with (
            open(self._file_path, "r", encoding="UTF-8") as file_to_read_from,
            open(self._file_path.replace(".csv", "__labeled.csv"), "w", encoding="UTF-8") as labeled_file,
        ):
            reader = csv.DictReader(file_to_read_from)
            print(reader.fieldnames)
            writer = csv.DictWriter(labeled_file, fieldnames=[*reader.fieldnames, self._LABEL_COLUMN_NAME])
            writer.writerow({field: field for field in reader.fieldnames})

            row: dict[str, str]
            for row in reader:
                print(f"{row[self._TEXT_COLUMN_NAME]}", end="\n\n")

                correct_label = input("Enter label: ")

                if correct_label == "q":
                    return
                if correct_label == "s":
                    os.system("cls" if os.name == "nt" else "clear")
                    continue

                while correct_label.lower() not in self._LABEL_MAPPING:
                    correct_label = input("This label is not valid. Enter valid label: ")
                    if correct_label == "q":
                        return

                if correct_label:
                    row[self._LABEL_COLUMN_NAME] = self._LABEL_MAPPING[correct_label.lower()]

                os.system("cls" if os.name == "nt" else "clear")

                writer.writerow(row)
