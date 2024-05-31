import discord
from discord.ext import commands
import asyncio
import random

token=''

# Configura los intents para poder recibir el contenido de los mensajes
intents = discord.Intents.default()
intents.message_content = True

# Define el prefijo de comandos para el bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Lista de productos de la tienda
productos = [
    {"nombre": "Producto 1", "cantidad": 5, "precio": 10},
    {"nombre": "Producto 2", "cantidad": 8, "precio": 15},
    {"nombre": "Producto 3", "cantidad": 3, "precio": 20},
    {"nombre": "Producto 4", "cantidad": 10, "precio": 25},
    {"nombre": "Producto 5", "cantidad": 2, "precio": 30},
    {"nombre": "Producto 6", "cantidad": 6, "precio": 35},
    {"nombre": "Producto 7", "cantidad": 4, "precio": 40},
    {"nombre": "Producto 8", "cantidad": 7, "precio": 45},
    {"nombre": "Producto 9", "cantidad": 1, "precio": 50},
    {"nombre": "Producto 10", "cantidad": 9, "precio": 55}
]

informacion_tarjeta = {}

def mostrar_productos():
    tabla = "```\n"
    tabla += "ID | Producto        | Cantidad | Precio\n"
    tabla += "-" * 35 + "\n"
    for i, producto in enumerate(productos):
        tabla += f"{i+1:2} | {producto['nombre']:15} | {producto['cantidad']:8} | ${producto['precio']:6}\n"
    tabla += "```"
    return tabla

# Comando para mostrar los productos disponibles
@bot.command(name='productos')
async def mostrar_productos_command(ctx):
    await ctx.send(mostrar_productos())

# Comando para seleccionar un producto y realizar un pedido
@bot.command(name='pedido')
async def hacer_pedido(ctx, *ids_productos: int):
    
    total_pedido = 0
    
    for id_producto in ids_productos:
        if 1 <= id_producto <= len(productos):
            producto = productos[id_producto - 1]
            if producto['cantidad'] > 0:
                producto['cantidad'] -= 1
                total_pedido += producto['precio']
            else:
                await ctx.send(f"Lo siento, el producto '{producto['nombre']}' está agotado.")
        else:
            await ctx.send("ID de producto inválido.")

    if total_pedido > 0:
        pedido_id = ''.join(random.choices('0123456789', k=10))
        tiempo_entrega = random.randint(5, 40)  # Tiempo de entrega aleatorio en segundos
        
        # Verifica si el usuario ya tiene información de tarjeta guardada
        if ctx.author.id in informacion_tarjeta:
            tarjeta = informacion_tarjeta[ctx.author.id]
            await ctx.send(f"Total de tu pedido: ${total_pedido}\nTu pedido ID es: {pedido_id}\nEl tiempo estimado de entrega es de {tiempo_entrega} segundos.\n\nInformación de tarjeta guardada:\nNúmero de tarjeta: {tarjeta['numero']}\nCVV: {tarjeta['cvv']}")
        else:
            # Si no tiene información de tarjeta guardada, solicita la información
            await ctx.send("Por favor, ingresa tu número de tarjeta de crédito (16 dígitos):")
            try:
                # Espera la respuesta del usuario
                mensaje = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author)
                numero_tarjeta = mensaje.content
                
                # Solicita el CVV
                await ctx.send("Por favor, ingresa el CVV de tu tarjeta (3 dígitos):")
                cvv_mensaje = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author)
                cvv = cvv_mensaje.content
                
                # Guarda la información de la tarjeta
                informacion_tarjeta[ctx.author.id] = {'numero': numero_tarjeta, 'cvv': cvv}
                
                # Envía la confirmación junto con el pedido
                await ctx.send(f"Total de tu pedido: ${total_pedido}\nTu pedido ID es: {pedido_id}\nEl tiempo estimado de entrega es de {tiempo_entrega} segundos.\n\nInformación de tarjeta guardada:\nNúmero de tarjeta: {numero_tarjeta}\nCVV: {cvv}")
            except asyncio.TimeoutError:
                await ctx.send("¡Tiempo de espera agotado! Por favor, vuelve a intentarlo.")
        
        await ctx.send("¿Deseas cancelar este pedido? (responde 'si' o 'no')")
        try:
            respuesta_cancelar = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author)
            if respuesta_cancelar.content.lower() == 'si':
                await ctx.send("Pedido cancelado.")
                return  # Sale de la función sin enviar el mensaje de entrega
        except asyncio.TimeoutError:
            await ctx.send("¡Tiempo de espera agotado! Pedido confirmado.")
        
        await asyncio.sleep(tiempo_entrega)
        await ctx.send(f"¡Tu pedido ID '{pedido_id}' ha sido entregado!")

