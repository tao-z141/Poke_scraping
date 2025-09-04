# Objectif
Ce Tp permet de **scraper toutes les images Pokémon depuis Bulbapedia** et de les stocker dans un **bucket S3** organisé par génération (`images/Generation_I/...`).  

---

## Prérequis
1. Un compte AWS avec :  
   - Un utilisateur IAM avec permissions `s3:PutObject` sur le bucket.  
   - Un bucket S3 (ex : `pokescrape`)

2. Une instance **EC2 (Ubuntu 22.04)**  
 
---

## Installation sur EC2

### 1. Mise à jour du système
```bash
sudo apt update && sudo apt upgrade -y
```
### 2. Installer Python et pip
```bash
sudo apt install -y python3 python3-pip
```
### 3. Installer les bibliothèques 
```bash
pip3 install requests beautifulsoup4 boto3
```
### Configurer les identifiants AWS 
```bash
aws configure
```
## Exécution du script
```bash
python3 scraper.py
```

## Le script :
```bash
Télécharge les images Pokémon depuis Bulbapedia.

Classe les fichiers localement par génération.

Uploade chaque image dans ton bucket S3 (dans images/Generation_I/...)
```

