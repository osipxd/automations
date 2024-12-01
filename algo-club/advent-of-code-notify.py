#!/usr/bin/env python3
import os
import random
import re
import time
from datetime import datetime, timezone

import requests

AOC_URL = 'https://adventofcode.com'
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

EMOJI_ELF = '\U0001F9DD'
EMOJI_SMILE = '\U0001F642'
EMOJI_CHRISTMAS_TREE = '\U0001F384'
EMOJI_STAR = '\U00002B50'
EMOJI_YAWNING = '\U0001F971'
EMOJI_ONE = '\U0000261D\U0000FE0F'
EMOJI_TWO = '\U0000270C\U0000FE0F'
EMOJI_CROSSED = '\U0001FAF0'

# 0. Set greeting and wait for Midnight EST
greeting = "П-привет, программисты! *нервно теребит колпак* Сегодня первый день Advent of Code, и я так волнуюсь!!! Помогите нам спасти Рождество!!!"

start = datetime.now(timezone.utc)
target_time = datetime(start.year, start.month, start.day, 5, 0, 1)  # Midnight EST (UTC-5)
remaining = target_time - start
remaining_seconds = remaining.total_seconds()

if remaining_seconds > 0:
    print(f'Sleep for {remaining}')
    time.sleep(remaining_seconds)
print(f'Started at {datetime.now(timezone.utc).time()}')

# 1. Retrieve the daily task and parse it
year, day = str(start.year), str(start.day)
day_url = f'{AOC_URL}/{year}/day/{day}'

response = requests.get(day_url)
response.raise_for_status()
title = re.search('<article class="day-desc"><h2>--- (.+) ---</h2>', response.text).group(1)
print(title)

# 2. Build message
def escape(text: str) -> str:
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        if char in text:
            text = text.replace(char, f'\\{char}')
    return text

message = (
    f'{EMOJI_CHRISTMAS_TREE} *[{escape(title)}]({day_url})*\n'
    '\n'
    f'{EMOJI_ELF} \\(вбегает молодой эльф\\): {escape(greeting)}\n'
    '\n'
    f'**>*На всякий случай напомню правила*\n'
    '> \n'
    f'>{EMOJI_ONE} Обсуждаем задачи в комментариях к посту\n'
    f'>{EMOJI_TWO} Прячь все спойлеры ||вот так|| в день публикации задачи\\. '
    f'На следующий день тред открыт для спойлеров {EMOJI_SMILE}\n'
    f'>{EMOJI_CROSSED} Помни про @aoc\\_club\\_chat, где можно общаться без привязки к задачам\\.||'
)

print(message)

# 3. Send the message to Telegram
response = requests.post(
    f'{TELEGRAM_API_URL}/sendMessage',
    json={
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'MarkdownV2',
        'link_preview_options': {
            'is_disabled': False,
        },
    }
)
response.raise_for_status()
