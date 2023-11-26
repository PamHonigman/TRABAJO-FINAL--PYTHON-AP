from django.contrib import admin
from .models import BandaHoraria, Curso, Alumno

class BandaHorariaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'horario_inicio', 'horario_fin')

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni')

# Register your models here.

admin.site.register(BandaHoraria, BandaHorariaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Alumno, AlumnoAdmin)