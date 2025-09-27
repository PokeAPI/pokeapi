import csv
import os
from read_swsh import TextFile

if __name__ == "__main__":
	path = os.path.abspath(os.path.dirname(__file__))
	fileList = os.listdir(path)

	entriesList = []
	goodFiles = []

	# Get all the files in the current directory
	for file in fileList:
		ext = os.path.splitext(path + "\\" + file)[1]
		# Only get the .dat and .tbl files
		if (ext == ".tbl" or ext == ".dat"):
			goodFiles.append(file)

	# Parse through each file and put it in flavor_text
	with open(path + "\\pokemon_species_flavor_text_updated.csv", "w", encoding = "utf-8", newline = "") as fCSV:
		writer = csv.writer(fCSV, delimiter = ",")
		for i in range(0, len(goodFiles), 2):
			file1 = os.path.splitext(path + "\\" + goodFiles[i])[0]
			file2 = os.path.splitext(path + "\\" + goodFiles[i + 1])[0]
			# Ensure that we're wroking with the same .dat and .tbl pair
			if (file1 == file2):
				try:
					print(goodFiles[i])
					print(goodFiles[i + 1])
					# Parse through the .dat and .tbl
					textFile = TextFile(path + "\\" + goodFiles[i], path + "\\" + goodFiles[i + 1])
					dictionary = textFile.GetDict()
				except UserWarning as error:
					print(error)
				except Exception as error:
					print(error)

				try:
					if (len(dictionary) == 0):
						raise UserWarning('Error: the files returned no data')

					# Get the language and game from the file's name
					fileName = os.path.basename(path + "\\" + goodFiles[i]).lower().split("_")
					language = int(fileName[0])
					game = fileName[1]

					version = -1
					if game == "lgpe":
						# Let's Go Pikachu, then Eevee
						version = 31
						dupe = True

					elif game == "swsh":
						dupe = False
						if fileName[3] == "a":
							# Sword
							version = 33
						elif fileName[3] == "b":
							# Shield
							version = 34

					# Loop through the text file's dictionary and append the parsed data into the list
					for label, flavor_text in dictionary.items():
						if (len(flavor_text) > 1 and "[VAR]" not in flavor_text):
							species = int(label[0][14:17])
							entriesList.append([species, version, language, flavor_text])

							# Append a duplicate entry for Let's Go Eevee (both games use the same table)
							if (dupe):
								entriesList.append([species, 32, language, flavor_text])

				except UserWarning as error:
					print(error)
				except Exception as error:
					print(error)

		with open(path + "\\pokemon_species_flavor_text.csv", "r", encoding = "utf-8", newline = "") as fPoke:
			reader = csv.reader(fPoke, delimiter = ",")

			currentEntries = []
			# Get first line (info on what each column represents)
			header = next(reader)
			for row in reader:
				# species_id, version_id, language_id, flavor_text
				row = [int(row[0]), int(row[1]), int(row[2]), row[3]]
				entriesList.append(row)

		# Sort the list based on species id
		writer.writerow(header)
		entriesList.sort()
		writer.writerows(entriesList)
		print("Done")