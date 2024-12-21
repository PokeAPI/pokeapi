import csv
import os
from read_swsh import TextFile

# data_path contains the countents of the `message` folder found in sword/shield's romfs:/bin/
if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", "..", "data")
    csv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", "pokedex", "data", "csv")

    languages = {
        "JPN": 1,
        "Korean": 3,
        "Trad_Chinese": 4,
        "French": 5,
        "German": 6,
        "Spanish": 7,
        "Italian": 8,
        "English": 9,
        "JPN_KANJI": 11,
        "Simp_Chinese": 12,
    }

    header = ["move_id", "local_language_id", "name"]
    entries = []

    # shadow moves
    with open(os.path.join(csv_path, "move_names.csv"), "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            if row[0].isnumeric() and int(row[0]) > 10000:
                entries.append([int(row[0]), int(row[1]), row[2]])

    with open(os.path.join(csv_path, "move_names.csv"), "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",", lineterminator="\n")
        for language_dir, language_id in languages.items():
            try:
                # Parse through the .dat and .tbl
                textFile = TextFile(
                    os.path.join(data_path, language_dir, "common", "wazaname.dat"),
                    os.path.join(data_path, language_dir, "common", "wazaname.tbl"),
                )
                dictionary = textFile.GetDict()
            except UserWarning as error:
                print(error)

            try:
                if len(dictionary) == 0:
                    raise UserWarning("Error: the files returned no data")

                # Loop through the text file's dictionary and append the parsed data into the list
                for label, text in dictionary.items():
                    id = int(label[0].split("_")[1])
                    if id == 0:
                        continue
                    entries.append([id, language_id, text.strip("\r")])

            except UserWarning as error:
                print(error)

        # Sort the list based on species id
        writer.writerow(header)
        entries.sort()
        writer.writerows(entries)
        print("Done")
