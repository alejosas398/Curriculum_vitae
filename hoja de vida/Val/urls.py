"""
URL configuration for Val project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from pagina_usuario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health_check, name='health_check'),
    
    # --- RUTAS GENERALES ---
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.signout, name='logout'),
    
    # --- TAREAS ---
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),

    # --- RUTAS DE LA HOJA DE VIDA ---
    path('hoja-de-vida/', views.ver_hoja_de_vida, name='ver_cv'),
    path('hoja-de-vida/<str:username>/', views.ver_hoja_de_vida, name='ver_cv_usuario'),
    path('cv/descargar/', views.descargar_cv_pdf, name='descargar_cv_pdf'),
    path('panel-admin/', views.panel_admin_perfil, name='panel_admin_perfil'),

    # --- PERFIL Y EDICIÓN ---
    path('perfil/editar/', views.edit_perfil, name='edit_perfil'),

    # --- AGREGAR CONTENIDO ---
    path('perfil/producto/nuevo/', views.add_productos, name='add_productos'),
    path('perfil/recomendacion/nueva/', views.add_recomendacion, name='add_recomendacion'),
    path('perfil/educacion/nueva/', views.add_educacion, name='add_educacion'),
    path('perfil/experiencia/nueva/', views.add_experiencia, name='add_experiencia'),
    path('perfil/habilidad/nueva/', views.add_habilidad, name='add_habilidad'),
    path('perfil/curso/nuevo/', views.add_curso, name='add_curso'),

    # --- EDITAR CONTENIDO ---
    path('perfil/producto/editar/<int:pk>/', views.edit_productos, name='edit_productos'),
    path('perfil/recomendacion/editar/<int:pk>/', views.edit_recomendacion, name='edit_recomendacion'),
    path('perfil/educacion/editar/<int:pk>/', views.edit_educacion, name='edit_educacion'),
    path('perfil/experiencia/editar/<int:pk>/', views.edit_experiencia, name='edit_experiencia'),
    path('perfil/habilidad/editar/<int:pk>/', views.edit_habilidad, name='edit_habilidad'),
    path('perfil/curso/editar/<int:pk>/', views.edit_curso, name='edit_curso'),

    # --- ELIMINAR CONTENIDO ---
    path('perfil/curso/eliminar/<int:pk>/', views.eliminar_curso, name='delete_curso'),
    path('perfil/producto/eliminar/<int:pk>/', views.eliminar_productos, name='delete_productos'),
    path('perfil/recomendacion/eliminar/<int:pk>/', views.eliminar_recomendacion, name='delete_recomendacion'),
    path('perfil/educacion/eliminar/<int:pk>/', views.eliminar_educacion, name='delete_educacion'),
    path('perfil/habilidad/eliminar/<int:pk>/', views.eliminar_habilidad, name='delete_habilidad'),
    path('perfil/experiencia/eliminar/<int:pk>/', views.eliminar_experiencia, name='delete_experiencia'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)