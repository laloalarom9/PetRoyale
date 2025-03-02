from django.conf import settings

def avatar_context(request):
    if request.user.is_authenticated:
        avatar_path = "img/avatares/hombre.png" if request.user.genero == "hombre" else "img/avatares/mujer.png"
    else:
        avatar_path = "img/iconos/login.png"  # Imagen por defecto

    return {"avatar_path": avatar_path}

def user_groups_processor(request):
    """ Agrega los grupos del usuario al contexto de las plantillas. """
    if request.user.is_authenticated:
        user_groups = list(request.user.groups.values_list("name", flat=True))
    else:
        user_groups = []

    return {"user_groups": user_groups}



