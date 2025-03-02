from django.shortcuts import render

def inicio(request):
    return render(request, "inicio.html")  # Se usa "inicio.html" desde templates

def reseñas(request):
    return render(request, "reseñas.html")  # Se usa "reseñas.html" desde templates
def pedidos(request):
    return render(request, "pedidos.html")  # Se usa "pedidos.html" desde templates
def Tienda(request):
    return render(request, "Tienda.html")  # Se usa "Tienda.html" desde templates
def faq(request):
    return render(request, "faq.html")  # Se usa faq.html" desde templates    
def login(request):
    return render(request, "login.html")  # Se usa "login.html" desde templates
def perfil(request):
    return render(request, "perfil.html")  # Se usa "perfil.html" desde templates
def registro(request):
    return render(request, "registro.html")  # Se usa "registro.html" desde templates
def password_reset(request):
    return render(request, "password_reset.html")  # Se usa "password_reset.html" desde templates
