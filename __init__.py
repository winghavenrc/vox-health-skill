from mycroft import MycroftSkill, intent_file_handler


class VoxHealth(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('health.vox.intent')
    def handle_health_vox(self, message):
#        self.speak_dialog('health.vox')
        self.speak_dialog('visit.type')

        self.visit_types = ['health concern', 'wellness exam', 'vaccination', 'screening mammography']

        visit_type = self.ask_selection(self.visit_types)


#        visit_type = self.get_response('visit.type')
#        self.speak_dialog('confirm.visit.type', {'visit': visit_type})

        confirmed = self.ask_yesno('confirm.visit.type', {'visit': visit_type})
        if confirmed == 'yes':
            self.speak_dialog('get.provider')
        else:
            self.speak_dialog('main.menu', expect_response=True)


def create_skill():
    return VoxHealth()

