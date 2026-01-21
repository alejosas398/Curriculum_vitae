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

# --- CSS DE ALTA FIDELIDAD (NEÓN TÁCTICO) ---
CUSTOM_ADMIN_CSS = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');

        :root {
            --bg-obsidian: #ffffff;  /* Fondo blanco */
            --bg-card: #ffffff;     /* Fondo de las tarjetas */
            --emerald: #10b981;     /* Color verde */
            --emerald-glow: rgba(16, 185, 129, 0.2);
            --border: #30363d;      /* Borde oscuro */
            --text-main: #333333;    /* Texto oscuro para contraste */
            --header-bg: linear-gradient(90deg, #34d399 0%, #059669 100%); /* Fondo degradado verde */
            --header-text: #f1f1f1; /* Texto blanco brillante para el encabezado */
        }

        /* RESET TOTAL DASHBOARD */
        body, #container, html, #content, .module, #content-main {
            background-color: var(--bg-obsidian) !important;
            color: var(--text-main) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* --- BARRA DE ENCABEZADO (MARTI OBSIDIAN OPS) --- */
        .header {
            background: var(--header-bg) !important;
            color: #FFD700 !important;  /* Color dorado para el texto */
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); /* Sombra sutil para mejorar la visibilidad */
            font-size: 28px !important;  /* Aumentar el tamaño de la fuente */
            font-weight: 700 !important; /* Hacer el texto en negrita */
            padding: 15px 30px !important; /* Espaciado del encabezado */
            border-bottom: 3px solid #333 !important; /* Borde en la parte inferior */
        }

        /* --- TÍTULO PRINCIPAL DEL DASHBOARD (Sistema de Control Central) */
        #content > h1,
        #content h1,
        .content > h1,
        .content h1 {
            color: #000000 !important;  /* Texto negro */
        }

        /* --- SECCIONES (APP CONTAINERS: Autenticación, Página_Usuario) --- */
        .module {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
            overflow: hidden !important;
            margin-bottom: 35px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
        }

        .module h2, .module caption {
            background: linear-gradient(90deg, #064e3b 0%, #10b981 100%) !important;
            color: white !important;
            padding: 16px 20px !important;
            font-family: 'Fira Code', monospace !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 13px;
        }

        /* --- FILAS DE MODELOS --- */
        .module table { width: 100% !important; border-collapse: collapse !important; }
        .module table tr {
            border-bottom: 1px solid var(--border) !important;
            transition: 0.3s;
        }

        .module table tr:nth-child(odd) { background-color: #f5f5f5; }  /* Filas grises claras */
        .module table tr:nth-child(even) { background-color: #ffffff; } /* Filas blancas */
        .module table tr:hover {
            background: rgba(16, 185, 129, 0.1) !important;
        }

        .module th, .module td {
            padding: 18px 20px !important;
            vertical-align: middle !important;
            font-size: 14px !important;
        }

        .module th a {
            color: var(--emerald) !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            text-decoration: none !important;
        }

        /* --- BOTONES "AÑADIR" --- */
        .addlink, a.addlink {
            background: var(--emerald) !important;
            color: #000 !important;
            padding: 8px 18px !important;
            border-radius: 10px !important;
            font-weight: 800 !important;
            font-size: 10px !important;
            text-transform: uppercase !important;
            letter-spacing: 1px;
            border: none !important;
            box-shadow: 0 4px 0px #065f46 !important;
            transition: all 0.2s ease !important;
            display: inline-block !important;
        }

        .addlink:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 0px #065f46, 0 0 15px var(--emerald) !important;
            background: #fff !important;
        }

        /* --- BOTONES "CAMBIAR" --- */
        .changelink, a.changelink {
            color: #8b949e !important;
            font-size: 11px !important;
            text-decoration: none !important;
            border: 1px solid var(--border) !important;
            padding: 6px 14px !important;
            border-radius: 8px !important;
            transition: 0.3s;
        }

        .changelink:hover {
            border-color: var(--emerald) !important;
            color: white !important;
            background: var(--emerald-glow) !important;
        }

        /* --- ACCIONES RECIENTES --- */
        .module #recent-actions {
            background: var(--bg-card) !important;
            color: var(--text-main) !important;
            padding: 10px 20px !important;
            border-radius: 16px !important;
            font-size: 12px;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2) !important;
            margin-bottom: 0 !important;
            border: none !important;
            overflow: hidden !important;
        }

        /* --- GESTIÓN DE TÍTULOS --- */
        #title-container h1 {
            font-family: 'Fira Code', monospace !important;
            font-size: 20px !important;
            color: var(--emerald) !important;
            text-transform: uppercase;
        }
    </style>
"""

# --- ACTIVANDO CSS EN EL ADMIN ---
admin.site.site_header = mark_safe(f"MARTI OBSIDIAN OPS {CUSTOM_ADMIN_CSS}")

# --- HELPERS ---
def emerald_label(text, icon):
    return format_html(
        '<span style="display: flex; align-items: center; gap: 8px; color: #10b981; font-family: \'Fira Code\';">'
        '<i class="{}" style="font-size: 13px;"></i><span>{}</span></span>', icon, text
    )

# --- REGISTROS Y MODELOS ---
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user_tag', 'profesion', 'cedula', 'activo')
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

    def user_tag(self, obj):
        return emerald_label(obj.user.username.upper(), "fas fa-user-circle")
    
    readonly_fields = ('user',)


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('skill_tag', 'level_bar')

    def skill_tag(self, obj): 
        return emerald_label(obj.nombre.upper(), "fas fa-microchip")

    def level_bar(self, obj):
        # Intentamos sacar el nivel del objeto, si no existe ponemos 85 por defecto
        # Asegúrate de que 'nivel' sea el nombre del campo en tu models.py
        valor = getattr(obj, 'nivel', 85) 
        porcentaje = f"{valor}%"
        
        return format_html(
            '<div style="width:100px; background:#334155; height:6px; border-radius:3px; overflow:hidden;">'
            '<div style="width:{}; background:#10b981; height:100%; box-shadow:0 0 8px #10b981;"></div></div>',
            porcentaje  # <-- Este es el argumento que Django te pide
        )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_tag', 'status')

    def task_tag(self, obj):
        return emerald_label(obj.title, "fas fa-terminal")

    def status(self, obj):
        color = "#10b981" if obj.datecompleted else "#f87171"
        return format_html(
            '<b style="color:{}; font-size:10px;">[ {} ]</b>',
            color,
            "COMPLETED" if obj.datecompleted else "PENDING"
        )


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'activo', 'fecha_inicio', 'fecha_fin')
    list_filter = ('activo', 'fecha_inicio')
    search_fields = ('cargo', 'empresa', 'descripcion', 'email_empresa')
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
        }),
        ('Contacto Auspiciador', {
            'fields': ('nombre_contacto_auspicia', 'telefono_contacto_auspicia', 'email_empresa_patrocinadora')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'total_horas')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Certificado', {
            'fields': ('certificado',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
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
