from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    imagen_subida = forms.ImageField(required=False)  # Creamos un campo para subir imágenes

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']  # No incluimos imagen

    def save(self, commit=True):
        producto = super().save(commit=False)
        if self.cleaned_data['imagen_subida']:
            producto.imagen = self.cleaned_data['imagen_subida'].read()  # Guardamos la imagen en binario
        if commit:
            producto.save()
        return producto
