from mycroft import MycroftSkill, intent_file_handler


class VoxHealth(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('health.vox.intent')
    def handle_health_vox(self, message):
        self.speak_dialog('health.vox')

        visit_type = self.get_response('visit.type')
        self.speak_dialog('confirm.visit.type', {'visit': visit_type})


def create_skill():
    return VoxHealth()

