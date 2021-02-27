import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import time

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

users = {}
messages = []


def fetch_users():
    try:
        result = client.users_list()
        for member in result["members"]:
            users[member["id"]] = member["name"]
        print("users: ", users)

    except slack.errors.SlackApiError as e:
        print("Error fetching Users")


def fetch_messages(convo_id):
    try:
        result = client.conversations_history(channel=convo_id)
        for message in result["messages"]:
            user = users[message['user']]
            msg = {}
            msg['user'] = user
            msg['content'] = message['text']
            msg['time'] = time.ctime(float(message['ts']))
            msg['replies'] = fetch_thread_replies(convo_id, message['ts'])
            messages.append(msg)
        print("messages: ", messages)

    except slack.errors.SlackApiError as e:
        print("Error fetching messages")


def fetch_thread_replies(convo_id, ts):
    try:
        result = client.conversations_replies(channel=convo_id, ts=ts)
        replies = []
        for reply in result["messages"]:
            if 'thread_ts' in reply:
                if reply['ts'] != reply['thread_ts']:
                    user = users[reply["user"]]
                    msg = {}
                    msg['user'] = user
                    msg['content'] = reply["text"]
                    msg['time'] = time.ctime(float(reply['ts']))
                    replies.append(msg)
        print("replies: ", replies)
        return replies

    except slack.errors.SlackApiError as e:
        print("Error fetching thread replies")


def fetch_coversations():
    try:
        result = client.conversations_list()
        print(result['messages'])

    except slack.errors.SlackApiError as e:
        print("Error fetching conversations")


def main():
    fetch_users()
    fetch_messages('C01P5100TFZ')


if __name__ == '__main__':
    main()
