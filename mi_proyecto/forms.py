from django import forms
from .models import Producto
from .models import Reseña

class ProductoForm(forms.ModelForm):
    imagen = forms.ImageField(required=False)  # ✅ Ahora coincide con el modelo

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'categoria', 'marca', 'edad_recomendada', 'tamano_mascota']  # ✅ Incluimos nuevos campos

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if Producto.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("⚠️ Ya existe un producto con este nombre. Intenta con otro.")
        return nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        producto_id = self.instance.id  # Obtener el ID del producto actual

        # Si hay otro producto con el mismo nombre, excepto el que se está editando
        if Producto.objects.filter(nombre=nombre).exclude(id=producto_id).exists():
            raise forms.ValidationError("⚠️ Ya existe un producto con este nombre. Intenta con otro.")

        return nombre
    
class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['contenido', 'valoracion']  
        widgets = {
            'valoracion': forms.NumberInput(attrs={
                'min': 1,
                'max': 5
            }),
        }
        
class SuscripcionForm(forms.Form):
    producto_id = forms.IntegerField(widget=forms.HiddenInput())
    duracion = forms.ChoiceField(
        choices=[("3", "3 meses"), ("6", "6 meses"), ("12", "12 meses")],
        widget=forms.Select()
    )


# mi_proyecto/forms.py
from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(attrs={"type": "text", "placeholder": "dd/mm/aaaa"})
    )

    class Meta:
        model = Mascota
        fields = ["nombre", "especie", "raza", "fecha_nacimiento", "foto"]

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class CrearPerfilForm(forms.ModelForm):
    ROL_CHOICES = [
        ("administrador", "Administrador"),
        ("operador", "Operador"),
        ("repartidor", "Repartidor"),
        ("cliente", "Cliente"),
    ]

    rol = forms.ChoiceField(choices=ROL_CHOICES, label="Tipo de Perfil")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirmar_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "rol"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar_password")

        if password and confirmar and password != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("⚠️ El nombre de usuario ya está en uso. Elige otro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("⚠️ Este correo electrónico ya está registrado.")
        return email


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        rol = self.cleaned_data["rol"]

        if rol == "administrador":
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False

        if commit:
            user.save()
            if rol != "administrador":
                group, _ = Group.objects.get_or_create(name=rol)
                user.groups.add(group)

        return user



