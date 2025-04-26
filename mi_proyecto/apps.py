from django.apps import AppConfig

class MiProyectoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mi_proyecto'

    def ready(self):
        import mi_proyecto.signals  # 🚀 ¡ESTO ES LO QUE FALTABA!
