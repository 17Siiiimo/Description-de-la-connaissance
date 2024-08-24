import mysql.connector
import json
import os

# Connexion à la base de données
cnx = mysql.connector.connect(
    user='root',
    password='AYLIIIINA47',
    host='localhost',
    database='stage'
)
cursor = cnx.cursor()

# Requête d'insertion mise à jour sans la colonne connaissancecol
query = """
    INSERT INTO connaissance (
        idEmployé,
        idGroupe,
        idStatut,
        dateCreation,
        Titre,
        Contenu,
        `Titre de la prochaine vision`,
        `Titre de la vision`,
        `Durée limite`,
        Public
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

json_directory = r'C:\Users\Pks\Desktop\STAGE\data\entries'

for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)
        
        print(f"Traitement du fichier: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                print(f"Contenu du fichier JSON: {data}")
                
                # Préparation des valeurs à insérer
                values = (
                    data.get("idEmployé"),
                    data.get("idGroupe"),
                    data.get("idStatut"),
                    data.get("dateCreation"),
                    data.get("titre"),
                    data.get("contenu"),
                    data.get("visionNext"),
                    data.get("visionCurrent"),
                    data.get("duration"),
                    data.get("public")
                )
                
                # Exécution de la requête d'insertion
                cursor.execute(query, values)
                cnx.commit()
                print(f"Données insérées: {values}")
                
            except json.JSONDecodeError as e:
                print(f"Erreur lors de la lecture du fichier JSON {file_path}: {e}")
            except mysql.connector.Error as e:
                print(f"Erreur MySQL lors de l'insertion des données: {e}")

# Fermeture de la connexion
cursor.close()
cnx.close()
