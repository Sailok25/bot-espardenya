# 🤖 Bot de Redaccions per Discord
Bot de Discord creat per gestionar les redaccions assignades als membres del servidor.

## ✨ Funcionalitats
- 📝 Assignar redaccions a usuaris amb un motiu
- 📚 Veure l'històric de redaccions
- 🗑️ Eliminar redaccions per ID

## 🎮 Comandes
- `/redaccio @usuari motiu` - Assigna una redacció
- `/historial` - Mostra les últimes redaccions
- `/borrar_redaccio id` - Elimina una redacció


## 🚀 Instal·lació

### 1. Prerequisits
- Python 3.8 o superior
- Token de bot de Discord

### 2. Configuració

```bash
# 1. Clonar el repositori
git clone https://github.com/tu-usuario/tu-bot-discord.git
cd tu-bot-discord

# 2. Crear entorn virtual (recomanat)
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Instal·lar dependències
pip install -r requirements.txt

# 4. Configurar variables d'entorn
cp .env.example .env
```

### 3. Configurar .env
Edita el fitxer .env amb:
```env
DISCORD_TOKEN=el_teu_token
ID_CANAL_REDACCIONS=el_teu_id
```

### 4. Obtenir credencials del bot
1. Ves a Discord Developer Portal

2. Crea una nova aplicació → "New Application"

3. Ves a "Bot" → "Add Bot"

4. Copia el token i posa'l a .env

5. Activa les següents opcións:
    - PRESENCE INTENT
    - SERVER MEMBERS INTENT
    - MESSAGE CONTENT INTENT

6. Invita el bot al teu servidor:
    - Ves a "OAuth2" → "URL Generator"
    - Selecciona: bot, applications.commands
    - Permisos: Send Messages, Read Messages/View Channels, Embed Links
    - Copia la URL i obre-la al navegador


## ⚠️ Notes importants
Les dades de cada redacció, es guarden a `data/redaccions.json`

Assegura't que el bot té permisos configurats per: __`LLEGIR`__ i __`ESCRIURE`__