from bottle import route, run, request, abort, static_file

from fsm import TocMachine
import os
PORT = os.environ['PORT']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

machine = TocMachine(
    states=[
        'user',
        'help',
        'moviePics',
        'nbaToday',
        'nbaStatus',
        'nbaStandings',
        'confStandings',
        'divStandings',
        'playerInfo',
        'pickDivision',
        'teams',
        'playerPpg',
        'nbaGames',
        'boxScore',
        'nbaNews'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'help',
            'conditions': 'is_going_to_help'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'moviePics',
            'conditions': 'is_going_to_moviePics'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'nbaToday',
            'conditions': 'is_going_to_nbaToday'
        },
        {
            'trigger': 'advance',
            'source': 'nbaToday',
            'dest': 'nbaStatus',
            'conditions': 'is_going_to_nbaStatus'
        },
        {
            'trigger': 'advance',
            'source': 'nbaStatus',
            'dest': 'nbaStandings',
            'conditions': 'is_going_to_nbaStandings'
        },
        {
            'trigger': 'advance',
            'source': 'nbaStandings',
            'dest': 'confStandings',
            'conditions': 'is_going_to_confStandings'
        },
        {
            'trigger': 'advance',
            'source': 'nbaStandings',
            'dest': 'divStandings',
            'conditions': 'is_going_to_divStandings'
        },
        {
            'trigger': 'advance',
            'source': 'nbaStatus',
            'dest': 'playerInfo',
            'conditions': 'is_going_to_playerInfo'
        },
        {
            'trigger': 'advance',
            'source': 'playerInfo',
            'dest': 'pickDivision',
            'conditions': 'is_going_to_pickDivision'
        },
        {
            'trigger': 'advance',
            'source': 'pickDivision',
            'dest': 'teams',
            'conditions': 'is_going_to_teams'
        },
        {
            'trigger': 'advance',
            'source': 'teams',
            'dest': 'playerPpg',
            'conditions': 'is_going_to_playerPpg'
        },
        {
            'trigger': 'advance',
            'source': 'nbaToday',
            'dest': 'nbaGames',
            'conditions': 'is_going_to_nbaGames'
        },
        {
            'trigger': 'advance',
            'source': 'nbaGames',
            'dest': 'boxScore',
            'conditions': 'is_going_to_boxScore'
        },
        {
            'trigger': 'advance',
            'source': 'nbaToday',
            'dest': 'nbaNews',
            'conditions': 'is_going_to_nbaNews'
        },
        {
            'trigger': 'advance',
            'source': [
                'nbaToday',
                'nbaStatus',
                'nbaStandings',
                'confStandings',
                'divStandings',
                'pickDivision',
                'teams',
                'playerPpg',
                'nbaGames',
                'boxScore',
                'nbaNews'
            ],
            'dest': 'user',
            'conditions': 'go_back_to_start'
        },
        {
            'trigger': 'advance',
            'source': [
                'nbaStandings',
                'confStandings',
                'divStandings',
                'pickDivision',
                'teams',
                'playerPpg',
                'nbaGames',
                'boxScore',
                'nbaNews'
            ],
            'dest': 'nbaToday',
            'conditions': 'go_back_to_nbaToday'
        },
        {
            'trigger': 'go_back',
            'source': [
                'help',
                'moviePics',
                'nbaToday',
                'nbaStatus'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        if 'messaging' in body['entry'][0]:
            event = body['entry'][0]['messaging'][0]
        else:
            print('not messaging')
            return

        try:
            machine.advance(event)
            return 'OK'
        except:
            print("SHIT")



@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    # show_fsm()
    run(host="0.0.0.0", port=PORT, debug=True, reloader=True)
    # run(host="localhost", port=5000, debug=True, reloader=True)