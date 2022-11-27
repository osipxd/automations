#!/usr/bin/env python3

import os
import requests

LEETCODE_URL = 'https://leetcode.com'

# Use https://convertingcolors.com/ and decimals format
COLORS = {
    'Easy': 47267,
    'Medium': 16760862,
    'Hard': 16723285,
}

# 1. Retreive the daily question
query = """
query questionOfToday {
    activeDailyCodingChallengeQuestion {
        date
        link
        question {
            acRate
            difficulty
            title
            topicTags { name }
        }
    }
}
"""

daily_question = requests.post(f'{LEETCODE_URL}/graphql', json={"query": query})\
    .json()['data']['activeDailyCodingChallengeQuestion']

# 2. Build message
topics = ['`{}`'.format(tag['name']) for tag in daily_question['question']['topicTags']]
day = daily_question['date'].rpartition('-')[-1]
acceptance = daily_question['question']['acRate']
data = {
    "content": f"Сегодня {day}-й день марафона и задача сегодняшнего дня:",
    "embeds": [
        {
            "title": daily_question['question']['title'],
            "description": "**Acceptance:** {:.1f}%\n**Topics:** ||{}||".format(acceptance, ', '.join(topics)),
            "url": LEETCODE_URL + daily_question['link'],
            "color": COLORS[daily_question['question']['difficulty']]
        }
    ]
}

# 3. Send the message to Discord
requests.post(os.environ['DISCORD_WEBHOOK'], json=data)\
    .raise_for_status()
