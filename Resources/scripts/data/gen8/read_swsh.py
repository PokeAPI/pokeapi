import copy
import os
import struct
import sys

class TextLine():
	offset = None
	length = None

class TextFile():
	def __init__(this, path1, path2):
		this.__dictEntries = {}
		this.__magic = 0x42544841
		this.__KEY_BASE = 0x7C89
		this.__KEY_ADVANCE = 0x2983
		this.__KEY_VARIABLE = 0x0010
		this.__KEY_TERMINATOR = 0x0000

		# Load dex labels
		if (os.path.splitext(path1)[1] == ".tbl"):
			this.__OpenTbl(path1)
		elif (os.path.splitext(path2)[1] == ".tbl"):
			this.__OpenTbl(path2)
		else:
			raise UserWarning("Error: a .tbl was not given")

		# Load dex entries
		if (os.path.splitext(path1)[1] == ".dat"):
			this.__OpenDat(path1)
		elif (os.path.splitext(path2)[1] == ".dat"):
			this.__OpenDat(path2)
		else:
			raise UserWarning("Error: a .dat was not given")

		# The table has 1 more entry than the dat to show when the table ends
		if (len(this.__labels) == len(this.__lines) + 1):
			for i in range(0, len(this.__lines)):
				this.__dictEntries[this.__labels[i]] = this.__lines[i]

	@property
	def __TextSections(this):
		"""(2 bytes) Gets the number of text sections"""
		return struct.unpack_from("<H", this.__data, 0x0)[0]

	@property
	def __LineCount(this):
		"""(2 bytes) Gets the amount of lines"""
		return struct.unpack_from("<H", this.__data, 0x2)[0]

	@property
	def __TotalLength(this):
		"""(4 bytes) Gets the total character length of all text sections"""
		return struct.unpack_from("<I", this.__data, 0x4)[0]

	@property
	def __InitialKey(this):
		"""(4 bytes) Gets the initial key; should be 0x00000000"""
		return struct.unpack_from("<I", this.__data, 0x8)[0]

	@property
	def __SectionDataOffset(this):
		"""(4 bytes) Gets the offset where the data section begins"""
		return struct.unpack_from("<I", this.__data, 0xC)[0]

	@property
	def __SectionLength(this):
		"""(4 bytes) Gets the length of characters the given section is"""
		offset = this.__SectionDataOffset
		return struct.unpack_from("<I", this.__data, offset)[0]

	@property
	def __LineOffsets(this):
		"""Figures out the offset for each entry based on the data section offset"""
		result = [None] * this.__LineCount
		sdo = int(this.__SectionDataOffset)
		for i in range(0, len(result)):
			result[i] = TextLine()
			result[i].offset = struct.unpack_from("<i", this.__data, (i * 8) + sdo + 4)[0] + sdo
			result[i].length = struct.unpack_from("<h", this.__data, (i * 8) + sdo + 8)[0]

		return result

	def GetLabels(this):
		return this.__labels

	def GetDict(this):
		return this.__dictEntries

	def HashFNV1_64(this, word):
		"""Fowler-Noll-Vo hash function; 64-bit"""
		fnvPrime_64 = 0x100000001b3
		offsetBasis_64 = 0xCBF29CE484222645

		hash = offsetBasis_64
		for c in word:
			hash = hash ^ ord(c)
			# Cast hash to at 64-bit value
			hash = (hash * fnvPrime_64) % 2**64

		return hash

	def __LineData(this, data):
		"""Loads the file into a list to later decrypt"""
		key = copy.copy(this.__KEY_BASE)
		result = [None] * this.__LineCount
		lines = this.__LineOffsets

		for i in range(0, len(lines)):
			# Make a list twice the size of the current text line size
			encrypted = lines[i].length * 2
			# Then copy the encrypted line starting from the given offset for however long the given list is
			end = lines[i].offset + encrypted
			encrypted = this.__data[lines[i].offset:end]

			result[i] = this.__CryptLineData(encrypted, key)
			# Cast key to a 16-bits (otherwise things break)
			key = (key + this.__KEY_ADVANCE) % 2**16

		return result

	def __CryptLineData(this, data, key):
		"""Decrypts the given line into a list of bytes"""
		copied = copy.copy(data)
		result = [None] * len(copied)

		for i in range(0, len(copied), 2):
			result[i] = copied[i] ^ (key % 256)
			result[i + 1] = copied[i + 1] ^ ((key >> 8) % 256)
			# Bit-shift and OR key, then cast to 16-bits (otherwise things break)
			key = (key << 3 | key >> 13) % 2**16

		return result

	def __GetLineString(this, data):
		"""Turns the given list of bytes into a finished string"""
		if (data is None):
			return None

		string = ""
		i = 0
		while (i < len(data)):
			# Cast 2 bytes to figure out what to do next
			value = struct.unpack_from("<H", data, i)[0]
			if (value == this.__KEY_TERMINATOR):
				break;
			i += 2

			if (value == this.__KEY_TERMINATOR):
				return string
			elif (value == this.__KEY_VARIABLE):
				string += "[VAR]"
			elif (value == "\n"):
				string += "\n"
			elif (value == "\\"):
				string += "\\"
			elif (value == "["):
				string += "\["
			else:
				string += chr(value)

		return string

	def __MakeLabelHash(this, f):
		"""Returns the label name and a FNV1_64 hash"""
		# Next 8 bytes is the hash of the label name
		hash = struct.unpack("<Q", f.read(8))[0]
		# Next 2 bytes is the label"s name length
		nameLength = struct.unpack("<H", f.read(2))[0]
		# Read the bytes until 0x0 is found
		name = this.__ReadUntil(f, 0x0)

		if (this.HashFNV1_64(name) == hash):
			return name, hash

	def __OpenDat(this, path):
		with open(path, "rb") as file:
			try:
				this.__data = file.read()
			except:
				raise UserWarning("Error: Could not open .dat")

		# Decrypt the text
		cryptedText = this.__LineData(this.__data)
		this.__lines = []
		for line in cryptedText:
			this.__lines.append(this.__GetLineString(bytearray(line)))

	def __OpenTbl(this, path):
		with open(path, "rb") as f:
			try:
				# First four bytes is "magic"; needs to be 0x42544841
				testMagic = struct.unpack("<I", f.read(4))[0]	
				if (testMagic == this.__magic):
					# Next four bytes is the number of entries to read
					count = struct.unpack("<I", f.read(4))[0]
					this.__labels = []
					# Iterate through the entries
					for i in range(0, count):
						this.__labels.append(this.__MakeLabelHash(f))

			except struct.error:
				raise UserWarning("Error: Coult not open .tbl")

	def __ReadUntil(this, f, value):
		"""Reads the given file until it reaches the given value"""
		string = ""
		c = f.read(1)
		end = bytes([value])
		while (c != end):
			# Read one byte at a time to get each character
			string += c.decode("utf-8")
			c = f.read(1)

		return string