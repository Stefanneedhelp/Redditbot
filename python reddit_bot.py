import os
import asyncio
import feedparser
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_FEED_URL = "https://www.reddit.com/r/cryptocurrency/.rss"

INTERESANTNE_RECI = ["bitcoin", "etf", "bullish", "pump", "whale", "elon", "hack", "crypto", "btc"]

bot = Bot(token=BOT_TOKEN)
vec_poslato = set()

async def proveri_reddit():
    while True:
        try:
            feed = feedparser.parse(RSS_FEED_URL)

            for post in feed.entries:
                naslov = post.title.lower()
                link = post.link

                if link not in vec_poslato and any(rec in naslov for rec in INTERESANTNE_RECI):
                    vec_poslato.add(link)
                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=f"📢 Nova Reddit vest:\n\n{post.title}\n🔗 {link}"
                    )

        except Exception as e:
            print("Greška pri čitanju feeda:", e)

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(proveri_reddit())
