import requests
import json
import os
GRAPH_URL = "https://graph.facebook.com/v2.6"

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

# texr message
def send_text_message(id, content):
	post_message_url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
	response_msg = json.dumps({"recipient": {"id": id}, "message": {"text": content}})
	requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)

# image message
def send_image_message(id, image):
	post_message_url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
	response_img = json.dumps({"recipient": {"id": id}, "message": {
		"attachment": {
			"type": "image",
			"payload": {
				"url": image
			}
		}
	}})
	requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_img)

# button message
def template_message(id, title, image_url, subtitle, data):
	post_message_url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
	response_template = json.dumps({"recipient": {"id": id}, "message": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": title,
                        "image_url": image_url,
                        "subtitle": subtitle,
                        "buttons": data
                    }
                ]
            }
        }
    }})
	requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_template)

# quick reply button message
def quick_reply_message(id, text, quick_replies):
	post_message_url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
	response_fast = json.dumps({"recipient": {"id": id}, "message": {
		"text": text,
		"quick_replies": quick_replies
	}})
	requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_fast)

