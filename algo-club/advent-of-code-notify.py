#!/usr/bin/env python3

from datetime import datetime
import os
import random
import re
import requests

AOC_URL = 'https://adventofcode.com'

# 0. Select random greeting
greeting = random.choice([
    'Хо-хо-хо!',
    'Хэй!',
    'Йоу!',
    'Привет!',
    'А я к вам с подарочком!',
    'Привет всем кто уже проснулся!',
    'На часах ровно... время выкладывать задачку!',
    ':wave::robot:',
    'Приветствую, человеки.',
    'Псс... Как насчёт заработать немного :star:?',
    '[ERROR: GREETING_NOT_FOUND]',
])

# 1. Retrieve the daily task and parse it
year = str(datetime.today().year)
day = str(datetime.today().day)
day_url = f'{AOC_URL}/{year}/day/{day}'

response = requests.get(day_url)
response.raise_for_status()
title = re.search('<article class="day-desc"><h2>--- (.+) ---</h2>', response.text).group(1)
print(title)

# 2. Build message
data = {
    "thread_name": title.replace(': ', ' - '),
    "content": f'{greeting} Сегодня {day}-й день Advent of Code!\n'
               'В этом треде можно задавать вопросы по задаче, делиться идеями и решениями.\n'
               '\n'
               'Если хочешь поделиться решением, будет классно если вместе со сылкой укажешь:\n'
               ':tools: Язык на котором оно написано\n'
               ':timer: Сложность по времени _(если можешь посчитать)_\n'
               ':floppy_disk: Сложность по памяти _(если можешь посчитать)_\n'
               '\n'
               '> :robot: Старайся не постить спойлеры к решению в день когда задача опубликована. '
               'Если очень хочется, окружи спойлер двумя вертикальными палками `||`, тогда текст будет скрыт. '
               'На следующий день - пожалуйста, тред открыт для спойлеров :slight_smile:',
    "embeds": [
        {
            "title": title,
            "url": day_url,
            "color": 16711680, # https://convertingcolors.com/decimal-color-16711680.html
        }
    ],
}

# 3. Send the message to Discord
response = requests.post(os.environ['DISCORD_WEBHOOK'], json=data)
