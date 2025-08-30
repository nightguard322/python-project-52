from django.apps import AppConfig
import os
import rollbar

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


    rollbar.init(
        access_token=os.getenv('ROLLBACK_ACCESS_TOKEN'),
        environment=os.getenv('DJANGO_ENVIRONMENT'),
        code_version=os.getenv('GIT_COMMIT')
    )
    
rollbar.report_message('Rollbar is configured correctly', 'info')
rollbar.report_message('Rollbar is configured correctly', 'info')
rollbar.report_message("Тестовое сообщение из Django", 'info')
        