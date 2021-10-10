from bs4 import BeautifulSoup
import requests
import csv
import os
import string

folder_name = "full"
queCount = 1
try:
	os.mkdir(folder_name)
except FileExistsError:
	pass
head = open(folder_name + "/headers.txt", "w+", encoding = "utf-8")
plt = open(folder_name + "/plots.txt", "w+", encoding = "utf-8")
ans = open(folder_name + "/answers.txt", "w+", encoding = "utf-8")

dumb_cases = ["but at which time interval", "sloved", "in before me"]
solveStrs = ["yes", "thank you", "thats it", "thats him", "thats right", "solved", "thats the one", "thanks", "of course", "bingo"] + dumb_cases
selfSolveStrs = ["this film is", "i remember", "i found it", "i figured it out", "is right"]
ignoreStrs = ["nope", "no its not", "thats not it", "i dont think", "thanks anyway", "thanks but", "not that", "could be it", "not movie", "not the movie", "it wasnt"]
translator = str.maketrans('', '', string.punctuation+'‘’“”') # for removing punctuation

pageMax = 143 + 1 # There are only 143 pages of 'solved'

for page in range(1, pageMax):
	url = 'https://irememberthismovie.com/category/solved'
	if page > 1:
		url = url + '/page/' + str(page) + '/'
	response = requests.get(url, timeout=5)
	content = BeautifulSoup(response.content, "html.parser")

	header = ""
	link = ""
	#Finds the article labels in the page 
	for article in content.findAll('article'):
		#this count is to make the findAll only find the first occurence of a
		count = 0
		for a in article.findAll('a'):
				if(count == 0):
					header = a.text.encode('utf-8').decode('utf-8')
				count = 1
		head.write(str(page) + "/" + str(queCount) + " " + header + "\n\n")
		plot = ""
		for div in article.findAll('div', attrs = {"class": "entry-content"}):
			#we find all div in the article because in them are the comments.
			for p in div.findAll('p'):
				#inside the div are the p labels which have the plot
				plot= plot +str(p.text.encode('utf-8').decode('utf-8'))
		plt.write(str(page) + "/" + str(queCount) + " " + plot+"\n\n")
		#Similar to above except only lookingf or articles with comments-link
		for div in article.findAll('div', attrs = {"class": "comments-link"}):
			#Getting the links to the comments
			for a in div.findAll('a'):
				urlC = a.get('href')
				commentArray = []
				count2 = -1
				check = 0
				responseC = requests.get(urlC, timeout = 5)
				contentC = BeautifulSoup(responseC.content, "html.parser")
				#The ol labels seemed to be a good marker for comments
				# Doesnt work in all cases as some comments are stored in divs, ols, uls, etc.. instead of just a p tag
				for ol in contentC.findAll('ol', attrs = {"class": "comment-list"}):
					#each li had a parent ol which allows me to check if the ol is a children type
					for li in ol.findAll("li"):
						a = str(li.parent.attrs)
						#If statement to determine if comment is a child comment
						if(a == "{'class': ['children']}"):
							#I only want the the direct children of li, thus the recursive = false
							for art in li.findAll('article', recursive = False):
								comments = ""
								for p in art.findAll('p'):
									comments = comments + " child -> " +str(p.text) + " "
								commentArray.append(comments)
						else:
							for art in li.findAll('article', recursive = False):
								comments = ""
								for p in art.findAll('p'):
									comments = comments +str(p.text) + " "
								commentArray.append(comments)
				
				po = ""
				commentCount = 0
				childOccur = 0

				for com in commentArray:
					ignore = False
					if(commentArray[commentCount].find("child ->") > 0 and childOccur == 0):
						# childOccur = commentCount
						for ignoreStr in ignoreStrs:
							if (commentArray[commentCount].translate(translator).lower().find(ignoreStr) >= 0):
								ignore = True
								break
						if ignore:
							commentCount += 1
							continue
						for solveStr in solveStrs:
							if (commentArray[commentCount].translate(translator).lower().find(solveStr) >= 0):
								if commentCount-2 < 0:
									pass
								else:
									for solveStr2 in solveStrs:
										if (commentArray[commentCount-1].translate(translator).lower().find(solveStr2) >= 0):
											po = commentArray[commentCount-2]
								for selfSolveStr in selfSolveStrs:
									if (commentArray[commentCount].translate(translator).lower().find(selfSolveStr) >= 0):
										po = commentArray[commentCount-1] + " " + commentArray[commentCount]
										break
								i = 1
								if po == "":
									while commentArray[commentCount - i] == "":
										i += 1
									po = commentArray[commentCount-i]
									break
						if (po != ""):
							break
					commentCount += 1
				if (po == ""):
					commentCount = 0
					for com in commentArray:
						for selfSolveStr in selfSolveStrs:
							if (commentArray[commentCount].translate(translator).lower().find(selfSolveStr) >= 0):
								po = commentArray[commentCount]
								break
						# if (po != ""):
						# 	break
						commentCount += 1
				# if queCount == 14:
				# 	print(po)
				if (po == ""):
					commentCount = 0
					for com in commentArray:
						for solveStr in solveStrs:
							if (commentArray[commentCount].translate(translator).lower().find(solveStr) >= 0):
								if commentCount-1 >= 0:
									po = commentArray[commentCount-1]
								break
						if (po != ""):
							break
						commentCount += 1
				if po == "":
					if len(commentArray) > 0:
						po = commentArray[0]
						commentCount = 0
					else:
						po = "[NO COMMENTS]"
						commentCount = -1
				# for solveStr in solveStrs:
				# 	if (po.find(solveStr) >= 0):
				# 		po = po + " " + commentArray[commentCount-1]
				i = 1
				while po.replace(" child -> ", "").strip() == "":
					# print(commentCount)
					po = commentArray[commentCount-i]
					i += 1
				ans.write(str(page) + "/" + str(queCount) + " " + po.encode('utf-8').decode('utf-8').replace(" child -> ", "") + "\n\n")
		queCount+=1
	print("Page " + str(page) + " completed.")
	ans.flush()

head.close()
plt.close()
ans.close()


