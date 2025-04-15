from django.apps import AppConfig


class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'

    def ready(self):
        try:
            import services
            print("client.services imported successfully")
        except Exception as e:
            print(f"Error importing client.services: {e}")