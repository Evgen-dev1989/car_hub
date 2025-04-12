from django.apps import AppConfig


class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'
    def ready(self):
        try:
            import services
            print("car_hub.services imported successfully")
        except Exception as e:
            print(f"Error importing car_hub.services: {e}")