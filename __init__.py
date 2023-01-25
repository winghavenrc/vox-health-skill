from mycroft import MycroftSkill, intent_file_handler

#import os
#import openai
import json

class VoxHealth(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('health.vox.intent')
    def handle_health_vox(self, message):
#        self.speak_dialog('health.vox')

        self.visit_types = ['health concern', 'wellness exam', 'vaccination', 'screening mammography']

        self.speak_dialog('visit.type', wait = True)


        visit_type = self.ask_selection(self.visit_types)


#        visit_type = self.get_response('visit.type')
#        self.speak_dialog('confirm.visit.type', {'visit': visit_type})

        confirmed = self.ask_yesno('confirm.visit.type', {'visit': visit_type})
        if confirmed != 'yes':
            self.speak_dialog('main.menu', expect_response=True)
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

                self.log.info(self.provider_list)
                self.speak_dialog("I can schedule with any of your currently active providers. Which one of these do you want to schedule with...", wait = True)

                selected = self.ask_selection(self.provider_list)
                self.speak_dialog('get.provider', data = {"provider": selected}, expect_response = True, wait=True)
            

# Closing file
                care_team_file.close()

#    @intent_file_handler('general.q.intent')
#    def handle_general_questions(self):

# Load your API key from an environment variable or secret management service
#        openai.api_key = ''

#        response = openai.Completion.create(model: "text-davinci-003", prompt = question, temperature=0, max_tokens=1000)
#        speakOut = response + " How else can I help you";
#        self.speak_dialog('general.q.answer', {'response': speakOut})


def create_skill():
    return VoxHealth()

