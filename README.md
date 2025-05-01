# Epic Events : Projet d'école [OpenClassroom](https://openclassrooms.com/fr)

Epic Events est une application web de gestion d'événements permettant la gestion des clients, contrats et événements. Ce projet est conçu pour être exécuté localement dans le terminal.

## Architecture Logicielle MVC

Le projet suit le pattern d'architecture MVC (Modèle-Vue-Contrôleur), un design pattern qui sépare l'application en trois composants principaux :

### 1. Modèle (Models)
- Représente les données et la logique métier
- Gère la persistance des données avec SQLAlchemy
- Définit les modèles de données (clients, contrats, événements, utilisateurs)
- Exemple : `models/sql_models.py` définit la structure de la base de données

### 2. Vue (Views)
- Gère l'affichage et l'interaction avec l'utilisateur
- Interface en ligne de commande (CLI)
- Présente les données et collecte les entrées utilisateur
- Exemple : `views/client_view.py` gère l'affichage des informations clients

### 3. Contrôleur (Controllers)
- Fait le lien entre le Modèle et la Vue
- Traite les requêtes de l'utilisateur
- Applique la logique métier
- Exemple : `controllers/client_controller.py` gère les opérations sur les clients

### Services Transversaux
En plus de l'architecture MVC, le projet utilise des services transversaux :
- `auth.py` : Gestion de l'authentification et des sessions
- `permission.py` : Système de permissions basé sur les rôles
- `database.py` : Configuration et gestion de la base de données

Cette architecture permet :
- Une séparation claire des responsabilités
- Une meilleure maintenabilité du code
- Une facilité de test
- Une évolutivité du système

## Installation et exécution

Suivez les étapes ci-dessous pour installer et exécuter le projet Epic Events localement.

### Prérequis

- Python 3.9 ou version ultérieure
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt** :
   ```bash
   git clone [URL_DU_REPO]
   cd epic_event
   ```

2. **Créer un environnement virtuel** :
   Sous Windows :
   ```bash
   python -m venv env
   env\Scripts\activate
   ```
   Sous macOS/Linux :
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données** :
   - Assurez-vous que le fichier `.env` contient la configuration de la base de données :
     ```
     DATABASE_URL=sqlite:///epicevents.db
     ```
   - La base de données sera automatiquement créée lors du premier lancement de l'application

5. **Lancer l'application** :
   ```bash
   python main.py
   ```

## Comptes de test

Voici les différents comptes disponibles pour tester l'application :

### Équipe Gestion
- **Admin** :
  - Username : `the_admin`
  - Mot de passe : `secret2025!`
  - Rôle : admin

- **Manager** :
  - Username : `the_manager`
  - Mot de passe : `secret2025!`
  - Rôle : manager

  - Username : `secret`
  - Mot de passe : `secret1234`
  - Rôle : manager

### Équipe Commerciale
- **Sailors** :
  - Username : `the_sailor`
  - Mot de passe : `secret2025!`
  - Rôle : sailor

  - Username : `test_create_sailor`
  - Mot de passe : `test1234`
  - Rôle : sailor

### Équipe Support
- **Support** :
  - Username : `the_support`
  - Mot de passe : `secret2025!`
  - Rôle : support

## Scénarios de test

### 1. Gestion des clients
- **Équipe Gestion** :
  - Créer 2 nouveaux sailors
  - Créer 2 nouveaux supports

- **Sailor 1** :
  - Créer 2 nouveaux clients
  - Peut modifier les informations de ses clients

- **Sailor 2** :
  - Tenter de mettre à jour un client dont il n'est pas responsable
  - Vérifier que l'accès est refusé

### 2. Gestion des contrats
- **Équipe Gestion** :
  - Créer 2 nouveaux contrats
  - Peut modifier les contrats

- **Sailor 1** :
  - Mettre à jour les contrats de ses clients
  - Créer un événement pour un client ayant signé un contrat
  - Tenter de créer un événement pour un client sans contrat (doit échouer)

- **Sailor 2** :
  - Tenter de mettre à jour un contrat d'un client dont il n'est pas responsable
  - Vérifier que l'accès est refusé

### 3. Gestion des événements
- **Équipe Gestion** :
  - Mettre à jour un événement pour associer un support

- **Support 1** :
  - Mettre à jour uniquement les événements dont il est responsable

- **Support 2** :
  - Tenter de mettre à jour un événement dont il n'est pas responsable
  - Vérifier que l'accès est refusé

## Structure du projet

```
epic_event/
├── controllers/              # Contrôleurs de l'application
│   ├── client_controller.py  # Gestion des clients
│   ├── contract_controller.py # Gestion des contrats
│   ├── event_controller.py   # Gestion des événements
│   └── user_controller.py    # Gestion des utilisateurs
├── views/                    # Vues de l'application
│   ├── auth_view.py         # Authentification
│   ├── client_view.py       # Interface clients
│   ├── contract_view.py     # Interface contrats
│   ├── event_view.py        # Interface événements
│   ├── main_menu.py         # Menu principal
│   └── user_view.py         # Interface utilisateurs
├── models/                   # Modèles de données
│   └── sql_models.py        # Modèles SQL
├── migrations/              # Scripts de migration
├── auth.py                  # Authentification et permissions
├── database.py              # Configuration de la base de données
├── init_roles.py           # Initialisation de la base de données
├── main.py                 # Point d'entrée de l'application
├── permission.py           # Gestion des permissions
├── requirements.txt        # Dépendances Python
└── .env                    # Variables d'environnement
```

## Fonctionnalités principales

- Gestion des utilisateurs avec différents rôles (admin, manager, sailor, support)
- Gestion des clients et de leurs contrats
- Gestion des événements
- Système de permissions basé sur les rôles
- Interface en ligne de commande
