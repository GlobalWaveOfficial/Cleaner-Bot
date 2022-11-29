from discord.ui import View, Button

class PermissionUpdateButton(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Button(label="Re-Invite", url="https://discord.com/api/oauth2/authorize?client_id=831223247357607968&permissions=430973479952&scope=bot%20applications.commands"))