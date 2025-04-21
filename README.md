# Darba Uzskaites Sistēma

## Instelācija
1. Klonēt repositoriju:
   ```bash
   git clone https://github.com/yourusername/DAR-main.git
   cd DAR-main

2. Instalēt atkarības:
   ```bash
   pip install -r requirements.txt

3. Iestatīt datubāzi:
   * Instalēt MySQL/MariaDB

   * Izveidot datubāzes lietotāju

   * Atjaunināt .env failu ar jūsu informāciju

4. Inicializēt datubāzi:
   ```bash
   python create_admin.py

## Izmantošana
* Windows - izmantot launch.bat
* Linux - izmantot launch.sh

## Konfigurācija
Kopēt .env.example uz .env un pamainīt:
   ```ini
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_PORT=3306

## Administratora pieja
Pamata administratora informācija
* Lietotājvārds: admin
* Parole: admin123

Lai pamainītu administratora paroli un vārdu, jāpalaiž create_admin.py konsolē
   ```cmd
   python create_admin.py
