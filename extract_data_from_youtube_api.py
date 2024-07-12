import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Chargement des variables d'environnement depuis le fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')  # Chemin vers le fichier .env
load_dotenv(dotenv_path)

# Récupération de la clé API YouTube depuis les variables d'environnement
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Vérification si la clé API est correctement chargée
if API_KEY is None:
    print("Erreur: Clé API YouTube non trouvée. Assurez-vous de la définir dans le fichier .env sous le nom YOUTUBE_API_KEY.")
    exit(1)  # Arrête le script avec un code d'erreur non nul

# Version de l'API YouTube à utiliser
API_VERSION = 'v3'

# Construction de l'objet YouTube en utilisant la clé API
youtube = build('youtube', API_VERSION, developerKey=API_KEY)

# Fonction pour obtenir les statistiques d'une chaîne YouTube
def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part='snippet, statistics',
        id=channel_id
    )
    response = request.execute()

    if response['items']:
        data = dict(
            channel_name=response['items'][0]['snippet']['title'],
            total_subscribers=response['items'][0]['statistics'].get('subscriberCount', 0),
            total_views=response['items'][0]['statistics'].get('viewCount', 0),
            total_videos=response['items'][0]['statistics'].get('videoCount', 0)
        )
        return data
    else:
        return None

# Chemin du fichier CSV contenant les données des chaînes YouTube
csv_file_path = "C:\\Users\\LENOVO\\Desktop\\projet\\youtube_data_united-kingdom.csv"

# Lecture du fichier CSV dans un DataFrame pandas
df = pd.read_csv(csv_file_path)

# Extraction des IDs de chaînes et suppression des doublons potentiels
channel_ids = df['NOMBRE'].str.split('@').str[-1].unique()

# Initialisation d'une liste pour stocker les statistiques des chaînes
channel_stats = []

# Boucle sur les IDs de chaînes pour obtenir les statistiques de chaque chaîne
for channel_id in channel_ids:
    stats = get_channel_stats(youtube, channel_id)
    if stats is not None:
        channel_stats.append(stats)

# Conversion de la liste de statistiques en un DataFrame pandas
stats_df = pd.DataFrame(channel_stats)

# Réinitialisation de l'index des DataFrames
df.reset_index(drop=True, inplace=True)
stats_df.reset_index(drop=True, inplace=True)

# Concaténation des DataFrames horizontalement
combined_df = pd.concat([df, stats_df], axis=1)

# Suppression de la colonne 'channel_name' de stats_df (puisque 'NOMBRE' existe déjà)
# combined_df.drop('channel_name', axis=1, inplace=True)

# Sauvegarde du DataFrame combiné dans un fichier CSV
output_csv_path = 'C:/Users/LENOVO/Desktop/projet/updated_youtube_data_uk.csv'
combined_df.to_csv(output_csv_path, index=False)

# Affichage des 10 premières lignes du DataFrame combiné
print(combined_df.head(10))

