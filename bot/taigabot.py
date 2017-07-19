from slackclient import SlackClient
from taiga import TaigaAPI
import re
import os
import time

BOT_ID = os.environ.get('BOT_ID')
TG_PATTERN = 'tg#'
TG_BASE_URL = os.environ.get('taiga_host')
TG_USER = os.environ.get('taiga_user')
TG_PASSWORD = os.environ.get('taiga_pass')
TG_PROJECT = os.environ.get('taiga_project')

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

api = TaigaAPI(host=TG_BASE_URL)
api.auth(
    username = TG_USER,
    password = TG_PASSWORD
)

def fetch_taiga(message, channel, thread, user):
    m = set(re.findall('tg#\d*', message.lower()))
    attachments = []
    if m:
        for match in m:
            print (match)
            text_response = ""

            project = api.projects.get_by_slug(TG_PROJECT)
            project.name = TG_PROJECT
            tg_element_id = match.lower().split(TG_PATTERN)[1].strip().lower()
            taiga_element = project.get_item_by_ref(tg_element_id)
            if taiga_element is not None:
                color = '#36a64f'
                if 'us' in taiga_element.element_shortcut:
                    color = '#6B2307'
                elif 'epic' in taiga_element.element_shortcut:
                    color = '#B5D86E'
                elif 'issue' in taiga_element.element_shortcut:
                    color = '#E53100'
                elif 'task' in taiga_element.element_shortcut:
                    color = '#E5BF57'

                attachments.append(
                    {
                        "fallback": "the @taigabot worked magic for you",
                        "color": color,
                        "pretext": taiga_element.element_type+" "+tg_element_id+" ("+taiga_element.subject+")",
                        "author_name": taiga_element.element_type,
                        "title": taiga_element.subject,
                        "title_link": TG_BASE_URL+"project/"+project.name+"/"+taiga_element.element_shortcut+"/"+tg_element_id,
                        "text": taiga_element.description,
                        "footer": "https://taiga.silicon.dev.espp.eon.com",
                        "footer_icon": "https://taiga.io/images/favicon/android-icon-192x192.png"
                    })
            else:
                color = '#ffffff'
                attachments.append(
                    {
                        "fallback": "the @taigabot worked magic for you",
                        "color": color,
                        "pretext": "TG#"+tg_element_id+" could not be found! It probably was deleted."
                    })

        slack_client.api_call("chat.postMessage", channel=channel, attachments=attachments, thread_ts=thread, as_user=True)


def determine_thread(output):
    if 'thread_ts' in output:
        ts = output['thread_ts']
    else:
        ts = output['ts']

    return ts

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and TG_PATTERN in output['text'].lower():
                return output['text'], output['channel'], determine_thread(output), output['user']
    return None, None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 0 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("The @taigabot connected and is running!")
        while True:
            message, channel, thread, user = parse_slack_output(slack_client.rtm_read())
            if message and channel and thread and user:
                fetch_taiga(message, channel, thread, user)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
