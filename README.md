1. Vérifier que le service est bien déployé

Dans Cloud Run, vérifier que le api-satisfaction est bien actif et récupérer son URL.

2. Tester l'API

Tu peux envoyer une requête comme celle-ci :

curl -X POST "https://api-satisfaction-913270433936.europe-west1.run.app/predict" -H "Content-Type: application/json" -d '{"text":"service excellent"}'

Tu devrais obtenir une réponse du type :
json
{
  "sentiment": "positive",
  "score": 0.7809,
  "text": "service excellent"
}

Tu peux également tester avec un avis négatif :

curl -X POST "https://api-satisfaction-913270433936.europe-west1.run.app/predict" -H "Content-Type: application/json" -d '{"text":"service mauvais"}'

3. Vérifier les données dans BigQuery

Après chaque appel à l'API, une ligne est enregistrée dans la table :

dataset_gold_modeling.predictions_sentiment

Tu peux exécuter :

SELECT
    prediction_date,
    text,
    sentiment,
    score
FROM dataset_gold_modeling.predictions_sentiment
ORDER BY prediction_date DESC;

Les tests réalisés via l'API doivent apparaître dans les résultats.

4. Vérifier le comportement du score

Au départ, les scores étaient fixés manuellement (0.85 et 0.15). Maintenant ils sont calculés à partir du modèle lui-même, donc ils peuvent varier selon le texte envoyé.

5. Vérifier le code

Dans `main.py` :

* chargement du modèle MLflow ;
* endpoint `/predict` ;
* calcul du score ;
* insertion automatique dans BigQuery.

6. Vérifier le chargement du modèle

Dans main.py, le modèle est chargé directement depuis les artefacts MLflow intégrés dans le dossier model.

L'API utilise maintenant le vrai modèle SVM et non plus une logique codée en dur.

7. Vérifier le CI/CD

J'ai également testé toute la chaîne de déploiement automatique.

Pour vérifier :

faire une petite modification dans le dépôt GitHub
faire un commit et un push sur la branche principale
aller dans Cloud Build.

Le trigger doit se lancer automatiquement.

Le pipeline exécute ensuite :

GitHub
→ Cloud Build
→ Build de l'image Docker
→ Push dans Artifact Registry
→ Déploiement Cloud Run

Une fois le build terminé en succès, une nouvelle révision Cloud Run est créée automatiquement.

5. Vérifier le déploiement

Dans Cloud Run, vérifier que la dernière révision est bien active puis refaire un test sur l'API.

L'objectif est de valider que toute la chaîne fonctionne correctement :

GitHub
→ Cloud Build
→ Docker
→ Artifact Registry
→ Cloud Run
→ API FastAPI
→ Modèle SVM
→ BigQuery
