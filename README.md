# Anime Episode Notifier (com Playwright)

Este bot acessa episódios do site AnimesDrive, extrai o link de vídeo hospedado no Discord e envia para um canal no Discord.

## Requisitos

- Python 3.8+
- Variável de ambiente `DISCORD_WEBHOOK`

## Uso

```bash
pip install -r requirements.txt
playwright install
python main.py
```

Edite `anime_config.json` com os animes que deseja monitorar.