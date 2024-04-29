import os
from copy import copy

import pandas as pd


def on_quit_save_old_df(df_to_save: pd.DataFrame, path: str) -> None:
    df_to_save.to_csv(path, index=False)


def on_quit_save_new_df(df_to_save: pd.DataFrame, path: str) -> None:
    if not os.path.exists(path):
        df_to_save.to_csv(path, index=False)
        return

    verified = pd.read_csv("./raw-data/verified/train-dataset.csv", header=0)
    for index, row in df_to_save.iterrows():
        verified.loc[len(verified)] = row

    verified.to_csv(path, index=False)


_LABEL_MAPPING = {
    "c": "Crisis",
    "o": "Other",
    "e": "Economical",
    "p": "Political",
    "r": "Corruption",
}

unverified_df = pd.read_csv("./raw-data/unverified/train-dataset.csv", header=0)
df = unverified_df.sort_values(by=["category", "txt"])
train_data_copy = copy(df.values)

verified_data_df = pd.DataFrame(columns=["channel", "txt", "date", "category"])

for train_item in train_data_copy:
    channel, txt, date, category = train_item[0], train_item[1], train_item[2], train_item[3]

    print(f"{txt}", end="\n\n")
    correct_label = input("Enter label: ")

    if correct_label == "q":
        on_quit_save_old_df(df, "./raw-data/unverified/train-dataset.csv")
        on_quit_save_new_df(verified_data_df, "./raw-data/verified/train-dataset.csv")
        exit(0)
    if correct_label == "s":
        df = df.drop(df[df["txt"] == txt].index)
        continue

    while correct_label.lower() not in _LABEL_MAPPING:
        correct_label = input("This label is not valid. Enter valid label: ")
        if correct_label == "q":
            on_quit_save_old_df(df, "./raw-data/unverified/train-dataset.csv")
            on_quit_save_new_df(verified_data_df, "./raw-data/verified/train-dataset.csv")
            exit(0)

    verified_data_df.loc[len(verified_data_df.index)] = {
        "channel": channel,
        "txt": txt,
        "date": date,
        "category": _LABEL_MAPPING[correct_label.lower()],
    }

    df = df.drop(df[df["txt"] == txt].index)

    os.system("cls" if os.name == "nt" else "clear")

on_quit_save_old_df(df, "./raw-data/unverified/train-dataset.csv")
on_quit_save_new_df(verified_data_df, "./raw-data/verified/train-dataset.csv")
