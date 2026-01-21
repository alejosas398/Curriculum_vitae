from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Task, Perfil, Experiencia, Educacion,
    Curso, Recomendacion, Productos, Habilidad, VentaGarage
)

# --- CONFIGURACIÓN DE TÍTULOS ---
admin.site.site_header = "MARTI OBSIDIAN OPS"
admin.site.site_title = "Obsidiana Admin"
admin.site.index_title = "Sistema de Control Central"

# --- HELPERS ---
def emerald_label(text, icon):
    return format_html(
        '<span style="color: #10b981; font-weight: bold;">{}</span>', text
    )

# --- REGISTROS Y MODELOS ---
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'profesion', 'cedula', 'activo')
    list_filter = ('activo', 'sexo', 'estado_civil')
    search_fields = ('user__first_name', 'user__last_name', 'cedula', 'profesion')
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'descripcion', 'foto')
        }),
        ('Datos Personales', {
            'fields': ('cedula', 'sexo', 'fecha_nacimiento', 'lugar_nacimiento', 'nacionalidad')
        }),
        ('Estado Civil', {
            'fields': ('estado_civil', 'licencia_conducir')
        }),
        ('Profesional', {
            'fields': ('profesion', 'sitio_web')
        }),
        ('Contacto', {
            'fields': ('telefono', 'telefono_convencional', 'telefono_fijo', 'direccion_domicilio', 'direccion_trabajo')
        }),
        ('Estado del Perfil', {
            'fields': ('activo',)
        }),
    )
    readonly_fields = ('user',)


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'important', 'datecompleted')
    list_filter = ('important', 'datecompleted')
    search_fields = ('title', 'description')


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'activo', 'fecha_inicio', 'fecha_fin')
    list_filter = ('activo', 'fecha_inicio')
    search_fields = ('cargo', 'empresa', 'descripcion')
    fieldsets = (
        ('Información Básica', {
            'fields': ('perfil', 'empresa', 'cargo', 'puesto', 'lugar_empresa')
        }),
        ('Contacto Empresarial', {
            'fields': ('nombre_contacto_empresarial', 'telefono_contacto_empresarial', 'email_empresa', 'sitio_web_empresa')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'certificado')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )

@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'estado', 'graduado')
    list_filter = ('estado', 'graduado', 'fecha_inicio')
    search_fields = ('titulo', 'institucion')
    fieldsets = (
        ('Información Académica', {
            'fields': ('perfil', 'titulo', 'institucion')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado', {
            'fields': ('estado', 'graduado')
        }),
    )

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre_curso', 'institucion', 'total_horas', 'activo')
    list_filter = ('activo', 'fecha_inicio', 'institucion')
    search_fields = ('nombre_curso', 'nombre', 'institucion', 'entidad')
    fieldsets = (
        ('Información del Curso', {
            'fields': ('perfil', 'nombre_curso', 'nombre', 'institucion', 'entidad')
    )

@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    list_display = ('nombre_contacto', 'tipo_reconocimiento', 'relacion', 'activo')
    list_filter = ('activo', 'relacion', 'tipo_reconocimiento')
    search_fields = ('nombre_contacto', 'telefono_contacto', 'entidad_patrocinadora')
    fieldsets = (
        ('Información de Contacto', {
            'fields': ('perfil', 'nombre_contacto', 'telefono_contacto', 'relacion')
        }),
        ('Reconocimiento', {
            'fields': ('tipo_reconocimiento', 'fecha_reconocimiento', 'entidad_patrocinadora')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Certificado', {
            'fields': ('certificado',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'activo')
    list_filter = ('activo', 'tipo')
    search_fields = ('titulo', 'nombre', 'descripcion')
    fieldsets = (
        ('Información del Producto', {
            'fields': ('perfil', 'titulo', 'nombre', 'tipo', 'clasificador')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'estado_producto', 'valor_bien', 'activo')
    list_filter = ('activo', 'estado_producto')
    search_fields = ('nombre_producto', 'descripcion')
    fieldsets = (
        ('Información del Producto', {
            'fields': ('perfil', 'nombre_producto', 'estado_producto')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'valor_bien')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
