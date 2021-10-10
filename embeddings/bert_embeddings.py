import torch
import numpy as np
from transformers import BertTokenizer, BertModel
import nltk.data
import unicodedata

np.set_printoptions(suppress=True)
device = torch.device('cuda:0')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
nltk_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states = True)

model.cuda()
model.eval()

# ## Process queries
queryFile = open("querySentences.txt", "r")
queries = queryFile.readlines()

queryOut = open("queryEmbeddings.txt", "w")

past_key_values = None
sentenceEmbeddings = []
for i, sentence in enumerate(queries):
	if i % 100 == 0:
		print("{}/{} lines read.".format(i, len(queries)))

	if sentence != "\n":
		encoded_text = tokenizer(sentence, return_tensors="pt")
		encoded_text.to(device)

		tokens_tensor = encoded_text["input_ids"]
		segments_tensor = encoded_text["attention_mask"]

		with torch.no_grad():
			outputs = model(tokens_tensor, segments_tensor, use_cache=True)
			hidden_states = outputs[2]

		# [# layers, # batches, # tokens, # features]
		token_embeddings = torch.stack(hidden_states, dim=0)

		# [# batches, # tokens, # layers, # features]
		token_embeddings = token_embeddings.permute(1,2,0,3)

		# print(len(token_embeddings[0][0][-1]))
		sentenceEmbeddings.append(token_embeddings[0][0][-1])
	else:
		# break # for testing
		if len(sentenceEmbeddings) > 0:
			docVec = np.zeros(768)
			for embedding in sentenceEmbeddings:
				sentenceVec = embedding.cpu().numpy()
				docVec = np.add(docVec, sentenceVec) # sum of sentences
			
			docVec = docVec / len(sentenceEmbeddings) # average of sentences

			for i in range(len(docVec)):
				if i == 0:
					queryOut.write(str(docVec.item(i)))
				else:
					queryOut.write(" "+str(docVec.item(i)))
			queryOut.write("\n")
			sentenceEmbeddings.clear()
			

# ### Process plots
# plotFile = open("plotSentences.txt", "r")
# plots = plotFile.readlines()

# plotOut = open("plotEmbeddings.txt", "w")

# sentenceEmbeddings = []
# for i, sentence in enumerate(plots):
# 	# if i < 1245500:
# 	# 	continue
# 	if i % 100 == 0:
# 		print("{}/{} lines read.".format(i, len(plots)))

# 	if sentence != "\n":
# 		encoded_text = tokenizer(sentence, return_tensors="pt")
# 		encoded_text.to(device)

# 		tokens_tensor = encoded_text["input_ids"]
# 		segments_tensor = encoded_text["attention_mask"]

# 		with torch.no_grad():
# 			# try:
# 			# 	outputs = model(tokens_tensor, segments_tensor)
# 			# 	hidden_states = outputs[2]
# 			# except:
# 			# 	print("error at line {}".format(i))
# 			# 	quit(1)
# 			outputs = model(tokens_tensor, segments_tensor)
# 			hidden_states = outputs[2]

# 		# [# layers, # batches, # tokens, # features]
# 		token_embeddings = torch.stack(hidden_states, dim=0)

# 		# [# batches, # tokens, # layers, # features]
# 		token_embeddings = token_embeddings.permute(1,2,0,3)

# 		# print(len(token_embeddings[0][0][-1]))
# 		sentenceEmbeddings.append(token_embeddings[0][0][-1])
# 	else:
# 		# break # for testing
# 		if len(sentenceEmbeddings) > 0:
# 			docVec = np.zeros(768)
# 			for embedding in sentenceEmbeddings:
# 				sentenceVec = embedding.cpu().numpy()
# 				docVec = np.add(docVec, sentenceVec) # sum of sentences
			
# 			docVec = docVec / len(sentenceEmbeddings) # average of sentences

# 			for i in range(len(docVec)):
# 				if i == 0:
# 					plotOut.write(str(docVec.item(i)))
# 				else:
# 					plotOut.write(" "+str(docVec.item(i)))
# 			plotOut.write("\n")
# 			sentenceEmbeddings.clear()