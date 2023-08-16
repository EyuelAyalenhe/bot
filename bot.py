import telegram
from bs4 import BeautifulSoup
import requests
import time
import asyncio


def scrape_website():
    # Replace with the URL of the website you want to scrape
    url = "http://www.mowsa.gov.et/"
    response = requests.get(url, timeout=90)
    soup = BeautifulSoup(response.content, "html.parser")

    img_elements = soup.find_all("img", class_="object-fit")
    img_data = [element["src"] for element in img_elements]

    p_elements = soup.find_all("p")
    p_data = [element.text.strip() for element in p_elements]

    h3_elements = soup.find_all("h3", class_="eael-entry-title")  # Finding all 'h3' elements with class 'eael-entry-title'
    h3_data = [element.text.strip() for element in h3_elements]    # Extracting the text content of the 'h3' elements

    return img_data, p_data, h3_data  # Returning the extracted image URLs, text data, and 'h3' data


async def send_message_to_channel(bot, channel_id, message):
    if message:
        await bot.send_message(chat_id=channel_id, text=message)


def send_images_to_channel(bot, channel_id, image_urls):
    for url in image_urls:
        bot.send_photo(chat_id=channel_id, photo=url)


async def main():
    bot = telegram.Bot(token="6363618249:AAExtzRpywoT7JG97HUa1mb0mB9RgPKs7u4")  # Replace with your own Telegram bot token

    channel_id = "@Eyuelayal"  # Replace with your own Telegram channel ID

    while True:
        img_data, p_data, h3_data = scrape_website()  # Scrapping the website for image URLs, text data, and 'h3' data

        send_images_to_channel(bot, channel_id, img_data)  # Sending the images to the Telegram channel

        for data in p_data:
            await send_message_to_channel(bot, channel_id, data)  # Sending each text data to the Telegram channel

        for data in h3_data:
            await send_message_to_channel(bot, channel_id, data)  # Sending each 'h3' data to the Telegram channel

        await asyncio.sleep(1800)  # Delaying execution for 1800 seconds (30 minutes)


if __name__ == "__main__":
    asyncio.run(main())  # Running the main asynchronous function
