# converts plaintext queries into generalised sentences
# use venv virtual environment (python3.7.*, spacy2.1.0)
# neuralcoref explicitly requires spacy2.1.0

import spacy
import neuralcoref

# change input and output vars as needed
input = open("ner_examples/query/input_query.txt", "r", encoding="utf-8")
output1 = open("ner_examples/query/queries.txt", "w", encoding="utf-8")
output2 = open("ner_examples/query/queries_generalised.txt", "w", encoding="utf-8")

nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)

ner_dict = {}
ner_tag_count = {}

for line in input.readlines():
    ner_dict.clear()
    ner_tag_count.clear()
    print(line)
    doc = nlp(line)
    output1.write(doc._.coref_resolved)

    doc2 = doc._.coref_resolved
    doc_r = nlp(doc2)
    for ent in doc_r.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ner_dict.get(ent.text) == None:
            if ner_tag_count.get(ent.label_) == None:
                ner_tag_count[ent.label_] = 1
            else:
                ner_tag_count.update({ent.label_: ner_tag_count.get(ent.label_)+1})
            ner_dict[ent.text] = "<"+ent.label_+">"+str(ner_tag_count.get(ent.label_))

    print(ner_dict)
    print(ner_tag_count)

    for ent in reversed(doc_r.ents):
        print(doc2)
        doc2 = doc2[0:ent.start_char] + ner_dict.get(ent.text) + doc2[ent.end_char:]

    print(doc2)
    output2.write(doc2)
