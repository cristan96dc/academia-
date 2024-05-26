from myapp.models import Cursos, Temario

# Crear o obtener el curso "Diseño de Interfaz de Usuario (UI) con Figma"
curso10, created = Cursos.objects.get_or_create(nombre='Diseño de Interfaz de Usuario (UI) con Figma')
if created:
    print("Curso 'Diseño de Interfaz de Usuario (UI) con Figma' creado.")
else:
    print("El curso 'Diseño de Interfaz de Usuario (UI) con Figma)' ya existe.")

# Iterar sobre las clases y descripciones
for i in range(1, 4):
    if i == 1:
        titulo = f"Clase {i}: Introducción a Figma"
        descripcion = "Exploraremos los conceptos básicos y la interfaz de Figma, incluyendo cómo crear proyectos y colaborar en tiempo real."
    elif i == 2:
        titulo = f"Clase {i}: Diseño de Interfaz de Usuario"
        descripcion = "Aprenderás técnicas de diseño de interfaz de usuario, incluyendo uso de componentes, estilos y prototipado en Figma."
    elif i == 3:
        titulo = f"Clase {i}: Prototipado Avanzado y Animaciones"
        descripcion = "Exploraremos cómo crear prototipos avanzados y añadir animaciones interactivas en Figma para mejorar la experiencia del usuario."

    # Crear un objeto Temario y vincularlo al curso10
    Temario.objects.create(curso=curso10, titulo=titulo, descripcion=descripcion)

print("Clases creadas exitosamente.")