from sentence_transformers import SentenceTransformer,util
import pandas as pd

modules = ['E-Invoices', 'Dashboard', 'Manual Upload','Tax','User and Entity Management']

model = SentenceTransformer('all-MiniLM-L6-v2')

db = pd.read_excel('Modules.xlsx')
Questions = db.iloc[:,0].tolist()
Answers = db.iloc[:,1].tolist()

Encoder = model.encode(Questions, normalize_embeddings=True)
Moduler = model.encode(modules, normalize_embeddings=True)

classified_modules = []
for i, faq_vec in enumerate(Encoder):
    scores = util.cos_sim(faq_vec, Moduler)[0]
    best_match_idx = scores.argmax()
    proba = max(scores)
    if proba < 0.50:
        classified_modules.append('General')
    else:
        classified_modules.append(modules[best_match_idx])


db['Module'] = classified_modules
db.to_excel('modules.xlsx',index = False)