import subprocess
subprocess.run(["playwright", "install", "chromium"], check=True)

from playwright.sync_api import sync_playwright
import requests
import json
import time
import os

CONFIG_FILE = "anime_config.json"
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

print(f"Webhook URL carregado: {WEBHOOK_URL}")

def get_discord_video_link(page_url):
    with sync_playwright() as p:
        print(f"Abrindo navegador para: {page_url}")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
        page.wait_for_selector("video", timeout=15000)

        video_element = page.query_selector("video")
        video_src = video_element.get_attribute("src") if video_element else None

        browser.close()
        return video_src

def send_discord_message(anime, site_url, video_link=None):
    content = f"📢 **Novo Episódio!**\n🎬 {anime}\n🔗 [Assistir no site]({site_url})"
    if video_link:
        content += f"\n📥 Download: {video_link}"
    print(f"Enviando para o Discord...\n{content}")
    response = requests.post(WEBHOOK_URL, json={"content": content})
    print(f"Resposta do Discord: {response.status_code}")

# Loop principal
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    anime_list = json.load(f)

while True:
    for anime in anime_list:
        nome = anime["nome"]
        url = anime["url"]

        print(f"\nChecando: {nome} - URL: {url}")
        try:
            video_link = get_discord_video_link(url)
            print(f"🔗 Link encontrado: {video_link}")
            if video_link:
                send_discord_message(nome, url, video_link)
        except Exception as e:
            print(f"❌ Erro ao checar {nome}: {e}")

    print("\nAguardando 10 minutos...\n")
    time.sleep(600)
