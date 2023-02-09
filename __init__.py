from mycroft import MycroftSkill, intent_file_handler

#import os
#import openai
import json
import datetime
import requests


class VoxHealth(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('health.vox.intent')

    def handle_health_vox(self, message):
#        self.speak_dialog('health.vox')

        self.visit_types = ['health concern', 'wellness exam', 'vaccination', 'screening mammography']

        self.speak_dialog('visit.type', wait = True)


        visit_type = self.ask_selection(self.visit_types, min_conf = .4)


#        visit_type = self.get_response('visit.type')
#        self.speak_dialog('confirm.visit.type', {'visit': visit_type})

        confirmed = self.ask_yesno('confirm.visit.type', {'visit': visit_type})
        if confirmed != 'yes':
            self.speak_dialog('main.menu', expect_response=False)
# Opening JSON file
        else:
            self.log.info(self.file_system.path)

            with self.file_system.open('care_team.json', "r") as care_team_file:
#            f = open('care_team.json')
  
# returns JSON object as 
# a dictionary
                care_team = json.load(care_team_file)

#            (data['people1'][0]
# Iterating through the json
# list
     
    # for printing the key-value pair of
    # nested dictionary for loop can be used

                self.provider_list = []

                for provider in care_team['entry']:
                    name = provider['name']
                    specialty = provider['specialty']
                    self.log.info(name)
                    self.log.info(specialty)

#                    lastname = provider['name']['family'];
#                    firstname = name['given'];
#                    fullname = firstname + " " + lastname + " " + specialty;
#                    self.provider_list.append(fullname)
                    self.provider_list.append(specialty)

                care_team_file.close()

                self.log.info(self.provider_list)
                self.speak_dialog("I can schedule with any of your currently active providers. Which one of these do you want to schedule with...", wait = True)

                selected = self.ask_selection(self.provider_list)
                self.speak_dialog('get.provider', data = {"provider": selected}, expect_response = True, wait=True)

#               find first appts available from today
                timeSlots = find_first(self)
            




def find_first(self):
    timeSlots = []

    # get the current date and time
    today = datetime.date.today()

    tomorrow = datetime.date(today.year, today.month, today.day+1)

    self.log.info(today)
    self.log.info(tomorrow)

    searchDate = today
    day = 0

    while day < 14:

      availableTimes = mt_find_available_appts(self, searchDate, 'am', 'America/Chicago')
      if (availableTimes.start.length > 0):
        self.log.info("Meditech FindFirst Found a date with availability ", searchDate)
#               meditech.revokeToken(handlerInput); // see revokeToken for why to call this now
        break
       
      searchDate = datetime.date(searchDate.year, searchDate.month, searchDate.day+1)
    

    return timeSlots



def mt_find_available_appts(self, searchDate, ampm, userTimezone):

# for a given searchDate

  ### Get a Meditech token

  BASE_HOST = 'https://greenfield-apis.meditech.com'
  IMPLEMENTATION_VERSION = '/v1/argoScheduling/STU3'
  OAUTH_AUTHORIZE = '/oauth/authorize'
  OAUTH_TOKEN = '/oauth/token'
  CLIENT_ID = 'Voxhealth@8c76706c946d4426a648b5c2789cd7e1'
  CLIENT_SECRET = 'gT_463aNSJiGJA7jvsCM4g=='
  GRANT_TYPE = 'client_credentials'
  SCOPE = 'patient/ArgoScheduling.* patient/ArgoScheduling.read'
  BASE_APPOINTMENT = '/Appointment'
  FIND_APPOINTMENTS = '/$find'
  HOLD_APPOINTMENT = '/$hold'
  BOOK_APPOINTMENT = '/$book'



# Define the OAuth2 client ID and secret
  client_id = CLIENT_ID
  client_secret = CLIENT_SECRET

# Define the OAuth2 token endpoint
  token_url = BASE_HOST + OAUTH_TOKEN

# Request an access token


  token_req_payload = {'grant_type': 'client_credentials', 'scope': 'patient/ArgoScheduling.* patient/ArgoScheduling.read'}

  response = requests.post(token_url, data=token_req_payload, verify=False, allow_redirects=False, auth=(client_id, client_secret))

#  response = requests.post(token_url, data={"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret })
  self.log.info(response)

# Parse the JSON response
  response_data = json.loads(response.text)

# Extract the access token from the response
  access_token = response_data["access_token"]

# Define the API endpoint
  url = BASE_HOST + IMPLEMENTATION_VERSION + BASE_APPOINTMENT + FIND_APPOINTMENTS

# Set the Authorization header with the access token as a bearer token
  headers = {
    "Authorization": "Bearer " + access_token
  }

  begin = searchDate
  end = datetime.date(searchDate.year, searchDate.month, searchDate.day+1)

# Define the parameters as a dictionary
  params = {
        "practitioner": '5563b254-66b1-5203-80e3-bef0be824970',  #Meehan
        "location": '1b2332fb-8906-5264-86e0-df72e983f350',  #Cardiology
        'service-type': '257585005',    #ECHO
        "start": begin,
        "end": end
  }

# Make a GET request to the API
  response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
  if response.status_code == 200:
    # Parse the JSON data returned by the API
    apptSlots = response.json()
    self.log.info(apptSlots)

    total = apptSlots["total"];
    if (total == 0):
        # means there's no appointments available
      return False

    start = []
    id = []

    index = 0
    while index < total:
      start = apptSlots["entry"][index]["resource"]["start"];
      end = apptSlots["entry"][index]["resource"]["end"];
      id = apptSlots["entry"][index]["resource"]["id"];

      localStart = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
      meridien = localStart.strftime("%p")

      save = False

      if ampm in ["AM", "MO", "morning"]:
        if meridien == "AM":
            save = True
      elif ampm in ["PM", "AF", "afternoon"]:
        if meridien == "PM":
            save = True
      if save == True:
        start.append(localStart);
        id.append(id);

      index += 1

  else:
    # Handle error
    self.log.info("Request failed with status code:", response.status_code)

  availableTimes = { "start": start, "id": id }

  return availableTimes



def create_skill():
    return VoxHealth()

