from django.shortcuts import render

def inicio(request):
    return render(request, "inicio.html")  # Se usa "inicio.html" desde templates

def reseñas(request):
    return render(request, "reseñas.html")  # Se usa "reseñas.html" desde templates
def pedidos(request):
    return render(request, "pedidos.html")  # Se usa "pedidos.html" desde templates