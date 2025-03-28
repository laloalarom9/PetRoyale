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
