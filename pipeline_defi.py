import subprocess, json, yaml, sys, mlflow

BINOME = sys.argv[1]
P = yaml.safe_load(open("params.yaml"))

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("defi-tp2")

with mlflow.start_run(run_name=BINOME):
    for etape in ["preparer", "entrainer", "evaluer", "mesurer"]:
        subprocess.run(["python", f"src/{etape}.py"], check=True)

    mets = json.load(open("reports/metrics.json"))
    mes = json.load(open("reports/mesures.json"))
    ok = (
        mes["taille_mo"] <= P["defi"]["taille_max_mo"]
        and mes["latence_ms"] <= P["defi"]["latence_max_ms"]
    )

    mlflow.log_params(P["entrainement"])
    mlflow.log_metrics({**mets, **mes})
    mlflow.set_tags({
        "binome": BINOME,
        "contraintes": "ok" if ok else "hors-contraintes"
    })
    print(
        f"{BINOME} : F1 {mets['f1']} | {mes['taille_mo']} Mo "
        f"| {mes['latence_ms']} ms | contraintes "
        f"{'OK' if ok else 'NON respectees'}"
    )
