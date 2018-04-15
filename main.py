import requests, time
from secret import BOT_TOKEN
import logging

logging.basicConfig(filename="bot.log",level=logging.ERROR)

def reply_with_text(chat_id,text):
  data = {'chat_id': chat_id, 'text': text}
  try:
    post = requests.post('{0}/sendMessage'.format(tg_default_url), data = data)
  except requests.exceptions.RequestException:
    logging.error('Could not connect to Telegram API.')

def get_bitstamp(pair_str):
  base_url = 'https://www.bitstamp.net/api/v2/ticker'
  try:
    response = requests.get('{0}/{1}/'.format(base_url,pair_str))
    return response.json()
  except requests.exceptions.RequestException:
    logging.error('Could not connect to Bitstamp API.')
    return

def respond_to_command(chat_id,command):
  if '/start' in command:
    logging.debug('Received /start command. Replying.')
    reply_with_text(chat_id, response_messages['hello'])
  elif '/btc' in command:
    logging.debug('Received /btc command. Replying.')
    course = get_bitstamp('btcusd')
    if course:
      course_str = 'Bitcoin bid: $' + str(course['bid']) + '; ask: $' + str(course['ask'])
    else:
      course_str = response_messages['stock_market_error']
    reply_with_text(chat_id, course_str)
  elif '/eth' in command:
    logging.debug('Received /btc command. Replying.')
    course = get_bitstamp('ethusd')
    if course:
      course_str = 'Ethereum bid: $' + str(course['bid']) + '; ask: $' + str(course['ask'])
    else:
      course_str = response_messages['stock_market_error']
    reply_with_text(chat_id, course_str)
  else:
    reply_with_text(chat_id,  response_messages['wrong_command'])

response_messages = {
  hello: 'Hi and hello! To check coin prices in: /btc, /eth',
  stock_market_error: 'Could not connect to stock market. Try again later.',
  wrong_command : 'I don\'t uderstand you, sir. Commands: /start, /btc, /eth'
}

logging.debug('Starting bot. Listening for messages...')

last_update = 0
tg_base_url = 'https://api.telegram.org/bot' + BOT_TOKEN

while True:
  time.sleep(3) #every time we say 'continue', we get here
  #get updates from Telegram
  try:
    response = requests.get('{0}/getUpdates?offset='.format(tg_base_url) + str(last_update+1))
    if response.status_code != 200:
      logging.error('API Telegram returned HTTP status code: ' + str(response.status_code))
      continue
    updates = response.json()
  except requests.exceptions.RequestException:
    logging.error('Could not connect to API Telegram.')
  except ValueError:
    logging.error('Could not parse API Telegram response.')
    
  if not updates['ok']:
    logging.debug('Telegram API returned response that we did not expect.')
    continue
  if not updates['result']: #no updates
    continue
  #process incoming updates  
  for update in updates['result']:
    logging.debug('[update '+str(update['update_id'])+']')
    if not 'message' in update:
      logging.debug('Not a message type came in update. Dont know how to handle. Skipping.')
      continue
    #request from user
    command = update['message']['text']
    chat_id =  update['message']['chat']['id']

    respond_to_command(chat_id,command)
    last_update = update['update_id']

#TODO: handle Ctrl+Z