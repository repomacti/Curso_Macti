import os, shutil

c_name = input('\n Nombre del curso : ')

paths = [c_name + '/Tema1/', 
         c_name + '/.ans/',
        ]

for p in paths:
    if not os.path.exists(p):
        print('Creando el directorio : {}'.format(p))
        os.makedirs(p , exist_ok=True)
    else:
        print('El directorio : {} ya existe'.format(p))

os.chdir(c_name)
os.system('git init')

lines = []
lines.append("# NBGRADER \n")
lines.append("nbg \n\n")
lines.append("# QUIZ \n")
lines.append("q*.ipynb \n")
lines.append(".ans/ \n")
    
with open(".gitignore", "w") as f:
    f.writelines(lines)

os.system('git status')
os.system('git add .')
os.system('git commit -m "Iniciando el repositorio"')

#for i in range(1,4):
#    filename = '/data/Plantillas/plantilla0' + str(i) + '.ipynb'
#    stream = pkg_resources.resource_stream('macti', filename)
#    print('Copiando {} al directorio {}'.format(stream.name.split(sep='/')[-1], paths[0]))
#    shutil.copy2(stream.name, paths[0])
