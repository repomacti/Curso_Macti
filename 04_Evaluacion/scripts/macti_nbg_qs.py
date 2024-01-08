#
# Author: Luis Miguel de la Cruz Salas
# Last update: Sat Jan  6 11:43:10 PM UTC 2024
#
import os, sys, shutil
from colorama import Fore, Back, Style
import pandas as pd

def init_course_nbgrader(path, home, path_c_name_nbg):
    """
    Inicializa el directorio con NBGRADER y modifica la ruta 
    c.CourseDirectory.root dentro del archivo nbgrader_config.py 
    de acuerdo con la ruta del directorio del curso.
    """
    print(Fore.WHITE + Back.MAGENTA + '\n --> Inicializando el directorio para ' + Style.BRIGHT + 'NBGRADER \n' + Style.RESET_ALL)
    nbgrader_qs = 'nbgrader quickstart ' + path_c_name_nbg
    print('nbgrader quickstart ' + Style.NORMAL + Fore.GREEN + path_c_name_nbg + Style.RESET_ALL)

    # Inicializamos el curso para NBGRADER 
    os.system(nbgrader_qs)

    # Agregamos la ruta del curso para NBGRADER en el archivo de 
    # configuración nbgrader_config.py
    print(Fore.WHITE + Back.MAGENTA + ' --> Modificando el parámetro:' + Fore.RED + Back.RESET + ' c.CourseDirectory.root ' + Back.WHITE + Style.RESET_ALL + '\n')

    # Leemos el archivo nbgrader_config.py
    with open(path_c_name_nbg + "/nbgrader_config.py", "r") as f:
        all_file = f.readlines()

    # Textos a substituir
    old_text = "# c.CourseDirectory.root = ''"
    new_text = 'c.CourseDirectory.root = "' + path_c_name_nbg + '" \n' 

    # Escribimos el archivo nbgrader_config.py con el nuevo texto
    with open(path_c_name_nbg + "/nbgrader_config.py", "w") as f:
        for line in all_file:        
            if old_text in line:
                f.writelines(new_text)
            else:
                f.writelines(line)
                
    print(Fore.WHITE + Back.MAGENTA + ' --> Copiando el archivo modificado' + Fore.GREEN + Back.RESET + ' nbgrader_config.py ' + Fore.BLACK + 'a' + Fore.GREEN + Back.RESET + ' {} '.format(home) + Back.WHITE + Style.RESET_ALL + '\n')
    
    # Copiamos el archvio nbgrader_config.py al home
    shutil.copy2(path_c_name_nbg + "/nbgrader_config.py", home)

#-------- DEFINICION DE ALGUNAS RUTAS --------
# Este script se debe ejecutar desde donde está el directorio
# del curso original de donde se van a copiar los notebooks de quizzes

os.system('clear')

line_len = 40

print()
print(Fore.WHITE + Back.GREEN + line_len*'-')
print(Fore.WHITE + Back.GREEN + '   MACTI: Configuración con ' + Style.BRIGHT + 'NBGRADER    ')
print(Fore.WHITE + Back.GREEN +  line_len*'-')
print(Style.RESET_ALL)

# Path del home
home = os.environ['HOME'] + '/'

# Path desde donde se ejecuta el script
path = os.getcwd() + '/'

# Nombre del curso original
c_name = input(' Nombre del curso : ')

# Path absoluto al curso original
path_c_name = path + c_name

# Nombre del curso con extension _nbg
c_name_nbg = c_name + '_nbg'

# Path absoluto al curso con extension _nbg
path_c_name_nbg = path + c_name + '_nbg'

#-------- INICIALIZACIÓN DEL DIRECTORIO CON NBGRADER --------

if c_name_nbg not in os.listdir():
    # El directorio NO existe, se crea usando nbgrader quickstart ...
    continuar = input('\n Se configurará el siguiente directorio con NBGRADER: \n' + Fore.GREEN + ' {} '.format(path_c_name_nbg) + Style.RESET_ALL + '\n ¿continuar? Si [S], No [N] ' + Style.RESET_ALL)
    
    if continuar in ['S','s']:
        # Se inicializa el directorio con NBGRADER
        init_course_nbgrader(path, home, path_c_name_nbg)
    else:
        sys.exit(Fore.WHITE + Back.RED + '\n Termina el proceso anticipandamente.' + Style.RESET_ALL)
        
    # Lista de temas para el curso
    topic_list = pd.read_csv('assignments_creation.csv')
    
else:
    # El directorio YA existe, solo se copiarán los notebooks de los quizzes
    print(Fore.RED + '\n El directorio ' + 
          Fore.GREEN + '{}'.format(path_c_name_nbg) + 
          Fore.RED + ' ya se había inicializado previamente.' +
          Style.RESET_ALL + '\n')
    
    # Lista de temas para el curso
    topic_list = pd.read_csv('assignments_update.csv')

#-------- SE MUESTRAN LOS ARCHIVOS QUE SE VAN A COPIAR --------

print(' Los archivos se van a copiar del directorio \n' + Fore.WHITE + Back.GREEN + '{}'.format(path_c_name) + Fore.RESET + Back.RESET + '\n al directorio ')
print(Fore.WHITE + Back.GREEN + '{}'.format(path_c_name_nbg) + Fore.RESET + Back.RESET)

print(' Lista de archivos: \n')
for topic in topic_list:
    print(' > ' + topic)
    for a in topic_list[topic]:
        print('  -', a)

#-------- SE PREGUNTA SI TODO ESTÁ CORRECTO PARA CONTINUAR --------

seguro = input("\n ¿Continuar? Si [S], No [N] ")#.format(src_dir_path, c_name_nbg))

if seguro in ['S', 's']:
    pass
else:
    print()
    sys.exit(Fore.WHITE + Back.RED + ' Termina el proceso anticipandamente.' + Style.RESET_ALL)

#-------- SE COMIENZA LA COPIA DE ARCHIVOS --------

print(Fore.WHITE + Back.MAGENTA + ' --> Copiando información de' + Back.RESET + Fore.GREEN + ' {} '.format(c_name) + Style.RESET_ALL + 'a' + Fore.GREEN + ' {} '.format(c_name_nbg) + Style.RESET_ALL)
print()

# Se recorren los topicos/temas (que son las columnas del DataFrame topic_list)
for topic in topic_list:
    # Se construye el nombre en el directorio source. Se usa la ruta absoluta
    p = path_c_name_nbg + '/source/' + topic
    print(' Subdirectorio del tema:')
    if os.path.exists(p): 
        print(' ' + Fore.GREEN + '{}'.format(p) + Style.RESET_ALL + ' YA existe\n')
    else:
        print(' ' + Fore.GREEN + '{}'.format(p) + Style.RESET_ALL + ' NO existe\n')

        print(Fore.WHITE + Back.MAGENTA + ' ---> Creando el directorio :' + Fore.GREEN + Back.RESET + ' {} '.format(p) + Style.RESET_ALL + '\n')
        os.makedirs(p, exist_ok=True)        

    # Por cada topico se determina la lista de notebooks (quizzes) a copiar
    for a in topic_list[topic]:
        if not isinstance(a, float): # Es necesario por si hay nan
            src = path_c_name + '/' + topic + '/' + a
            dst = path_c_name_nbg + '/source/' + topic        
            print(' Fuente: {} \n Destino: {}\n'.format(src, dst))

            # Se copian los archivos
            shutil.copy2(src, dst)

