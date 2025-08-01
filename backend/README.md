# NumiViz Backend API

Backend API pour la plateforme d'éducation mathématique interactive NumiViz.

## 🏗️ Architecture

### Base de données SQLite
- **Aucune installation serveur nécessaire** : la base est un simple fichier local (`numiviz.db`).
- **Le fichier de base de données est créé automatiquement** au premier lancement.
- **Vous pouvez l'ouvrir/éditer avec [DB Browser for SQLite](https://sqlitebrowser.org/)**.

### Technologies
- **FastAPI** : Framework web moderne
- **SQLite** : Base de données légère, intégrée à Python
- **Pydantic** : Validation de données
- **JWT** : Authentification sécurisée
- **Manim** : Génération d'animations mathématiques

## 🚀 Installation

### 1. Prérequis
```bash
# Installer Python 3.8+
python --version
```

### 2. Configuration de l'environnement
```bash
# (Optionnel) Copier le fichier d'exemple si besoin
# copy env_example.txt .env
# Modifier .env si vous souhaitez changer le nom du fichier DB (SQLITE_DB_PATH)
```

### 3. Installation des dépendances
```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
# Démarrer le serveur
python main.py

# Ou avec uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### Authentification
- `POST /api/auth/register` - Inscription d'un nouvel utilisateur
- `POST /api/auth/login` - Connexion utilisateur

### Utilisateurs
- `GET /api/users/me` - Informations de l'utilisateur connecté
- `PUT /api/users/me` - Mise à jour du profil

### Modules (Enseignants)
- `POST /api/modules` - Créer un module
- `GET /api/modules` - Lister les modules
- `GET /api/modules/{module_id}` - Détails d'un module
- `PUT /api/modules/{module_id}` - Modifier un module

### Leçons (Enseignants)
- `POST /api/lessons` - Créer une leçon
- `GET /api/modules/{module_id}/lessons` - Leçons d'un module

### Exercices (Enseignants)
- `POST /api/exercises` - Créer un exercice
- `GET /api/modules/{module_id}/exercises` - Exercices d'un module
- `GET /exercises/filter?chapter=...&tp=...` - Exercices filtrés par chapitre et TP

### Progression (Étudiants)
- `POST /api/progress` - Enregistrer la progression
- `GET /api/progress` - Consulter sa progression

### Tableau de bord (Enseignants)
- `GET /api/teacher/dashboard` - Statistiques et progrès des étudiants

### Visualisations
- `POST /api/plot/function` - Générer un graphique
- `POST /api/animation/generate` - Générer une animation

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

### Inscription
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "John Doe",
    "email": "john@example.com",
    "mot_de_passe": "password123",
    "role": "etudiant"
  }'
```

### Connexion
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Utilisation du token
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 👥 Rôles Utilisateurs

### Étudiant
- Consulter les modules
- Suivre les leçons
- Répondre aux exercices
- Voir sa progression

### Enseignant
- Créer et modifier des modules
- Créer des leçons et exercices
- Consulter les progrès des étudiants
- Accéder au tableau de bord

### Administrateur
- Tous les droits des enseignants
- Gestion des utilisateurs
- Configuration de la plateforme

## 📊 Structure de la Base de Données (SQLite)

- Le fichier de base de données est `numiviz.db` (modifiable via `.env`)
- Les tables sont créées automatiquement au premier lancement
- Structure simplifiée :

| Table                  | Champs principaux                                  |
|------------------------|----------------------------------------------------|
| utilisateur            | id_utilisateur, nom, email, mot_de_passe, role...  |
| module                 | id_module, titre, type, description, contenu...    |
| lecon                  | id_lecon, titre, contenu, id_module, id_enseignant |
| exercice               | id_exercice, question, solution, feedback, ...     |
| visualisation          | id_visualisation, type, parametres, ...            |
| progression_etudiant   | id_progression, id_etudiant, id_module, statut...  |
| session_etude          | id_session, id_etudiant, id_module, duree_totale...|

## 🛠️ Développement

### Structure des fichiers
```
backend/
├── main.py              # Point d'entrée FastAPI
├── database.py          # Configuration base de données SQLite
├── models.py            # Modèles Pydantic
├── services.py          # Logique métier
├── requirements.txt     # Dépendances Python
├── .env                 # Configuration (optionnelle)
└── README.md            # Documentation
```

### Tests
```bash
# Installer pytest
pip install pytest

# Lancer les tests
pytest
```

### Documentation API
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔧 Configuration

### Variables d'environnement
- `SQLITE_DB_PATH` (optionnel) : chemin du fichier base de données (par défaut `numiviz.db`)
- `JWT_SECRET` : Clé secrète pour JWT
- `DEBUG` : Mode debug (True/False)

### Sécurité
- Mots de passe hashés avec SHA-256
- Tokens JWT avec expiration
- Validation des données avec Pydantic
- Gestion des rôles et permissions

## 🚀 Déploiement

### Production
```bash
# Installer gunicorn
pip install gunicorn

# Lancer en production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker (optionnel)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Notes

- L'API est conçue pour être scalable et maintenable
- Tous les endpoints sont documentés avec Swagger
- La validation des données est automatique avec Pydantic
- Les erreurs sont gérées de manière cohérente
- Le système de progression permet un suivi détaillé des étudiants

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.
