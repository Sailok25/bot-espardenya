import discord
from discord import app_commands
from discord.ext import commands
import datetime

# Importacions propies
from config import DISCORD_TOKEN, ID_CANAL_REDACCIONS, COMMAND_PREFIX, REDACCIONS_FILE
from utils.data_handler import carregar_dades, guardar_dades

# Configuración d'intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Crear bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Carregar dades
redaccions = carregar_dades(REDACCIONS_FILE)

@bot.event
async def on_ready():
    print(f'Bot connectat com {bot.user} exitósament!')
    
    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)} comandes sincronitzades')
    except Exception as e:
        print(f'Error sincronitzant comandaments: {e}')

@bot.tree.command(name="redaccio", description="Assigna una redacció a un usuari")
@app_commands.describe(usuari="Usuari", rao="Raó de la redacció")
async def redaccio(interaction: discord.Interaction, usuari: discord.Member, rao: str):
    # Verificar si hay canal configurado
    if ID_CANAL_REDACCIONS == 0:
        await interaction.response.send_message(
            "No s'ha configurat el canal de redaccions. Configura ID_CANAL_REDACCIONS al fitxer .env",
            ephemeral=True
        )
        return
    
    # 1. Crear ID
    id_redaccio = len(redaccions) + 1
    
    # 2. Crear embed per al canal amb informació de la redacció
    embed = discord.Embed(
        title=f"Redacció #{id_redaccio}",
        description="S'ha dictat una nova redacció a un membre espardenya.",
        color=discord.Color.red()
    )
    embed.add_field(name="Usuari", value=usuari.mention, inline=True)
    embed.add_field(name="Motiu de la redacció", value=rao, inline=False)
    
    hora = datetime.datetime.now().strftime("Avui a les %H:%M")
    embed.set_footer(text=f"Dictada per {interaction.user.name} • {hora}")
    
    # 3. Enviar el embed al canal de redaccions
    canal = bot.get_channel(ID_CANAL_REDACCIONS)
    if canal:
        await canal.send(embed=embed)
    else:
        await interaction.response.send_message(
            f"No s'ha trobat el canal amb ID {ID_CANAL_REDACCIONS}",
            ephemeral=True
        )
        return
    
    # 4. Guardar la redacció en un fitxer .json
    nova_redaccio = {
        "id": id_redaccio,
        "usuari": str(usuari),
        "usuari_id": usuari.id,
        "rao": rao,
        "per": interaction.user.name,
        "per_id": interaction.user.id,
        "data": datetime.datetime.now().isoformat()
    }
    redaccions.append(nova_redaccio)
    guardar_dades(REDACCIONS_FILE, redaccions)
    
    # 5. Respondre a l'usuari que ha dictat la redacció si ha anat bé
    await interaction.response.send_message(
        f"Redacció #{id_redaccio} creada per a l'{usuari.mention} amb éxit.", 
        ephemeral=True
    )

@bot.tree.command(name="historial", description="Mostra l'historial de redaccions")
async def historial_redaccions(interaction: discord.Interaction):
    if not redaccions:
        await interaction.response.send_message(
            "No hi ha redaccions al sistema.",
            ephemeral=True
        )
        return
    
    # Mostrar les últimes 10 redaccions
    ultimes = redaccions[-10:] if len(redaccions) > 10 else redaccions
    
    embed = discord.Embed(
        title="Historial de Redaccions",
        color=discord.Color.blue()
    )
    
    for r in reversed(ultimes):  # Mostrar les més recents primer
        data_obj = datetime.datetime.fromisoformat(r['data'])
        data_format = data_obj.strftime("%d/%m/%Y %H:%M")
        
        embed.add_field(
            name=f"#{r['id']} - {r['usuari']}",
            value=f"**Motiu:** {r['rao'][:100]}\n**Per:** {r['per']}\n**Data:** {data_format}",
            inline=False
        )
    
    embed.set_footer(text=f"Total: {len(redaccions)} redaccions")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="borrar_redaccio", description="Elimina una redacció per ID")
@app_commands.describe(id_redaccio="ID de la redacció a eliminar")
async def borrar_redaccio(interaction: discord.Interaction, id_redaccio: int):
    global redaccions
    
    for i, r in enumerate(redaccions):
        if r["id"] == id_redaccio:
            # Eliminar
            redaccions.pop(i)
            guardar_dades(REDACCIONS_FILE, redaccions)
            
            await interaction.response.send_message(
                f"Redacció #{id_redaccio} eliminada correctament.",
                ephemeral=True
            )
            return
    
    await interaction.response.send_message(
        f"No s'ha trobat cap redacció amb el #{id_redaccio}",
        ephemeral=True
    )

# Maneig d'errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tens permisos per executar aquesta comanda.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"Error: {error}")

# Executar bot
if __name__ == "__main__":
    if DISCORD_TOKEN is None:
        print("ERROR: No s'ha trobat DISCORD_TOKEN al fitxer .env")
        print("Crea un fitxer .env amb les teves credencials o si ja el tens, actualitza'l.")
    elif ID_CANAL_REDACCIONS == 0:
        print("AVÍS: ID_CANAL_REDACCIONS no està configurat o és 0")
        print("Configura'l al fitxer .env")
        bot.run(DISCORD_TOKEN)
    else:
        bot.run(DISCORD_TOKEN)