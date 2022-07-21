# Reverse engineering BLE RGB strip
![](https://i.ibb.co/T0KvF5h/Untitled-1.png)

# General info

## How does a BLE RGB strip work?

BLE or **Bluetooth Low Energy** makes it possible to send small amounts of data between devices. In our example we use this technology to change colors remotely on a ledstrip.

We pair our phone with the Bluetooth controller connected on the RGB pins. We use an application to send colors encoded into hex values inside Bluetooth packets, The Bluetooth controller on the ledstrip is decoding these values to convert them into colors, **r**ed **g**reen and **b**lue. Combining RGB can form a variety of colors.

## Why would we reverse engineer this?

For nerds like us, the provided app to control the RGB has very limited possibilities. That's why we want to make the ledstrip more interactive.

When you know the values matching the colors, it means you can write your own applications to control the RGB strip. This means you can combine it with any API or code, which makes it extra fun! For example, you could make your ledstrip flash red 3x times every time you get an important notification. You could convert text to morse code or whatever! You can do endless amount of things.

# Let's hack!
## Requirements

- Android/ iOS device
- Computer running Linux/ Windows/ MacOS
-    BLE RGB strip with mobile app
     - I bought mine from Shein, very cheap and fast      delivery. Buy [here](https://eur.shein.com/1pc-Colorful-LED-Strip-Light-p-6505567-cat-2310.html?share_from=andsheur&url_from=GM7216279255387840512&ref=www&rep=dir&ret=eur "here").
-    Software to read BLE packets
     -    I used  [WireShark](https://www.wireshark.org/ "WireShark")


## Generating HCI dumps:

The first thing we want to do is reading the values sent from your mobile app to the RBG BLE controller.

We can easily do this by [recording HCI logs](https://medium.com/@charlie.d.anderson/how-to-get-the-bluetooth-host-controller-interface-logs-from-a-modern-android-phone-d23bde00b9fa).

![](https://media.discordapp.net/attachments/999407861526438018/999634597581160529/Screenshot_20220721-131055_Settings.jpg?width=427&height=436)

Close every application, start recording the logs using the tutorial linked above.

Power your RGB strips and connect to it using the app provided for your specific model.

![](https://media.discordapp.net/attachments/999407861526438018/999633777112395887/Screenshot_20220721-130710_iStrip.jpg?width=968&height=336)

When connected, change to every color, this makes sure the value of all colors are getting recorded.

![](https://media.discordapp.net/attachments/999407861526438018/999634279384486049/Screenshot_20220721-130937_iStrip.jpg?width=968&height=426)

When you recorded every color you will [generate HCI dumps](https://medium.com/@charlie.d.anderson/how-to-get-the-bluetooth-host-controller-interface-logs-from-a-modern-android-phone-d23bde00b9fa) we can use to read the data from further on on our computer.

![](https://media.discordapp.net/attachments/999407861526438018/999635549205823498/Screenshot_20220721-131436_My_Files.jpg?width=790&height=436)

Now we can send these logs over to our computer and start reading them!

## Reading data from HCI dump

When we generated a HCI dump containing the packets to change colors, we have to read tohose packets to find out which values are for which color.

We will open the HCI dump in Wireshark

![](https://media.discordapp.net/attachments/999407861526438018/999637013177307246/unknown.png)

Now we can see all data sent between your phone and the BLE controller from the RBG strip.

We will filter these on **info** and search for the ones with **Sent Write Command**
![](https://media.discordapp.net/attachments/999407861526438018/999651966630236251/unknown.png)

Open them and copy all **values** into a text file.

![](https://media.discordapp.net/attachments/999407861526438018/999655027662663760/unknown.png)

![](https://media.discordapp.net/attachments/999407861526438018/999655965026697338/unknown.png)

Now you have a list of encoded values that you can use to make an application with, but first we have to find out which value is which color.

## Writing values to RGB strip w/ official app

To find out what these values mean i used the app [nRF Connect app](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=nl&gl=US)

![](https://media.discordapp.net/attachments/999407861526438018/999657803645993031/Screenshot_20220721-144152_nRF_Connect.jpg?width=687&height=436)

Open the application and connect to your RGB BLE controller.

Now you have to write the values to the right UUID (you can see this in the Wireshark frame)

![](https://media.discordapp.net/attachments/999407861526438018/999658932345765928/unknown.png)
![](https://media.discordapp.net/attachments/999407861526438018/999659272042467468/Screenshot_20220721-144859_nRF_Connect.jpg?width=306&height=436)

![](https://media.discordapp.net/attachments/999407861526438018/999660117727383592/unknown.png)

![](https://media.discordapp.net/attachments/999407861526438018/999660001339650169/Screenshot_20220721-145152_nRF_Connect.jpg?width=968&height=270)

Now I noticed the RGB strip changed to yellow. This means this value corresperonds to the color yellow, you will do this with every value untill you have a complete list.

| Colors | Values                         |
|------------|----------------------------------|
| **off**    | 7f77944a5498752f8929a2e435c4be8d |
| **red**    | 1273622a87797e5c768211ee59308e5b |
| **yellow** | eddba94760386c34940680801f92f403 |
| **green**  | 42c9e15436faf27b95fb68d3159c93e2 |
| **blue**   | 0b193631a1c203cfadfdbad7820f3856 |
| **purple** | 801639fcb80f1979175eb8de87e03ef2 |
| **orange** | aab33a2d5e7e856fab326f0f442bfe00 |

Now it is very easy to use these values to make your own custom applications/ triggers using pything or whatever language you love! 

For example a red flash when you get hit in a game. A flash when you get a follower on Twitter, Changing the RGB from the other side of the world using a simple web interface, ...

I made an example by controlling my RGB strip colors with a discord bot.

## Discord Bot Example

![](https://media.discordapp.net/attachments/999407861526438018/999409149332947065/Screenshot_20220720-221450_Gallery.jpg?width=196&height=436)

### [Video in action](https://www.tiktok.com/@juicyhacker/video/7122552769936067886?is_from_webapp=1&sender_device=pc&web_id=7112045024872007174)

For this example I used python with the [BleakCLient](https://github.com/hbldh/bleak), Asyncio and [Discord](https://discordpy.readthedocs.io/en/stable/) modules.

``` py
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

```

If you are planning to use this script be sure to store private data such as tokens and the macadresses into **.env** files.

You don't want people to change your leds from over the world without permission. :)

Have fun!