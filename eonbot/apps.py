from django.apps import AppConfig
import os
from eonchatapp import settings

class EonquoraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eonbot'

    def ready(self):
        # Create or reset the restart flag
        with open('server_restart_flag.txt', 'w') as f:
            f.write('1')