#Borrar tarjeta de debito
@bot.command(name='borrar_tarjeta')
async def borrar_tarjeta(ctx):
    if ctx.author.id in informacion_tarjeta:
        del informacion_tarjeta[ctx.author.id]
        await ctx.send("La información de tu tarjeta de crédito ha sido eliminada correctamente.")
    else:
        await ctx.send("No tienes información de tarjeta de crédito guardada.")

@bot.command(name='cancelar')
async def cancelar_pedido(ctx, pedido_id: str):
    await ctx.send(f"Su pedido con la ID {pedido_id} ha sido cancelado con éxito. Recibirá su reembolso en 3 días hábiles a su tarjeta de débito.")

# Comando para consultar el estado de un pedido utilizando su ID
@bot.command(name='consultar')
async def consultar_pedido(ctx, pedido_id: str):
    tiempo_restante = random.randint(1, 10)
    while tiempo_restante > 0:
        await ctx.send(f"Tu pedido ID '{pedido_id}' llegará en {tiempo_restante} segundos.")
        await asyncio.sleep(1)
        tiempo_restante -= 1
    await ctx.send(f"¡Tu pedido ID '{pedido_id}' ha sido entregado!")


# Define una función para manejar mensajes
async def handle_message(message):
    # Evita que el bot responda a sí mismo o a otros bots
    if message.author == bot.user or message.author.bot:
        return
    
    if message.content.lower() == "hola":
        await message.channel.send(f"¡Hola {message.author.name}! Bienvenid@ a la tienda!, puedes escribir [ayuda] para ver todos los comandos disponibles ")
    
    if message.content.lower() == "¿como estas?" or message.content.lower() == "como estas?":
        await message.channel.send("¡Estoy bien, gracias por preguntar!")

    if message.content.lower() == "adios":
        await message.channel.send(f"Adiós {message.author.name}, ¡hasta luego!")
        
    if message.content.lower() == "envios disponibles" or message.content.lower() == "envios" or message.content.lower() == "envio" or message.content.lower() == "paqueteria":
        await message.channel.send("Tenemos envíos gratuitos a toda la República Mexicana directo a su casa a través de DHL.")

    if message.content.lower() == "ayuda":
        await message.channel.send("Los comandos disponibles son: /n !pedidos (Sirve para ordenar un producto con su id y la cantidad) /n !productos (muestra todos los productos disponible), !borrar_tarjeta (borra la informacion de su tarjeta), !info (da la informacion del usuario)")


#saludo
@bot.command(name='saludo')
async def saludo(ctx):
    await ctx.send(f"Hola {ctx.author.name}, Bienvenid@ a nuestra tienda")

@bot.command(name='bye')
async def dc(cxt):
    await cxt.send("Adios :)")
    await bot.close()

#información usuario
@bot.command(name='info')
async def info(ctx):
    user = ctx.author
    await ctx.send(f"Tu nombre es {user.name} y tu ID es {user.id}")

# Registra el evento on_ready
@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name}')

# Registra el evento on_message
@bot.event
async def on_message(message):
    await handle_message(message)
    await bot.process_commands(message)

# Define la función principal asincrónica para iniciar el bot
async def main():
    try:
        async with bot:
            await bot.start(token)
    except KeyboardInterrupt:
        print("Bot detenido manualmente")
    finally:
        await bot.close()

# Ejecuta la función principal en el contexto asincrónico
if __name__ == "__main__":
    asyncio.run(main())
