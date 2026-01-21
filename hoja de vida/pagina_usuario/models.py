from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Perfil(models.Model):
    SEXO_CHOICES = [('H', 'Hombre'), ('M', 'Mujer')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100, blank=True, default='', verbose_name='Descripción del perfil')
    activo = models.BooleanField(default=True, verbose_name='Perfil activo')
    lugar_nacimiento = models.CharField(max_length=60, blank=True, default='')
    cedula = models.CharField(max_length=10, unique=True)
    profesion = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono celular')
    telefono_convencional = models.CharField(max_length=15, blank=True, default='')
    telefono_fijo = models.CharField(max_length=15, blank=True, default='')
    direccion_domicilio = models.TextField(blank=True)
    direccion_trabajo = models.TextField(blank=True, default='')
    nacionalidad = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, default='')
    estado_civil = models.CharField(max_length=20, blank=True)
    licencia_conducir = models.CharField(max_length=50, blank=True)
    sitio_web = models.CharField(max_length=100, blank=True, default='', verbose_name='Sitio web')
    foto = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Experiencia(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='experiencias')
    empresa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100, blank=True, default='')
    lugar_empresa = models.CharField(max_length=100, blank=True, default='', verbose_name='Lugar de la empresa')
    email_empresa = models.EmailField(blank=True, default='', verbose_name='Email de la empresa')
    sitio_web_empresa = models.CharField(max_length=100, blank=True, default='', verbose_name='Sitio web de empresa')
    nombre_contacto_empresarial = models.CharField(max_length=100, blank=True, default='')
    telefono_contacto_empresarial = models.CharField(max_length=60, blank=True, default='')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    certificado = models.FileField(upload_to='certificados/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Experiencia'
        verbose_name_plural = 'Experiencias'
    
    def __str__(self):
        return f"{self.cargo} - {self.empresa}"

class Educacion(models.Model):
    ESTADO_CHOICES = [
        ('Completado', 'Completado'),
        ('En progreso', 'En progreso'),
        ('No completado', 'No completado'),
    ]
    
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='educaciones')
    titulo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Completado')
    graduado = models.BooleanField(default=False)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Educación'
        verbose_name_plural = 'Educaciones'
    
    def __str__(self):
        return f"{self.titulo} - {self.institucion}"

class Curso(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='cursos')
    nombre = models.CharField(max_length=150, default='', blank=True)
    nombre_curso = models.CharField(max_length=150, blank=True)
    institucion = models.CharField(max_length=100)
    entidad = models.CharField(max_length=100, blank=True, verbose_name='Entidad patrocinadora')
    nombre_contacto_auspicia = models.CharField(max_length=100, blank=True, default='')
    telefono_contacto_auspicia = models.CharField(max_length=60, blank=True, default='')
    email_empresa_patrocinadora = models.EmailField(blank=True, default='')
    total_horas = models.IntegerField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True, verbose_name='Descripción del curso')
    activo = models.BooleanField(default=True)
    certificado = models.FileField(upload_to='certificados_cursos/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
    
    def __str__(self):
        return self.nombre or self.nombre_curso

class Productos(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='productos')
    titulo = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150, blank=True, default='')
    tipo = models.CharField(max_length=50, verbose_name='Tipo (Académico o Laboral)')
    clasificador = models.CharField(max_length=100, blank=True, default='')
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    
    def __str__(self):
        return self.titulo or self.nombre

class Recomendacion(models.Model):
    TIPO_RECONOCIMIENTO = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]
    
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='recomendaciones')
    nombre_contacto = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=15)
    relacion = models.CharField(max_length=50, blank=True)
    tipo_reconocimiento = models.CharField(max_length=20, choices=TIPO_RECONOCIMIENTO, blank=True, default='')
    fecha_reconocimiento = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)
    entidad_patrocinadora = models.CharField(max_length=100, blank=True, default='')
    activo = models.BooleanField(default=True)
    certificado = models.FileField(upload_to='certificados_recomendaciones/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Recomendación'
        verbose_name_plural = 'Recomendaciones'
    
    def __str__(self):
        return self.nombre_contacto

class Habilidad(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='habilidades')
    nombre = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'
    
    def __str__(self):
        return self.nombre

class VentaGarage(models.Model):
    ESTADO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]
    
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='ventas_garage')
    nombre_producto = models.CharField(max_length=100)
    estado_producto = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    descripcion = models.TextField(blank=True)
    valor_bien = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Venta Garage'
        verbose_name_plural = 'Ventas Garage'
    
    def __str__(self):
        return self.nombre_producto