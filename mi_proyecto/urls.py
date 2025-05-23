from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mi_proyecto.views import inicio, editar_perfil, eliminar_cuenta  # Importa solo lo necesario
from mi_proyecto import views  # Importa vistas correctamente
from django.contrib.auth import views as auth_views  # Importar vistas de autenticación
from mi_proyecto.views import lista_productos, agregar_producto, editar_producto, eliminar_producto
from mi_proyecto import views
from mi_proyecto.views import lista_productos, agregar_producto, editar_producto, eliminar_producto
from mi_proyecto.views import checkout, procesar_compra  # ✅ Asegúrate de importar procesar_compra
from .views import crear_perfil#####CREAR USUARIO
from mi_proyecto.views import (
    inicio,
    editar_perfil,
    eliminar_cuenta,
    agregar_mascota,        # Asegúrate de tener estas también
    editar_mascota,         # ⬅️ ESTA es la que falta
    eliminar_mascota,
)
from .views import lista_perfiles, crear_perfil
from .views import lista_perfiles, crear_perfil, editar_rol_usuario
from .views import lista_perfiles, crear_perfil, editar_rol_usuario, eliminar_perfil
from django.shortcuts import redirect
from .views import UpdateLocationView #Repartidor
from .views import repartidor_view
from .views import asignar_pedidos_a_ruta

urlpatterns = [
    # Administrador
    path("admin/", admin.site.urls),

    # Páginas principales
    path("", inicio, name="inicio"),
    path("reseñas/", views.reseñas, name="reseñas"),
    path("pedidos/", views.pedidos, name="pedidos"),
    path("Tienda/", views.Tienda, name="Tienda"),
    path("faq/", views.faq, name="faq"),

    # Autenticación
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registro/", views.registro_view, name="registro"),
    path("perfil/", editar_perfil, name="perfil"),
    path("eliminar-cuenta/", eliminar_cuenta, name="eliminar_cuenta"),

    # Recuperación de contraseña (usando vistas de Django)
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

    # Gestión de productos
    path("productos/", views.lista_productos, name="lista_productos"),
    path("productos/agregar/", views.agregar_producto, name="agregar_producto"),
    path("productos/editar/<int:producto_id>/", views.editar_producto, name="editar_producto"),
    path("productos/eliminar/<int:producto_id>/", views.eliminar_producto, name="eliminar_producto"),
    path("producto/<int:producto_id>/", views.producto_detalle, name="producto_detalle"),
    path('carrito/', views.carrito, name='carrito'),  # Esta es la URL para el carrito
    path('carrito/', views.carrito, name='carrito'),  # ✅ Esta es la URL para el carrito
    path('checkout/', views.checkout, name='checkout'),  # ✅ Nueva ruta para checkout
    path('carrito/reducir/<int:producto_id>/', views.reducir_cantidad_carrito, name='reducir_cantidad_carrito'),
    path('carrito/reducir-suscripcion/<str:producto_id>/', views.reducir_suscripcion_carrito, name='reducir_suscripcion_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # ✅ Asegurar que existe esta URL
    path("checkout/procesar/", views.procesar_compra, name="procesar_compra"),
    path("confirmar_compra/", procesar_compra, name="confirmar_compra"),  # ✅ Agregar esta línea
    path("cambiar-mascota/<int:pedido_id>/", views.cambiar_mascota, name="cambiar_mascota"),


   
    #Reseñas
    path('producto/<int:producto_id>/reseña/', views.crear_reseña, name='crear_reseña'),
    path("producto/1/reseña/", lambda request: redirect("crear_reseña")),

    #Suscripciones
    # Suscripciones
    path("suscripciones/", views.suscripciones, name="suscripciones"),
    path("suscripciones/seleccionar/", views.seleccionar_suscripcion, name="seleccionar_suscripcion"),
    path("suscripcion/agregar/", views.agregar_suscripcion_al_carrito, name="agregar_suscripcion_al_carrito"),
    path('suscripciones/gestionar/', views.gestionar_suscripcion, name='gestionar_suscripcion'),
    path("suscripciones/cancelar/<int:pedido_id>/", views.cancelar_suscripcion, name="cancelar_suscripcion"),
    path("suscripciones/reactivar/<int:pedido_id>/", views.reactivar_suscripcion, name="reactivar_suscripcion"),
    path("perfil/mascota/editar/<int:pk>/", editar_mascota, name="editar_mascota"),
    path("perfil/mascota/eliminar/<int:pk>/", eliminar_mascota, name="eliminar_mascota"),
    path("perfil/mascota/agregar/", agregar_mascota, name="agregar_mascota"),
    path("desvincular-mascota/<int:pedido_id>/", views.desvincular_mascota, name="desvincular_mascota"),
    path('eliminar/<int:pedido_id>/', views.eliminar_suscripcion, name='eliminar_suscripcion'),

    #CREAR PERFILES
    path("crear_perfil/", crear_perfil, name="crear_perfil"),
    path("perfiles/", lista_perfiles, name="lista_perfiles"),
    path("perfiles/<int:user_id>/editar/", editar_rol_usuario, name="editar_rol_usuario"),
    path("perfiles/<int:user_id>/eliminar/", eliminar_perfil, name="eliminar_perfil"),
    path('reseñas/eliminar/<int:reseña_id>/', views.eliminar_reseña, name='eliminar_reseña'),

    #Repartidor
    path('repartidor/', repartidor_view, name='repartidor'),
    path('repartidor/', UpdateLocationView.as_view(), name='repartidor'), 
    path('repartidor/', UpdateLocationView.as_view(), name='update-location'),
    path('update-location/', views.update_location, name='update-location'),
    path("marcar-entregado/", views.marcar_entregado, name="marcar-entregado"),
    path("marcar-mes-entregado/", views.marcar_mes_entregado, name="marcar-mes-entregado"),
    path("api/estado-meses-entregados/", views.estado_meses_entregados, name="estado-meses-entregados"),


    
    

    #Ruta
    path('asignar_pedidos/', asignar_pedidos_a_ruta, name='asignar_pedidos'),
    path("rutas/", views.listar_rutas, name="listar_rutas"),
    
    #Donaciones
    path("donaciones/", views.donaciones_view, name="donaciones"),
    path("donacion/confirmar/", views.confirmar_donacion, name="confirmar_donacion"),
    path("donacion/confirmar/", views.confirmar_donacion, name="confirmar_donacion"),


]

# Configuración para servir archivos estáticos y multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Asegurar que Django sirva archivos subidos