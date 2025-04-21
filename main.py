import os
import asyncio
import feedparser
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN ili CHAT_ID nisu postavljeni!")

# 🔝 Najveći kripto subredditi
rss_feedovi = ["https://www.needhelp.com/trouver-un-job"
   ]

# 🧠 Ključne reči koje nas zanimaju
KLJUCNE_RECI = [
    "Montage", "Menuisier", "ébéniste", "Électricité", "Pose carrelage",
    "Percer", "fixer", "Enduit", "Pose de porte", "portail", "Découpe",
    "Pose sanitaire", "Pose parquet", "Peinture", "Poser", "Installation", "Reparer", "Réparer", "Revêtements de sol"
   
]

bot = Bot(token=BOT_TOKEN)
vec_poslato = set()

async def proveri_reddit():
    while True:
        try:
            for url in rss_feedovi:
                feed = feedparser.parse(url)
                for post in feed.entries:
                    naslov = post.title.lower()
                    link = post.link

                    if link not in vec_poslato and any(rec in naslov for rec in KLJUCNE_RECI):
                        vec_poslato.add(link)
                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=f"📰 *Nova Reddit vest!*\n\n{post.title}\n🔗 {link}",
                            parse_mode="Markdown"
                        )
                        print(f"📤 Poslato: {post.title}")
        except Exception as e:
            print("❌ Greška:", e)

        await asyncio.sleep(60)

if __name__ == "__main__":
    print("✅ Reddit bot pokrenut...")
    asyncio.run(proveri_reddit())


