# Guide de déploiement sur Render

## Vue d'ensemble

Render est une plateforme cloud gratuite et facile à utiliser pour héberger des services web. Ce guide vous aidera à déployer votre API FastAPI EMSI ClassFlow sur Render.

## Prérequis

1. Un compte GitHub avec votre projet pushé
2. Un compte Render (gratuit) sur https://render.com
3. Votre URL de base de données PostgreSQL (Supabase)

## Étapes de déploiement

### Étape 1: Préparer votre repository GitHub

1. **Créez un nouveau repository** sur GitHub (ou utilisez un existant)
2. **Pushez votre code** local vers GitHub:

```bash
git init
git remote add origin https://github.com/votre-username/EmsiClassFlowBackEnd.git
git add .
git commit -m "Initial commit - EMSI ClassFlow API"
git branch -M main
git push -u origin main
```

### Étape 2: Créer un service sur Render

1. **Allez sur** https://render.com
2. **Connectez-vous** avec votre compte GitHub
3. **Cliquez** sur "New +" → "Web Service"
4. **Sélectionnez** votre repository GitHub `EmsiClassFlowBackEnd`
5. **Remplissez les détails:**

| Champ | Valeur |
|-------|--------|
| Name | `emsi-classflow-api` |
| Environment | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| Plan | Free (ou Pro selon vos besoins) |

### Étape 3: Configurer les variables d'environnement

1. **Dans le dashboard Render**, allez à "Environment"
2. **Ajoutez ces variables:**

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
PYTHONUNBUFFERED=true
PYTHON_VERSION=3.11
```

**Où obtenir DATABASE_URL:**
- Supabase: Allez dans Settings → Database → Connection String → URI
- PostgreSQL local: `postgresql://user:password@localhost:5432/dbname`

### Étape 4: Déployer

1. **Cliquez** sur "Create Web Service"
2. Render va automatiquement:
   - Cloner votre repository
   - Installer les dépendances
   - Lancer votre application
3. **Attendez** 2-5 minutes que le déploiement se termine
4. **Votre API sera accessible** à: `https://emsi-classflow-api.onrender.com`

## Fichiers importants pour Render

### ✅ `requirements.txt`
Déjà créé - contient toutes les dépendances Python

### ✅ `build.sh` (Optionnel)
Script de construction personnalisé (créé pour vous)

### ✅ `render.yaml` (Optionnel)
Configuration IaC pour Render (créée pour vous)

## Vérifier que tout fonctionne

Une fois déployé, testez votre API:

```bash
# Test basic endpoint
curl https://emsi-classflow-api.onrender.com/

# Test health check
curl https://emsi-classflow-api.onrender.com/health

# Accès à la documentation
https://emsi-classflow-api.onrender.com/docs
```

## Configuration avancée

### Gérer les secrets sensibles

**Ne mettez JAMAIS** les mots de passe directement dans votre code. Utilisez les variables d'environnement:

1. **Dans Render Dashboard:**
   - Allez à "Environment"
   - Ajoutez vos variables secrètes
   - Cochez "Secret" pour les données sensibles

2. **Dans votre code** (déjà inclus):
```python
import os

DATABASE_URL = os.getenv("DATABASE_URL")
```

### Optimiser la base de données

Pour une meilleure performance avec Supabase:

1. **Ajoutez** `pool_pre_ping=True` dans `database.py` (déjà fait ✓)
2. **Limitez** le nombre de connexions concurrent
3. **Utilisez** des indexes sur vos tables les plus interrogées

### Logs et monitoring

1. **Allez** sur votre service Render
2. **Cliquez** sur "Logs" pour voir les erreurs et activité
3. **Configurez** des alertes de crash
4. **Vérifiez** les performances dans le dashboard

## Dépannage

### "Module not found" error
```
Solution: Vérifiez que requirements.txt contient toutes les dépendances
pip freeze > requirements.txt
```

### "Connection refused" sur la base de données
```
Solution: Vérifiez que DATABASE_URL est correct et accessible
- Testez la connexion localement
- Vérifiez les IP whitelist sur Supabase/PostgreSQL
```

### Port 8000 non accessible
```
Solution: Render utilise automatiquement le port 10000
Utilisez: --port 8000 dans la commande de démarrage
```

### La base de données n'initialise pas les tables
```
Solution: Ajouter une commande de migration après build:
1. Installez Alembic: pip install alembic
2. Créez les migrations
3. Ajoutez dans build.sh: alembic upgrade head
```

## Alternatives et options premium

### Plan gratuit (Free)
- ✓ Idéal pour développement/test
- ✗ Arrête après 15 minutes d'inactivité
- ✗ Démarrage lent (~30s)
- Parfait pour votre cas

### Plan Starter ($7/mois)
- ✓ Disponible 24/7
- ✓ Redémarrages automatiques
- ✓ Plus de ressources

### Alternatives à Render
- **Heroku** (payant, très cher)
- **Railway** (gratuit avec crédit)
- **Vercel** (serverless, payant)
- **Azure** (gratuit 12 mois)
- **Google Cloud Run** (gratuit avec limites)

## Configuration pour production

Si vous passez en production:

```python
# Dans app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://votre-domaine.com",
        "https://www.votre-domaine.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Domaine personnalisé (Optional)

1. **Achetez** un domaine sur Namecheap, GoDaddy, etc.
2. **Dans Render Dashboard:**
   - Allez à "Settings" → "Custom Domain"
   - Suivez les instructions pour configurer le DNS
3. **Votre API sera accessible** à: `https://api.votre-domaine.com`

## Mise à jour et redéploiement

Render redéploie automatiquement à chaque push sur GitHub:

```bash
git add .
git commit -m "Update description"
git push origin main
```

Render automatiquement:
1. Détecte le changement
2. Récupère le nouveau code
3. Reconstruit l'image
4. Redéploie

## Support et ressources

- **Documentation Render**: https://render.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **PostgreSQL avec Render**: https://render.com/docs/databases

## Checklist final avant déploiement

- [ ] Code sur GitHub
- [ ] `requirements.txt` à jour
- [ ] `DATABASE_URL` configurée
- [ ] Variables d'environnement sensibles ajoutées
- [ ] `build.sh` présent
- [ ] Endpoints testés localement
- [ ] `.env` file dans `.gitignore`
- [ ] Production CORS configuré

---

**Besoin d'aide?** Consultez les logs Render ou contactez support@render.com
