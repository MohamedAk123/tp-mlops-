import os, json, time, statistics, joblib, pandas as pd
m = joblib.load('models/model.pkl')
X = pd.read_csv('data/prepare/test.csv').drop(columns='fraude')
taille = os.path.getsize('models/model.pkl') / 1e6          # taille en Mo
m.predict(X)                                                # premier appel : chauffe
t = []
for _ in range(20):                                         # 20 mesures, on garde la mediane
    d = time.perf_counter(); m.predict(X); t.append((time.perf_counter() - d) * 1000)
latence = statistics.median(t)                              # ms pour les 1 250 lignes
json.dump({'taille_mo': round(taille, 2), 'latence_ms': round(latence, 1)},
          open('reports/mesures.json', 'w'), indent=2)
print(f'taille : {taille:.2f} Mo | latence : {latence:.1f} ms pour {len(X)} lignes')
