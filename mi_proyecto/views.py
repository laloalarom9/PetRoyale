from django.shortcuts import render

def inicio(request):
    return render(request, "inicio.html")  # Se usa "inicio.html" desde templates
