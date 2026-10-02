import joblib, numpy as np, pandas as pd
from sklearn.metrics import confusion_matrix
COUT_FN, COUT_FP = 1000, 50          # fraude manquee / fausse alerte, en MAD
te = pd.read_csv('data/prepare/test.csv')
m = joblib.load('models/model.pkl')
proba = m.predict_proba(te.drop(columns='fraude'))[:, 1]    # probabilite de fraude
def cout(seuil):
    tn, fp, fn, tp = confusion_matrix(te['fraude'], (proba >= seuil).astype(int)).ravel()
    return COUT_FN * fn + COUT_FP * fp, fn, fp
print('seuil 0.50 :', cout(0.50))
# A COMPLETER : parcourir les seuils de 0.05 a 0.95 par pas de 0.01,
# trouver celui qui minimise le cout, et afficher cout, fraudes manquees, fausses alertes

seuils = np.arange(0.05, 0.951, 0.01)
meilleur_seuil = min(seuils, key=lambda s: cout(s)[0])
cout_min, fn_min, fp_min = cout(meilleur_seuil)

print(f"meilleur seuil : {meilleur_seuil:.2f}")
print(f"co?t : {cout_min} MAD | fraudes manqu?es : {fn_min} | fausses alertes : {fp_min}")
