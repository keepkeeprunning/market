import requests, time
from secret import BOT_TOKEN

#app loop
#read updates
#loop through updates
#parse query
#send response
#update last_update
#sleep

def reply_with_text(chat_id,text):
  if not isinstance(text, str):
    print('reply_with_text: Error. Passed variable is not string')
    return
  try:
    post = requests.post(default_url + '/sendMessage' \
                            , data = {'chat_id': chat_id, 'text': text})
  except requests.exceptions.RequestException:
    print('reply_with_text: Error. Could not connect to Telegram API.')

def get_bitstamp(pair_str):
  base_url = 'https://www.bitstamp.net/api/v2/ticker/'
  try:
    res = requests.get(base_url + pair_str + '/')
    return res.json()
  except requests.exceptions.RequestException:
    print('exception while connecting to Bitstamp')
    return

print('Starting bot. Listening for messages...')

last_update = 0
default_url = 'https://api.telegram.org/bot' + BOT_TOKEN
while True:
  time.sleep(3) #every time we say 'continue', we get here
  try:
    resp = requests.get(default_url +'/getUpdates?offset=' + str(last_update+1))
    if resp.status_code != 200:
      print('main_loop: Error. API Telegram returned HTTP status code: ' + str(resp.status_code))
      continue
    updates = resp.json()
  except requests.exceptions.RequestException:
    print('main_loop: Error. Could not connect to API Telegram.')
  except ValueError:
    print('main_loop: Error. Could not parse API Telegram response.')

  if not updates['ok']:
    print('main_loop: Telegram API returned response that we did not expect.')
    continue
  if not updates['result']: #no updates
    continue

  for update in updates['result']:
    print('[update '+str(update['update_id'])+']')
    if not ('message' in update):
      print('Not a message type came in update. Dont know how to handle. Skipping.')
      continue
    #parse request
    message = update['message']['text']
    chat_id =  update['message']['chat']['id']
    #send response
    if '/start' in message:
      print('Received /start command. Replying.')
      reply_with_text(chat_id, 'Hi and hello! To check coin prices in: /btc, /eth')
    elif '/btc' in message:
      print('Received /btc command. Replying.')
      course = get_bitstamp('btcusd')
      if course:
        course_str = 'Bitcoin bid: $' + str(course['bid']) + '; ask: $' + str(course['ask'])
      else:
        course_str = 'Could not connect to stock market. Try again later.'
      reply_with_text(chat_id, course_str)
    elif '/eth' in message:
      print('Received /btc command. Replying.')
      course = get_bitstamp('ethusd')
      if course:
        course_str = 'Ethereum bid: $' + str(course['bid']) + '; ask: $' + str(course['ask'])
      else:
        course_str = 'Could not connect to stock market. Try again later.'
      reply_with_text(chat_id, course_str)
    else:
      reply_with_text(chat_id, 'I don\'t uderstand you, sir. Commands: /start, /btc, /eth' )
    last_update = update['update_id']

#TODO: handle Ctrl+Z