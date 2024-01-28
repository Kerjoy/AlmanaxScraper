import discord
from discord.ext import commands
import urllib.request
import re
import datetime
from bs4 import BeautifulSoup
import requests
import asyncio

bot = commands.Bot(command_prefix='-', description= "Este es un DuckBot, al servicio del gremio")

sourceLinkAlmanax = 'http://www.krosmoz.com/es/almanax'
horaServidor = 16
minServidor = 1
token_access_discord = ''

@bot.command()
async def ayuda(ctx):
	print ("Enviado ayuda solicitada")

	mensaje = discord.Embed(title = "`Resiste, los patos van a tu rescate`", color=0xe5be01)
	mensaje.add_field(name="Busca en los dias de almanax: ", value="-balmanax ObjetoBuscar(Puede ser una cosa, zona etc, solo 1 palabra se buscara en toda la pagina.)", inline=False)
	mensaje.add_field(name="Almanax actual: ", value="-almanax", inline=False)
	mensaje.add_field(name="Almanax actualizado diario: ", value="Se envia puntualmente, automaticamente sin comandos.", inline=False)
	await ctx.send(embed = mensaje) 

	print("Envio de ayuda finalizada")

@bot.command()
async def almanax(ctx):
	print("Procesando almanax")

	source = requests.get(sourceLinkAlmanax).text
	soup = BeautifulSoup(source, 'lxml')

	mision = soup.find('div', class_='mid').p.text
	bonus = soup.find('div', class_='more').getText()
	ofrenda = soup.find('div', class_='more-infos-content').p.text
	linkImagen = soup.find('div', {"class": "more-infos"}).img['src']

	mision = mision.replace("Misión:", "")
	bonus = bonus.replace(mision, "")
	bonus = bonus.replace(ofrenda, "")
	bonus = bonus.replace("Misión:", "")


	fechaexacta = '{0:%d-%m-%Y}'.format(datetime.datetime.now())

	mensaje = discord.Embed(title = "`Duckmanax del " + fechaexacta + "`", url=sourceLinkAlmanax, color=0xe5be01)
	mensaje.add_field(name="Mision: ", value=f"{mision}", inline=False)
	mensaje.add_field(name="Bonus: ", value=f"{bonus.strip()}", inline=False)
	mensaje.add_field(name="Ofrenda: ", value=f"{ofrenda.strip()}", inline=False)
	mensaje.set_image(url=linkImagen)
	await ctx.send(embed = mensaje)

	print("Almanax enviado")

@bot.command()
async def balmanax(ctx, busqueda: str):
	print("Procesando busqueda de almanax")
	fecha = datetime.datetime.now()
	año = fecha.year
	smes = fecha.month
	sdia = fecha.day
	lp1 = len(busqueda)

	for mes in range (smes,13):

		if mes > smes:
			sdia = 1
		
		for dia in range (sdia,32):

			print("Procesando Año:", año, "Mes:", mes, "Dia:", dia, "Buscando:", busqueda)

			if mes < 10:
				mes2 = "0" + str(mes)
			else:
				mes2 = mes
			if dia < 10:
				dia2 = "0" + str (dia)
			else:
				dia2 = dia

			link = "http://www.krosmoz.com/es/almanax/" + str(año) + "-" + str(mes2) + "-" + str(dia2)

			try:
				data = requests.get(link).text
				soup = BeautifulSoup(data, 'lxml')
				datos = (soup.find('div', class_='mid').p.text) + soup.find('div', class_='more').getText()
			except Exception as error:
				pass

			for linea in data.split(" "):
				lp2 = len(linea)
				try:
					if re.findall(busqueda, linea, re.IGNORECASE) and (lp2 <= lp1 + 2):
						#mensaje enriquecido1
						source = requests.get(link).text
						soup = BeautifulSoup(source, 'lxml')

						mision = soup.find('div', class_='mid').p.text
						bonus = soup.find('div', class_='more').getText()
						ofrenda = soup.find('div', class_='more-infos-content').p.text
						linkImagen = soup.find('div', {"class": "more-infos"}).img['src']

						mision = mision.replace("Misión:", "")
						bonus = bonus.replace(mision, "")
						bonus = bonus.replace(ofrenda, "")
						bonus = bonus.replace("Misión:", "")


						fechaexacta = str(dia2) + "/" + str(mes2) + "/" + str(año)

						mensaje = discord.Embed(title = "`Busqueda Duckmanax " + fechaexacta + "`", url=link, color=0xe5be01)
						mensaje.add_field(name="Mision: ", value=f"{mision}", inline=False)
						mensaje.add_field(name="Bonus: ", value=f"{bonus.strip()}", inline=False)
						mensaje.add_field(name="Ofrenda: ", value=f"{ofrenda.strip()}", inline=False)
						mensaje.set_image(url=linkImagen)
						await ctx.send(embed = mensaje)
						#mensaje enriquecido2
						#await ctx.send("Encontre esta coincidencia de " + busqueda + " : " + link)
						break
				except Exception as error2:
					pass
	await ctx.send("Busqueda finalizada de " + busqueda)
	print("Busqueda de almanax finalizada")

