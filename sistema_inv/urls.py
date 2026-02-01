from django.contrib import admin
from django.contrib.auth import views as auth_views
from usuarios.forms import CustomAuthenticationForm
from django.urls import path, include
from django.views.generic import RedirectView
from usuarios import views as usuarios_views



urlpatterns = [
    path('admin/', admin.site.urls),

    # Mostrar el login en la raíz; nombre 'login' usado por LOGIN_URL
    path('', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomAuthenticationForm), name='login'),
    # /login/ redirige a la raíz (opcional)
    path('login/', RedirectView.as_view(pattern_name='login', permanent=False)),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Apps bajo prefijos claros
    path('inventario/', include('inventario.urls')),
    path('usuarios/', include('usuarios.urls')),

    # Flujo de creación de cuenta pública
    path('crear-cuenta/', usuarios_views.crear_usuario_publico, name='crear_usuario_publico'),
]