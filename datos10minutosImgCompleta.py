# -*- encoding: utf8
# Autores: Bellini Saibene Yanina;Banchero, Santiago

import argparse
import pyodbc
import traceback
import sys, os
try:
	from identify import Identify
except ImportError:
	raise ImportError,"Se requiere el modulo Identify: https://github.com/INTA-Radar/ImgCompuestas/blob/master/identify.py"	


parser = argparse.ArgumentParser(description="Calcula las variables del DataSet de entrenamiento y testeo para cada caso")

parser.add_argument("path_img", 
                    help="Ubicación de los archivos raster a procesar")
parser.add_argument ("fecha", help="Fecha a procesar, formato: aaaammdd")
parser.add_argument("archivo", default="db", choices=["db", "txt"],help="Donde almacenar los datos")

#TODO: agregarle argumentos para seleccionar que variable y que elevación y/o horario se quiere procesar.
'''parser.add_argument("-dBZ", action='store_true', help="Genera las variables relacionadas con dBZ")
parser.add_argument("-ZDR", action='store_true', help="Genera la imágen relacionadas con ZDR")
parser.add_argument("-KDP", action='store_true', help="Genera las variables relacionadas con KDP")
parser.add_argument("-RhoHV", action='store_true', help="Genera la imágen relacionadas con RhoHV")
parser.add_argument("-PhiDP", action='store_true', help="Genera la imágen relacionadas con PhiDP")
parser.add_argument("-E", action='store_true', help="Genera la imágen relacionadas con Energía Cinética")
parser.add_argument("-EW", action='store_true', help="Genera la imágen relacionadas con Energía Cinética (funcion de peso)")'''

args = parser.parse_args()

#Realizar la conexion al sql server
if args.archivo=='db':
	#TODO: Se debe manejar la conexión...solicitar los datos de alguna manera...o bien por parámetro o por teclado
	#Ejemplo de conexión a SQL Server con Autenticación Integrada
	#con = pyodbc.connect('Trusted_Connection=yes;DRIVER={SQL Server};SERVER=nombre del servidor;DATABASE=nombre de la base de datos')
	#Ejemplo de conexión a SQL Server con Autenticación de SQL Server
	con = pyodbc.connect('DRIVER={SQL Server};SERVER=nombre del servidor;DATABASE=ImplementacionGranizoRadar;UID=usuario;PWD=contraseña')
else:
	#TODO: Código para crear los archivos de texto para almacenar el procesamiento.
	file=args.fecha	

#Obtiene el Id del Evento a partir de la fecha
anio=args.fecha[0:4]
mes=args.fecha[4:6]
dia=args.fecha[6:8]

# Creo los objetos Identify con las imagenes a procesar

#---- Bloque de procesamiento de los datos de imagenes cada 10 minutos ---------#
#recorro todos los puntos

print 'Iniciando recuperación de datos de los lotes de campo.'

dbz = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find('dBZ') >0 and i.find('MAX') == -1 and i.find('MIN') == -1 and i.find('AVG') == -1 and i.find('TOT') == -1 and i.endswith('tif')]
zdr = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find('ZDR') >0 and i.find('MAX') == -1 and i.find('MIN') == -1 and i.find('AVG') == -1 and i.find('TOT') == -1 and i.endswith('tif')]
rho = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find('RhoHV') >0 and i.find('MAX') == -1 and i.find('MIN') == -1 and i.find('AVG') == -1 and i.find('TOT') == -1 and i.endswith('tif')]

#Este bloque es para recorrer el que tenga mayor cantidad y hacer un solo bucle.
cantidaddbz = len(dbz)
cantidadzdr	= len(zdr)
cantidadrho = len(rho)

if cantidadrho > cantidaddbz :
	if cantidadrho > cantidadzdr :
		cantidad = cantidadrho
	else:
		cantidad = cantidadzdr
else:
	if cantidaddbz > cantidadzdr:
		cantidad = cantidaddbz
	else:
		cantidad = cantidadzdr		

if cantidaddbz==1728: #Este valor sale de multiplicar 144 tomas de datos en un día * 12 elevaciones
	volcompletodbz=1
else:
	volcompletodbz=0
	
if cantidadrho==1728:
	volcompletorho=1