@bot.event
async def on_message(ctx):
    if ctx.channel.name == 'almanax':
        await bot.process_commands(ctx)

@bot.event
async def on_ready():
	print("Bot listo")
	await bot.change_presence(activity=discord.Streaming(name="-ayuda",url="url twitch chanel"))

	while 1:

		await asyncio.sleep(1)
		fechaDailyAlmanax = datetime.datetime.now()

		info = open (r"path for save status of daily msg almanax",'r')
		flagIOE = info.read()
		flagOE = int(flagIOE)
		print("Hora actual:", fechaDailyAlmanax.hour, ":", fechaDailyAlmanax.minute, " Token OE: ", flagOE)
		info.close()

		if fechaDailyAlmanax.hour >= horaServidor and fechaDailyAlmanax.minute >= 1 and fechaDailyAlmanax.minute <= minServidor and flagOE == 0:
			info = open (r"path for save status of daily msg almanax",'w')
			info.write("1")
			info.close()

			print ("Procesando almanax automatico")

			source = requests.get(sourceLinkAlmanax).text
			soup = BeautifulSoup(source, 'lxml')

			mision = soup.find('div', class_='mid').p.text
			bonus = soup.find('div', class_='more').getText()
			ofrenda = soup.find('div', class_='more-infos-content').p.text
			linkImagen = soup.find('div', {"class": "more-infos"}).img['src']

			mision = mision.replace("Misión:", "")
			bonus = bonus.replace(mision, "")
			bonus = bonus.replace(ofrenda, "")
			bonus = bonus.replace("Misión:", "")

			fechaexacta = '{0:%d-%m-%Y}'.format(datetime.datetime.now())

			mensaje = discord.Embed(title = "`Duckmanax automatico del " + fechaexacta + "`", url=sourceLinkAlmanax, color=0xe5be01)
			mensaje.add_field(name="Mision: ", value=f"{mision}", inline=False)
			mensaje.add_field(name="Bonus: ", value=f"{bonus.strip()}", inline=False)
			mensaje.add_field(name="Ofrenda: ", value=f"{ofrenda.strip()}", inline=False)
			mensaje.add_field(name="Vuela entre las nubes despidiéndose: ", value="Que tengan un patastico dia @everyone", inline=False)
			mensaje.set_image(url=linkImagen)

			channel = bot.get_channel(709556171148623952)
			await channel.send(embed = mensaje)

			print("Almanax automatico enviado")

		if fechaDailyAlmanax.hour >= 0 and fechaDailyAlmanax.hour < horaServidor and flagOE == 1:
			info = open (r"path for save status of daily msg almanax",'w')
			info.write("0")
			info.close()
			print ("Reseteo de mensaje de almanax automatico")

bot.run(token_access_discord)