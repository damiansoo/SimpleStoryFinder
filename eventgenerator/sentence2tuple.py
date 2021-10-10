# converts sentences into 5 part tuples
import spacy
import unicodedata

input = open("test.txt", "r")
output = open("tuples.txt", "w")

nlp = spacy.load("en_core_web_sm")
queries = input.readlines()
for query in queries:
    text = query
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace('…', '...').replace('–', '-')
    text = text.replace('\n', '')
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    doc = nlp(text)
    verbFound = False

    subject = None
    verb = None
    object = None
    preposition = None
    modifier = None

    # node = None
    # node_child = None
    for token in doc:
        # if token.dep_ == "nsubj":
        #     subject.append(token.text)
        #     if token.head != None:
        #         verb.append(token.head.text)
        #         node = token.head.text
        #         node_child = token.text

        # if token.head.text == node:

        #     object.append(token.text)

        # if node == token.text:
        #     print([child for child in token.children])
            # if token.children[0].text == node_child:
            #     object.append(token.children[1].text)

        # if token.dep_ == "nsubj":
        #     subject.append(token.text)
        # if token.dep_ == "pobj":
        #     object.append(token.text)
        # if token.pos_ == "VERB":
        #      verb.append(token.text)
        # if token.dep_ == "prep":
        #     preposition.append(token.text)

        # if token.pos_ == "VERB":
        #     verb.append(token.text)
        #     verbFound = True
        # if token.pos_ == "NOUN" or token.pos_ == "PRON" or token.pos_ == "PROPN":
        #     if verbFound:
        #         object.append(token.text)
        #     else:
        #         subject.append(token.text)
        # if token.pos_ == "ADP":
        #     preposition.append(token.text)

        if token.pos_ == "VERB":
            if verb == None:
                verb = token.text+"_"+token.tag_
            verbFound = True
        if token.pos_ == "NOUN" or token.pos_ == "PRON" or token.pos_ == "PROPN":
            if subject == None:
                subject = token.text+"_"+token.tag_
            else:
                if token.dep_ != "nsubj":
                    if object != None:
                        modifier = object
                    object = token.text+"_"+token.tag_
        if token.pos_ == "ADP":
            if preposition == None:
                preposition = token.text+"_"+token.tag_
    
    sentenceTuple = subject, verb, object, preposition, modifier
    print(sentenceTuple)
    print()
        