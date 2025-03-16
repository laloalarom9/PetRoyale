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
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # ✅ Asegurar que existe esta URL

]

# Configuración para servir archivos estáticos y multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Asegurar que Django sirva archivos subidos
