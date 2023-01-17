from mycroft import MycroftSkill, intent_file_handler


class VoxHealth(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('health.vox.intent')
    def handle_health_vox(self, message):
        self.speak_dialog('health.vox')


def create_skill():
    return VoxHealth()