else:
	volcompletorho=0

if cantidadzdr==1728:
	volcompletozdr=1
else:
	volcompletozdr=0				

print 'cantidad dbz:', len(dbz)
print 'cantidad zdr:', len(zdr)
print 'cantidad rho:', len(rho)
print 'cantidad:', cantidad
#raw_input()

#recorro todos los puntos

print 'Iniciando obtención de datos para la fecha determinada.'

	# Bloque de obtención de los datos de cada imagen en cada elevacion y en cada horario

for i in xrange(cantidad):
	print "Intentando procesar archivo ", i, " de ", cantidad, "."
	#raw_input()
	
	try:
		img_tif_name=args.path_img+dbz[i]
		horariodbz = dbz[i][8:12]
		elevadbz = dbz[i][24:26]
		print "Elevacion: ", elevadbz
		#raw_input()
		imgdbz = file(img_tif_name)
		imgdbzd= Identify(img_tif_name)
	except IOError:
		imgdbz= None
		print "No se encuetra el archivo: "+img_tif_name
	except IndexError:
		print "El archivo para esa elevación y toma no se encuentra."
		imgdbz= None	
	
	try:
		img_tif_name=args.path_img+zdr[i]
		horariozdr = zdr[i][8:12]
		elevazdr = zdr[i][24:26]
		imgzdr = file(img_tif_name)
		imgzdrd= Identify(img_tif_name)
	except IOError:
		imgzdr= None
		print "No se encuetra el archivo: "+img_tif_name
	except IndexError:
		imgzdr= None	
	try:
		img_tif_name=args.path_img+rho[i]
		horariorho = rho[i][8:12]
		elevarho = rho[i][26:28]
		imgrho = file(img_tif_name)
		imgrhod= Identify(img_tif_name)		
	except IOError:
		imgrho= None
		print "No se encuetra el archivo: "+img_tif_name
	except IndexError:
		imgrho= None	

	
	# Recorrido de una matriz
	# De izquierda a derecha
	# De arriba hacia abajo
	for y in xrange(504): #Todas las imágenes tienen el mismo tamaño
		for x in xrange(486): #Todas las imágenes tienen el mismo tamaño
			print 'X:', x, 'Y:', y
			if imgdbz==None: 
				valordbz=-99
				elevadbz=-99
				horariodbz=-99
			else:	
				valordbz = imgdbzd.get_pixel_data(y,x)
			
			print 'X:', x, 'Y:', y
			if imgzdr==None: 
				valorzdr=-99
				elevazdr=-99
				horariozdr=-99
			else:	
				valorzdr = imgzdrd.get_pixel_value(y,x)
			
			print 'X:', x, 'Y:', y
			if imgrho==None: 
				valorrho=-99
				elevarho=-99
				horariorho=-99
			else:
				valorrho = imgrhod.get_pixel_value(y,x)
		
			#Obtenido los datos, almacenar en las tablas correspondientes
			
			instr= 'INSERT INTO datosdBZ([Fecha],[x],[y],[Elevacion],[Horario],[dBZ],[VolCompleto]) VALUES (?,?,?,?,?,?,?)'
     
			curins = con.cursor()
			curins.execute(instr, (args.fecha,x,y, elevadbz ,horariodbz, valordbz, volcompletodbz))
			curins.commit()
			
			instr= 'INSERT INTO datosZDR([Fecha],[x],[y],[Elevacion],[Horario],[ZDR],[VolCompleto]) VALUES (?,?,?,?,?,?,?)'
     
			curins = con.cursor()
			curins.execute(instr, (args.fecha,x,y, elevazdr ,horariozdr, valorzdr, volcompletozdr))
			curins.commit()
			
			instr= 'INSERT INTO datosRhoHV([Fecha],[x],[y],[Elevacion],[Horario],[RhoHV],[VolCompleto]) VALUES (?,?,?,?,?,?,?)'
     
			curins = con.cursor()
			curins.execute(instr, (args.fecha,x,y, elevarho ,horariorho, valorrho, volcompletorho))
			curins.commit()
			
# Cierro la conexión con la base de datos y los archivos
# Almacenar en archivos de texto

print "Almacenamiento finalizado"
con.close()


