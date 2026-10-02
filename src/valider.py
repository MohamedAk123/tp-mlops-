import sys
import pandas as pd

fichier = sys.argv[1] if len(sys.argv) > 1 else "data/transactions.csv"
df = pd.read_csv(fichier)
erreurs = []

colonnes = {"montant", "anciennete", "freq_24h", "nuit", "fraude"}
absentes = colonnes - set(df.columns)

if absentes:
    erreurs.append(f"colonnes absentes : {sorted(absentes)}")
else:
    nb_vides = int(df[list(colonnes)].isna().sum().sum())
    if nb_vides:
        erreurs.append(f"valeurs manquantes : {nb_vides}")

    nb_montants = int((df["montant"] <= 0).sum())
    if nb_montants:
        erreurs.append(f"montants <= 0 : {nb_montants} lignes")

    if not df["nuit"].isin([0, 1]).all():
        erreurs.append("nuit doit valoir 0 ou 1")

    if (df["freq_24h"] < 1).any():
        erreurs.append("freq_24h doit être >= 1")

    taux = df["fraude"].mean()
    if not 0.01 <= taux <= 0.50:
        erreurs.append(f"taux de fraude hors limites : {taux:.1%}")

if erreurs:
    print("VALIDATION ECHOUEE")
    for erreur in erreurs:
        print(" -", erreur)
    sys.exit(1)

print(f"validation OK : {len(df)} lignes, taux de fraude {df['fraude'].mean():.1%}")
