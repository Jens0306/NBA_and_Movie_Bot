from bottle import route, run, request, abort, static_file

from fsm import TocMachine
import os
PORT = os.environ['PORT']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

machine = TocMachine(
    states=[
        'user',
        'start',
        'nbaToday',
        'nbaStatus',
        'nbaStandings',
        'playerInfo',
        'pickDivision',
        'teams',
        'playerPpg',
        'nbaGames',
        'boxScore',
        'nbaNews',
        'state10',
        'standing',
        'players_info',
        'translate',
        'trans_result'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'start',
            'conditions': 'is_going_to_start'
        },
        {
            'trigger': 'advance',
            'source': 'start',
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
            'source': 'start',
            'dest': 'translate',
            'conditions': 'search_word'
        },
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'translate',
            'conditions': 'search_word'
        },
        {
            'trigger': 'advance',
            'source': [
                'nbaToday',
                'nbaStatus',
                'nbaStandings',
                'pickDivision',
                'teams',
                'playerPpg',
                'nbaGames',
                'boxScore',
                'nbaNews'
            ],
            'dest': 'start',
            'conditions': 'go_back_to_start'
        },
        {
            'trigger': 'advance',
            'source': [
                'nbaStandings'
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
                'start',
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
    # run(host="127.0.0.1", port="localhost", debug=True, reloader=True)