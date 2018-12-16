from transitions.extensions import GraphMachine

from utils import *
from web_scraper import *

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

mytext = "Oh yeah lakers!"
print("================================")
# print(word_tokenize(mytext))
print("================================")

dataInfo = NBA_today()
currentYear = str(dataInfo[0])
currentDate = str(dataInfo[1])
# currentDate = "20181207"
all_teams = []
all_teams = list(NBA_team(currentYear))
imgUrls = moviePoster(1)
print(imgUrls)


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
#====================================== Conditions ======================================
    # # input s to start
    # def is_going_to_start(self, event):
    #     if event.get("postback"):
    #         text = event['postback']['title']
    #         return text.lower() == 's'
    #     elif event.get("message"):
    #         text = event['message']['text']
    #         return text.lower() == 's'
    #     return False

    # input help to see how to play with it
    def is_going_to_help(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'help'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "help" in text:
                return True
        return False

    # input s to start (NBA today)
    def is_going_to_nbaToday(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            # return text.lower() == 'nba today'
            return text.lower() == "s"
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "s" in text:
                return True
        return False

    def is_going_to_moviePics(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'movie'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "movie" in text:
                return True
        return False

    def is_going_to_nbaStatus(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'nba stats'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if ("stats" in text or "status" in text):
                return True
        return False
    
    def is_going_to_nbaStandings(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'standings'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if ("standings" in text or "standing" in text):
                return True
        return False
    
    def is_going_to_confStandings(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'conference'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if ("conference" in text):
                return True
        return False

    def is_going_to_divStandings(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'division'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if ("division" in text):
                return True
        return False

    def is_going_to_playerInfo(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'players info'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if ("players" in text or "player" in text):
                return True
        return False

    def is_going_to_pickDivision(self, event):
        if event.get("postback"):
            text = event['postback']['title']            
            return (text.lower() == 'east' or text.lower() == 'west')
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "east" in text or "west" in text:
                return True
        return False


    def is_going_to_teams(self, event):
        if event.get("postback"):
            text = event['postback']['title']            
            return (text.lower() == 'atlantic' or text.lower() == 'central' or text.lower() == 'southeast' or text.lower() == 'southwest' or text.lower() == 'northwest' or text.lower() == 'pacific')
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if ("atlantic" in text or "central" in text or "southeast" in text or "southwest" in text or "northwest" in text or "pacific" in text):
                return True
        return False


    def is_going_to_playerPpg(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            text = text.lower()
            if (text in all_teams):
                return True
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            for word in text:
                if (word in all_teams):
                    return True
        return False


    def is_going_to_nbaGames(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'nba games'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "game" in text or "games" in text:
                return True
        return False

    def is_going_to_boxScore(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'box score'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "box" in text or "boxscore" in text:
                return True
        return False
    
    def is_going_to_nbaNews(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'nba news'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "news" in text or "headline" in text:
                return True
        return False


    def go_back_to_start(self, event):
        sender_id = event['sender']['id']
        data = "Welcome home."
        if event.get("postback"):
            text = event['postback']['title']    
            response = send_text_message(sender_id, data)
            return text.lower() == 'home'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "home" in text:
                response = send_text_message(sender_id, data)
                return True
        return False


    def go_back_to_nbaToday(self, event):
        if event.get("postback"):
            text = event['postback']['title']
            return text.lower() == 'more nba'
        elif event.get("message"):
            text = event['message']['text']
            text = word_tokenize(text.lower())
            if "more" in text and "nba" in text:
                return True
        return False

#===================================== actions =======================================
    # def on_enter_start(self, event):
    #     print("==========================")
    #     print("Start Playing")
    #     print("==========================")
    #     sender_id = event['sender']['id']
    #     text = "What can I do for you?"
    #     quick_replies = [
    #         {
    #             "content_type": "text",
    #             "title": "NBA TODAY",
    #             "payload": "NBA TODAY"
    #         },
    #         {
    #             "content_type": "text",
    #             "title": "Search Words",
    #             "payload": "Search Words"
    #         }
    #     ]
    #     response = quick_reply_message(sender_id, text, quick_replies)

    def on_enter_help(self, event):
        print("==========================")
        print("Start Playing")
        print("==========================")
        sender_id = event['sender']['id']
        text = "Enter 'S' to start playing.\nEnter 'Help' to see the usage.\nEnter 'Movie' to see top5 movies' poster"
        quick_replies = [
            {
                "content_type": "text",
                "title": "S",
                "payload": "S"
            },
            {
                "content_type": "text",
                "title": "Help",
                "payload": "Help"
            },
            {
                "content_type": "text",
                "title": "Movie",
                "payload": "Movie"
            }
        ]
        response = quick_reply_message(sender_id, text, quick_replies)
        self.go_back()

    def on_enter_moviePics(self, event):
        print("==========================")
        print("Movie Pictures")
        print("==========================")
        sender_id = event['sender']['id']
        for img in imgUrls:
            responese = send_image_message(sender_id, img)
        self.go_back()

    def on_enter_nbaToday(self, event):
        print("==========================")
        print("More NBA Options")
        print("==========================")
        sender_id = event['sender']['id']
        title="NBA TODAY" 
        image_url="https://i.imgur.com/nWs2EuN.jpg"
        subtitle="more options"
        data = [
            {
                "type": "postback",
                "title": "NBA Games",
                "payload": "NBA Games"
            },
            {
                "type": "postback",
                "title": "NBA Stats",
                "payload": "NBA Stats"
            },
            {
                "type": "postback",
                "title": "NBA News",
                "payload": "NBA News"
            }
        ]
        response = template_message(sender_id, title, image_url, subtitle, data)

    def on_enter_nbaStatus(self, event):
        print("==========================")
        print("NBA Status")
        print("==========================")
        sender_id = event['sender']['id']
        title="NBA Status"
        image_url="https://i.imgur.com/nWs2EuN.jpg"
        subtitle="Standings/Players"
        data = [
            {
                "type": "postback",
                "title": "Standings",
                "payload": "Standings"
            },
            {
                "type": "postback",
                "title": "Players Info",
                "payload": "Players Info"
            }
        ]
        response = template_message(sender_id, title, image_url, subtitle, data)

    def on_enter_nbaStandings(self, event):
        print("==========================")
        print("Standings")
        print("==========================")
        sender_id = event['sender']['id']
        title="Standings" 
        image_url="https://i.imgur.com/nWs2EuN.jpg"
        subtitle="more options"
        data = [
            {
                "type": "postback",
                "title": "Conference",
                "payload": "Conference"
            },
            {
                "type": "postback",
                "title": "Division",
                "payload": "Division"
            }
        ]
        response = template_message(sender_id, title, image_url, subtitle, data)

    def on_enter_confStandings(self, event):
        print("==========================")
        print("Sort By Conference")
        print("==========================")
        sender_id = event['sender']['id']
        standsList = NBA_standings("conference")
        eastStands = standsList[0]
        westStands = standsList[1]
        response = send_text_message(sender_id, eastStands)
        response = send_text_message(sender_id, westStands)
        text = "What's next?"
        quick_replies = [
            {
                "content_type": "text",
                "title": "More NBA",
                "payload": "More NBA"
            },
            {
                "content_type": "text",
                "title": "Home",
                "payload": "Home"
            },
        ]
        response = quick_reply_message(sender_id, text, quick_replies)

    def on_enter_divStandings(self, event):
        print("==========================")
        print("Sort By Division")
        print("==========================")
        sender_id = event['sender']['id']
        standsList = NBA_standings("division")
        for stands in standsList:
            response = send_text_message(sender_id, stands)
        text = "What's next?"
        quick_replies = [
            {
                "content_type": "text",
                "title": "More NBA",
                "payload": "More NBA"
            },
            {
                "content_type": "text",
                "title": "Home",
                "payload": "Home"
            },
        ]
        response = quick_reply_message(sender_id, text, quick_replies)

    def on_enter_playerInfo(self, event):
        print("==========================")
        print("Player Info")
        print("Choose conference")
        print("==========================")
        sender_id = event['sender']['id']
        title="EAST/WEST"
        image_url="https://i.imgur.com/nWs2EuN.jpg"
        subtitle="Conference"
        data = [
            {
                "type": "postback",
                "title": "WEST",
                "payload": "WEST"
            },
            {
                "type": "postback",
                "title": "EAST",
                "payload": "EAST"
            }
        ]
        response = template_message(sender_id, title, image_url, subtitle, data)


    def on_enter_pickDivision(self, event):
        print("==========================")
        print("Pick division")
        print("==========================")
        sender_id = event['sender']['id']
        text = "Pick a division"
        division = NBA_division(currentYear)
        quick_replies = []
        if (event['postback']['payload'].lower() == "east"):
            print(division['east'])
            for e in division['east']:
                quick_replies.append(
                    {
                        "content_type": "text",
                        "title": e,
                        "payload": e
                    }
                )
        else:
            for e in division['west']:
                quick_replies.append(
                    {
                        "content_type": "text",
                        "title": e,
                        "payload": e
                    }
                )
        response = quick_reply_message(sender_id, text, quick_replies)

    def on_enter_teams(self, event):
        sender_id = event['sender']['id']
        text = "Pick a team"
        quick_replies = []
        print("================================")
        print(event['message']['text'].lower())
        print("================================")
        teams = NBA_division_team(event['message']['text'], currentYear)
        for team in teams:
            quick_replies.append(
                {
                    "content_type": "text",
                    "title": team,
                    "payload": team
                }
            )
        response = quick_reply_message(sender_id, text, quick_replies)

    def on_enter_playerPpg(self, event):
        print("team info:")
        sender_id = event['sender']['id']
        text = word_tokenize(event['message']['text'].lower())
        team = ""
        for word in text:
            if word in all_teams:
                team = word
                break
        print("================================")
        print(team)
        print("================================")
        data = NBA_teamStats(team)
        response = send_text_message(sender_id, data)
        # quick reply to go back
        text = "What's next?"
        quick_replies = [
            {
                "content_type": "text",
                "title": "More NBA",
                "payload": "More NBA"
            },
            {
                "content_type": "text",
                "title": "Home",
                "payload": "Home"
            },
        ]
        response = quick_reply_message(sender_id, text, quick_replies)

    def on_enter_nbaGames(self, event):
        print("======================")
        print("Games Today")
        print("======================")
        data = NBA_score(currentDate)
        sender_id = event['sender']['id']
        response = send_text_message(sender_id, data)
        text = "More information?"
        quick_replies = [
            {
                "content_type": "text",
                "title": "Box Score",
                "payload": "Box Score"
            },
            {
                "content_type": "text",
                "title": "More NBA",
                "payload": "More NBA"
            },
            {
                "content_type": "text",
                "title": "Home",
                "payload": "Home"
            }
        ]
        response = quick_reply_message(sender_id, text, quick_replies)
        
    def on_enter_boxScore(self, event):
        print("======================")
        print("Box Score")
        print("======================")
        sender_id = event['sender']['id']
        data = NBA_boxScore(currentDate)
        response = send_text_message(sender_id, data)
        text = "What's next?"
        quick_replies = [
            {
                "content_type": "text",
                "title": "More NBA",
                "payload": "More NBA"
            },
            {
                "content_type": "text",
                "title": "Home",
                "payload": "Home"
            }
        ]
        response = quick_reply_message(sender_id, text, quick_replies)

    def on_enter_nbaNews(self, event):
        print("======================")
        print("News")
        print("======================")
        sender_id = event['sender']['id']
        data = NBA_news()
        response = send_text_message(sender_id, data)
        text = "What's next?"
        quick_replies = [
            {
                "content_type": "text",
                "title": "More NBA",
                "payload": "More NBA"
            },
            {
                "content_type": "text",
                "title": "Home",
                "payload": "Home"
            }
        ]
        response = quick_reply_message(sender_id, text, quick_replies)

    # def on_exit_state1(self):
    #     print('Leaving state1')

    # def on_exit_state2(self):
    #     print("Leaving state2")

    # def on_exit_state3(self):
    #     print("Leaving state3")


    


    # def on_exit_state1(self):
    #     print("Exiting state1")
    # def is_going_to_state1(self, event):

    #     if event.get("postback"):
    #         text = event['postback']['title']
    #         return text.lower() == 'nba games'
    #     elif event.get("message"):
    #         text = event['message']['text']
    #         return text.lower() == 'nba games'

    #     return False

    # def is_going_to_state2(self, event):
    #     if event.get("message"):
    #         text = event['message']['text']
    #         return text.lower() == '2'
    #     return False
    
    # def is_going_to_state3(self, event):
    #     if event.get("message"):
    #         text = event['message']['text']
    #         return text.lower() == '3'
    #     return False

    # def on_enter_state1(self, event):
    #     print("I'm entering state1")
    #     data = NBA_score()
    #     # NBA_score()
    #     sender_id = event['sender']['id']
    #     responese = send_text_message(sender_id, data)
    #     self.go_back()

    # def on_exit_state1(self):
    #     print('Leaving state1')

    # def on_enter_state2(self, event):
    #     print("I'm entering state2")
    #     para = translate()
    #     sender_id = event['sender']['id']
    #     responese = send_image_message(sender_id, "https://i.imgur.com/nbPuP6V.jpg")
    #     self.go_back()

    # def on_exit_state2(self):
    #     print('Leaving state2')

    # def on_enter_state3(self, event):
    #     print("I'm entering state3")
    #     sender_id = event['sender']['id']
    #     title="選擇服務"
    #     image_url="https://i.imgur.com/nbPuP6V.jpg"
    #     subtitle="請選擇"
    #     data = [
    #         {
    #             "type": "postback",
    #             "title": "NBA Games",
    #             "payload": "NBA Games"
    #         },
    #         {
    #             "type": "postback",
    #             "title": "法文單字查詢",
    #             "payload": "法文單字查詢"
    #         },
    #         {
    #             "type": "postback",
    #             "title": "Cafe",
    #             "payload": "Cafe"
    #         }
    #     ]
    #     responese = template_message(sender_id, title, image_url, subtitle, data)
    #     self.go_back()

    # def on_exit_state3(self):
    #     print("Leaving state3")
