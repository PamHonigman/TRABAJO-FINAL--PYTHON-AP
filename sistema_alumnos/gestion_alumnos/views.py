import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Alumno, Curso
import csv
import os
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def cargar_alumno(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if csv_file.name.endswith('.csv'):
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
                next(csv_data)

                for row in csv_data:
                    dni, nombre, apellido, telefono, correo_electronico, curso_id = row
                    
                    alumno, created = Alumno.objects.update_or_create(
                        dni=dni,
                        defaults={
                            'nombre': nombre,
                            'apellido': apellido,
                            'telefono': telefono,
                            'correo_electronico': correo_electronico,
                            'curso_id': curso_id,
                        }
                    )

                return JsonResponse({'message': 'Alumnos cargados correctamente.'}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'El archivo debe ser un archivo CSV válido.'}, status=400)
    else:
        return JsonResponse({'error': 'Debe proporcionar un archivo CSV para cargar.'}, status=400)


def listar_alumno(request):
    alumnos = Alumno.objects.all()

    if not alumnos:
        return JsonResponse({'error': 'No hay alumnos cargados.'}, status=404)

    serialized_alumnos = []
    for alumno in alumnos:
        serialized_alumnos.append({
            'nombre': alumno.nombre,
            'apellido': alumno.apellido,
            'dni': alumno.dni,
            'telefono': alumno.telefono,
            'correo_electronico': alumno.correo_electronico,
            'curso': alumno.curso.nombre if alumno.curso else None,
            'banda_horaria': alumno.curso.banda_horaria.nombre if alumno.curso else None,
        })

    return JsonResponse({'alumnos': serialized_alumnos})


def obtener_alumno(request, dni):
    alumno = get_object_or_404(Alumno, dni=dni)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{alumno.apellido}_{alumno.nombre}_info.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerow(['nombre', 'apellido', 'dni', 'telefono', 'correo_electronico', 'curso', 'banda_horaria'])
    
    try:
        csv_writer.writerow([
            alumno.nombre,
            alumno.apellido,
            alumno.dni,
            alumno.telefono,
            alumno.correo_electronico,
            alumno.curso.nombre if alumno.curso else None,
            alumno.curso.banda_horaria.nombre if alumno.curso else None,
        ])

        return response

    except Exception as e:
        return JsonResponse({'error': f'Error al generar el archivo CSV: {str(e)}'}, status=500)
    
@csrf_exempt
def modificar_alumno(request, dni):
    alumno = get_object_or_404(Alumno, dni=dni)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))

            required_fields = ['nombre', 'apellido', 'telefono', 'correo_electronico']
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Error en el formato JSON de la solicitud.'}, status=400)

            alumno.nombre = data['nombre']
            alumno.apellido = data['apellido']
            alumno.telefono = data['telefono']
            alumno.correo_electronico = data['correo_electronico']
            
            alumno.save()

            return JsonResponse({'message': 'Alumno modificado correctamente.'}, status=200)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido. Utiliza el método PUT para modificar al alumno.'}, status=405)


@csrf_exempt
def eliminar_alumno(request, dni):
    alumno = get_object_or_404(Alumno, dni=dni)

    if request.method == 'DELETE':
        alumno.delete()

        return JsonResponse({'message': 'Alumno eliminado correctamente.'}, status=200)
    else:
        return JsonResponse({'error': 'Metodo no permitido. Utiliza el metodo DELETE para eliminar al alumno.'}, status=405)


@csrf_exempt
def asignar_curso(request, dni, id_curso):
    alumno = get_object_or_404(Alumno, dni=dni)
    curso = get_object_or_404(Curso, id=id_curso)

    if request.method == 'POST':
        alumno.curso = curso
        alumno.save()

        return JsonResponse({'message': f'Curso asignado correctamente al alumno con DNI {dni}.'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido. Utiliza el método POST para asignar un curso al alumno.'}, status=405)


def alumnos_por_curso(request, id_curso):
    curso = get_object_or_404(Curso, id=id_curso)
    
    alumnos = Alumno.objects.filter(curso_id=id_curso)

    serialized_alumnos = []
    for alumno in alumnos:
        serialized_alumnos.append({
            'nombre': alumno.nombre,
            'apellido': alumno.apellido,
            'dni': alumno.dni,
            'telefono': alumno.telefono,
            'correo_electronico': alumno.correo_electronico,
        })

    return JsonResponse({'alumnos': serialized_alumnos})