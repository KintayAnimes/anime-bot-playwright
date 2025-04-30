import os
import json
import time
from playwright.sync_api import sync_playwright

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
CONFIG_FILE = "anime_config.json"
SEEN_FILE = "last_seen_episodes.json"

# Carrega lista de animes
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    anime_list = json.load(f)

try:
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        last_seen = json.load(f)
except FileNotFoundError:
    last_seen = {anime["nome"]: False for anime in anime_list}


def get_discord_video_link(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        try:
            page.wait_for_selector("video#video", timeout=10000)
            src = page.locator("video#video").get_attribute("src")
        except:
            src = None
        browser.close()
        return src


def send_discord_message(anime, site_url, video_url):
    if video_url:
        content = f"📢 **Novo Episódio Disponível!**\n🎬 {anime}\n🔗 [Assistir no site]({site_url})\n🎥 Link detectado:\n{video_url}"
    else:
        content = f"📢 **Novo Episódio Disponível!**\n🎬 {anime}\n🔗 [Assistir no site]({site_url})"

    os.system(f'curl -H "Content-Type: application/json" -X POST -d '{{"content": "{content}"}}' {WEBHOOK_URL}')


while True:
    for anime in anime_list:
        nome = anime["nome"]
        url = anime["url"]

        print(f"Checando: {nome} - URL: {url}")
        video_link = get_discord_video_link(url)
        print(f"Link encontrado: {video_link}")

        if video_link and not last_seen.get(nome, False):
            send_discord_message(nome, url, video_link)
            last_seen[nome] = True

    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(last_seen, f, ensure_ascii=False, indent=4)

    print("Aguardando 10 minutos...")
    time.sleep(600)