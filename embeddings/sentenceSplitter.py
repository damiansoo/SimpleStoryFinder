import unicodedata
import math
path = "C:/Users/damia/Documents/COSC490/data/"

# queryFile = open(path+"prequery.txt", "r", encoding="utf-8")
# queryOut = open("querySentences.txt", "w")

# queries = queryFile.readlines()
# for line in queries:
# 	text = line.split(" ", 1)[1].strip()
# 	sentences = text.split(".")
# 	for sentence in sentences:
# 		if sentence == "":
# 			continue
# 		queryOut.write((sentence.strip()+".\n"))
# 	queryOut.write("\n")


# This part does not really need to exist, just doing this for consistencies sake
# Okay I lied need to add weird exceptions some sentences are 
# like 2000 characters (see line 1245565 of plots)

plotFile = open(path+"plots.txt", "r", encoding="utf-8")
plotOut = open("plotSentences.txt", "w")

plots = plotFile.readlines()
for line in plots:
	if line == "<EOS>\n":
		plotOut.write("\n")
	else:
		line = unicodedata.normalize('NFKD', line).encode('ascii', 'ignore').decode('utf-8')
		spaceCount = 0
		for char in line:
			if char == " ":
				spaceCount += 1
		if spaceCount < 300:
			plotOut.write(line)
		else:
			print(spaceCount)
			newSentences = []
			newSentenceCount = math.ceil(spaceCount/300)
			while newSentenceCount > 1:
				newSpaceCount = 0
				char = 0
				while True:
					if char == len(line):
						break
					if line[char] == " ":
						newSpaceCount += 1
					char += 1
					if newSpaceCount == 300:
						break
				while True:
					if char == len(line):
						newSentenceCount = 1
						break
					if line[char] == ",":
						newSentences.append(line[:char])
						line = line[char+1:]
						newSentenceCount -= 1
						break
					char+=1
			newSentences.append(line)
			for i in range(len(newSentences)):
				plotOut.write(newSentences[i].strip()+"\n")
				# if i == len(newSentences)-1:
				# 	plotOut.write(newSentences[i].strip()+"\n")
				# else:
				# 	plotOut.write(newSentences[i].strip()+"\n")

			# this sentence is long boi
			# newSentences = []
			# print(len(line))
			# while len(line) > 512:
			# 	i = 450
			# 	while line[i] != " ":
			# 		i += 1
			# 	newSentences.append(line[:i])
			# 	line = line[i+1:]
			# newSentences.append(line)
			# for sentence in newSentences:
			# 	print(len(sentence))
			# print()

