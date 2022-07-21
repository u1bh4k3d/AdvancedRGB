import discord
import asyncio
from bleak import BleakClient


# Discord bot token
TOKEN = "tokenhere"

# RGB BLE controller mac address
ADDRESS = "macadresshere"

# UUID to write values to
MODEL_NBR_UUID = "uuidhere"

# Config of colors coresperonding to values
RGB_CONF = {

    "off" : "7f77944a5498752f8929a2e435c4be8d",
    "red" : "1273622a87797e5c768211ee59308e5b",
    "yellow" : "eddba94760386c34940680801f92f403",
    "green" : "42c9e15436faf27b95fb68d3159c93e2",
    "blue" : "0b193631a1c203cfadfdbad7820f3856",
    "purple" : "801639fcb80f1979175eb8de87e03ef2",
    "test" : "7e00038a02000000ef",
    "orange" : "aab33a2d5e7e856fab326f0f442bfe00"
    
}


discord_bot = discord.Client()
bluetooth_client = BleakClient(ADDRESS)

@discord_bot.event
async def on_ready():
    global bluetooth_client

    try:
        await bluetooth_client.connect()
        model_number = await bluetooth_client.write_gatt_char(MODEL_NBR_UUID, bytearray.fromhex(RGB_CONF["off"]))

    except Exception as e:
        print(e)


@discord_bot.event
async def on_message(message):
    if message.content.startswith("set "):
        config = str(message.content.split(" ",1)[1])
        print("Wrote bluetooth command [" + config + "] on device (" + ADDRESS + ")")
        if config not in RGB_CONF:
            return
        await message.channel.send("**Config: **" + config)
           
        try:
            await bluetooth_client.write_gatt_char(MODEL_NBR_UUID, bytearray.fromhex(RGB_CONF[config]))
        except Exception as e:
            print("Unable to send bluetooth command!: {0}".format(e))

if __name__ == "__main__":
    print("Starting discord bot...")
    discord_bot.run(TOKEN)