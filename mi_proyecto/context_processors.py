from django.conf import settings
from django.contrib.auth.models import Group
def avatar_context(request):
    if request.user.is_authenticated:
        avatar_path = "img/avatares/hombre.png" if request.user.genero == "hombre" else "img/avatares/mujer.png"
    else:
        avatar_path = "img/iconos/login.png"  # Imagen por defecto

    return {"avatar_path": avatar_path}

def user_groups_processor(request):
    if request.user.is_authenticated:
        user_groups = list(request.user.groups.values_list("name", flat=True))
        is_repartidor = "repartidor" in user_groups
    else:
        user_groups = []
        is_repartidor = False

    return {"user_groups": user_groups, "is_repartidor": is_repartidor}



