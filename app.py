from flask import Flask, render_template, request, jsonify
import json
import os
import mysql.connector

app = Flask(__name__)

# Configuration de la base de données
db_config = {
    'user': 'root',
    'password': 'AYLIIIINA47',
    'host': 'localhost',
    'database': 'stage',
    'port': 3306
}

def test_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Version de MySQL : {version[0]}")
    except mysql.connector.Error as err:
        print(f"Erreur de connexion : {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_id_from_table(table, column, value):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = f"SELECT id{table} FROM {table} WHERE {column} = %s"
        print(f"Exécution de la requête SQL : {query} avec la valeur : '{value}'")
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        print(f"Résultat de la requête : {result}")
        if result:
            return result[0]
        else:
            print(f"Aucun résultat trouvé pour {column} = '{value}' dans {table}")
            return None
    except mysql.connector.Error as err:
        print(f"Erreur de base de données : {err}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/')
def index():
    return render_template('page2.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    print(f"Données reçues : {data}")
    
    nom_prenom = data.get('Nom et Prénom', '').strip()
    print(f"Nom et Prénom (nettoyé) : '{nom_prenom}'")

    # Assurez-vous que le nom de la colonne est correct
    id_employe = get_id_from_table('employe', 'nomcomplet', nom_prenom)
    print(f"ID Employé trouvé : {id_employe}")

    id_groupe = get_id_from_table('groupe', 'Groupeeng', data.get('groupeResponsable'))
    id_statut = get_id_from_table('statue', 'namestatue', data.get('statut'))
    
    claims = []
    index = 0
    while f'titre{index}' in data or f'titre{index}.5' in data:
        claim_data = {
            "dateCreation": data.get("dateCreation", ""),
            "idEmployé": id_employe,  # Utilise l'ID récupéré
            "idGroupe": id_groupe,    # Utilise l'ID récupéré
            "idStatut": id_statut,    # Utilise l'ID récupéré
            "titre": data.get(f'titre{index}', ''),
            "contenu": data.get(f'contenu{index}', ''),
            "visionNext": data.get(f'visionNext{index}', ''),
            "visionCurrent": data.get(f'visionCurrent{index}', ''),
            "duration": data.get(f'duration{index}', ''),
            "public": data.get(f'public{index}', '')
        }
        claims.append(claim_data.copy())
        
        if f'titre{index}.5' in data:
            claim_data.update({
                "titre": data.get(f'titre{index}.5', ''),
                "contenu": data.get(f'contenu{index}.5', ''),
                "visionNext": data.get(f'visionNext{index}.5', ''),
                "visionCurrent": data.get(f'visionCurrent{index}.5', ''),
                "duration": data.get(f'duration{index}.5', ''),
                "public": data.get(f'public{index}.5', '')
            })
            claims.append(claim_data.copy())
        
        index += 1

    # Sauvegarder chaque réclamation dans un fichier JSON individuel
    output_dir = 'data/entries'
    os.makedirs(output_dir, exist_ok=True)
    
    for i, claim in enumerate(claims):
        file_name = f'entry_{i + 1}.json'
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(claim, file, ensure_ascii=False, indent=4)

    return jsonify({"status": "success", "message": "Formulaire soumis avec succès"}), 200

if __name__ == '__main__':
    # Tester la connexion à la base de données avant de démarrer l'application
    test_connection()
    app.run(debug=True)
