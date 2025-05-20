# Application Flutter de Gestion de Troupeaux

Cette application mobile Flutter permet de gérer des troupeaux d'animaux, leurs sites et leurs visites. Elle se connecte à l'API BackEndAnim.

## Fonctionnalités

- **Authentification** : Inscription et connexion des utilisateurs
- **Gestion des troupeaux** : Création, modification et suppression de troupeaux
- **Gestion des moutons** : Suivi des animaux par troupeau (race, sexe, âge, couleur)
- **Gestion des sites** : Localisation des sites de pâturage avec coordonnées GPS
- **Visualisation cartographique** : Affichage des sites sur une carte
- **Suivi des visites** : Enregistrement des visites effectuées sur chaque site

## Configuration

1. Assurez-vous d'avoir Flutter installé sur votre machine
2. Clonez ce dépôt
3. Créez un fichier `.env` à la racine du projet avec le contenu suivant :
   ```
   API_URL=http://votre-api-url:port
   ```
4. Exécutez `flutter pub get` pour installer les dépendances
5. Lancez l'application avec `flutter run`

## Structure du projet

```
lib/
├── main.dart                # Point d'entrée de l'application
├── models/                  # Modèles de données
│   ├── flock.dart           # Modèle de troupeau
│   ├── sheep.dart           # Modèle de mouton
│   ├── site.dart            # Modèle de site
│   ├── user.dart            # Modèle d'utilisateur
│   └── visit.dart           # Modèle de visite
├── providers/               # Gestion d'état avec Provider
│   ├── auth_provider.dart   # Gestion de l'authentification
│   └── flock_provider.dart  # Gestion des troupeaux
├── screens/                 # Écrans de l'application
│   ├── login_screen.dart    # Écran de connexion
│   ├── register_screen.dart # Écran d'inscription
│   ├── home_screen.dart     # Écran principal
│   └── ...                  # Autres écrans
├── services/                # Services pour les appels API
│   ├── api_service.dart     # Service de base pour les appels HTTP
│   ├── auth_service.dart    # Service d'authentification
│   └── ...                  # Autres services
└── widgets/                 # Widgets réutilisables
```

## Dépendances principales

- **http**: Pour les appels API REST
- **provider**: Pour la gestion d'état
- **flutter_secure_storage**: Pour le stockage sécurisé du token d'authentification
- **flutter_map**: Pour l'affichage des cartes
- **intl**: Pour le formatage des dates
- **flutter_dotenv**: Pour la gestion des variables d'environnement

## API BackEndAnim

Cette application se connecte à l'API BackEndAnim qui fournit les endpoints suivants :

- `/auth` : Authentification (login, token)
- `/user` : Gestion des utilisateurs
- `/flocks` : Gestion des troupeaux
- `/sheep` : Gestion des moutons
- `/sites` : Gestion des sites
- `/visits` : Gestion des visites

## Développement

Pour contribuer au développement :

1. Créez une branche pour votre fonctionnalité
2. Développez et testez votre code
3. Soumettez une pull request

## Licence

Ce projet est sous licence MIT.

