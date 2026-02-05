import os
from dotenv import load_dotenv

# Carregar variables d'entorn
load_dotenv()

# Configuració del bot
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ID_CANAL_REDACCIONS = int(os.getenv('ID_CANAL_REDACCIONS', 0))
COMMAND_PREFIX = '/'

# Ruta del fitxer de redaccions
REDACCIONS_FILE = 'data/redaccions.json'

# Verificar configuració
if DISCORD_TOKEN is None:
    print("ADVERTENCIA: DISCORD_TOKEN no trobat al .env")
    print("Si no tens un fitxer .env, crea'l i ompla'l amb les teves credencials (mira el fitxer .env.example)")