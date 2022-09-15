import spacy


import csv
from pathlib import Path

def load_entities():
    entities_loc = Path.cwd()  / "entities.csv"  # distributed alongside this notebook

    names = dict()
    descriptions = dict()
    with entities_loc.open("r", encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            qid = row[0]
            name = row[1]
            desc = row[2]
            names[qid] = name
            descriptions[qid] = desc
    return names, descriptions

nlp = spacy.load("en_core_web_lg")
text = "Tennis champion Emerson was expected to win Wimbledon."
doc = nlp(text)
for ent in doc.ents:
    print(f"Named Entity '{ent.text}' with label '{ent.label_}'")

name_dict, desc_dict = load_entities()
for QID in name_dict.keys():
    print(f"{QID}, name={name_dict[QID]}, desc={desc_dict[QID]}")

from spacy.kb import KnowledgeBase
kb = KnowledgeBase(vocab=nlp.vocab, entity_vector_length=300)


for qid, desc in desc_dict.items():
   desc_doc = nlp(desc)
   desc_enc = desc_doc.vector
   kb.add_entity(entity=qid, entity_vector=desc_enc, freq=342)   # 342 is an arbitrary value here

for qid, name in name_dict.items():
   kb.add_alias(alias=name, entities=[qid], probabilities=[1])   # 100% prior probability P(entity|alias)


qids = name_dict.keys()
probs = [0.3 for qid in qids]
kb.add_alias(alias="Emerson", entities=qids, probabilities=probs)  # sum([probs]) should be <= 1 !


print(f"Entities in the KB: {kb.get_entity_strings()}")
print(f"Aliases in the KB: {kb.get_alias_strings()}")

print(f"Candidates for 'Roy Stanley Emerson': {[c.entity_ for c in kb.get_alias_candidates('Roy Stanley Emerson')]}")
print(f"Candidates for 'Emerson': {[c.entity_ for c in kb.get_alias_candidates('Emerson')]}")
print(f"Candidates for 'Sofie': {[c.entity_ for c in kb.get_alias_candidates('Sofie')]}")