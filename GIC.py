#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Generar Imagen Compuesta Versión 3.0 - Abril 2014
#       
#       Copyright 2012 yabellini <yabellini@YABELLINI>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       
#		Este script es parte del set de software desarrollado por INTA
#		para el tratamiento de los datos de los radares meteorológicos.
#		
#		Esta versión 3.0 permite el cálculo de imágenes compuestas en
#		el rango de 240 km para las variables Z (dBZ), ZDR, PhiDP,
#		KDP y RhoHV.
#
#		Los argumentos son: 
#			path_img: "Ubicación de los archivos raster a procesar"
#			fecha: "Fecha a procesar, formato: aaaammdd"
#			extension: "Extensión de los archivos a procesar, para imágenes valor x defecto: tif"
#			variable: "Variable a procesar. Posibles valores dBZ, ZDR, RhoHV, KDP, PhiDP, E. Valor por defecto: dBZ"
#			-mto: "Calcula imágenes compuestas x cada paso de toma de datos (default: 10 minutos). Para todas las elevaciones."
#			-ele: "Número de elevación a procesar. Posibles valores: 0 (todas), 1 a 12."
#			-d: "Indica que no hace falta generar las imágenes horarias para la imágen compuesta de 24 horas y todas las elevaciones."
#			-maxi: "Genera la imágen compuesta con el valor máximo"
#			-mini: "Genera la imágen compuesta con el valor mínimo"
#			-prom: "Genera la imágen compuesta con el valor promedio"
#			-tot: "Genera la imágen compuesta con el valor total"
import sys, os
import argparse

try:
	from osgeo import gdal
	from osgeo import osr 
except ImportError:
	raise ImportError,"Se requiere el modulo osgeo.  Se puede descargar de http://www.lfd.uci.edu/~gohlke/pythonlibs/"

try:
	import numpy, numpy.ma as ma  
except ImportError:
	raise ImportError,"Se requiere el modulo numpy. http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy"

def save_imgcomp(imagen, archivo, datos, dtval):
	new_ds_ref = osr.SpatialReference() 
	new_ds_ref.ImportFromEPSG(4326)  
	driver = gdal.GetDriverByName("GTiff")
	ds = driver.Create(archivo, imagen.RasterXSize, imagen.RasterYSize, 1, gdal.GDT_Float64)
	ds.SetGeoTransform(imagen.GetGeoTransform()) 
	ds.SetProjection(new_ds_ref.ExportToWkt())
	outband=ds.GetRasterBand(1)
	outband.SetNoDataValue(dtval)
	outband.WriteArray(datos)
	ds = None 
	return
	
def gen_unaelevacion(imgs, args):
	#Se debe hacer el calculo para el día completo, asi que debo comparar todas las imágenes contenidas en imgs
	#Creo las variables necesarias para el calculo del promedio
	print 'Creo la matriz con 144 lugares, dentro de la función: gen_unaelevacion'
	A = ma.zeros((144,505,487))
	Tot = ma.zeros((144,505,487))
	# Abro el archivo correspondiente para la primera comparación
	imageninicio = gdal.Open(args.path_img+imgs[0])
	
	#Leo la banda 1 que es la única en este tipo de archivo
	bandaimagen = imageninicio.GetRasterBand(1)
	
	#Los paso a una matriz
	# Esto es la matriz NxM de datos de la imagen, acá están TODOS los 
	# valores de pixeles de la imagen
	if args.maxi:
		#print 'Abro para datos maximos'
		datosmaximos = bandaimagen.ReadAsArray(0, 0, imageninicio.RasterXSize, imageninicio.RasterYSize)
	if args.mini:
		#print 'Abro para datos minimos'
		datosminimos = bandaimagen.ReadAsArray(0, 0, imageninicio.RasterXSize, imageninicio.RasterYSize)
		datosminimos[datosminimos==-99]=9999
		print datosminimos
	if args.tot:
		#print 'Abro para total'
		datostot = bandaimagen.ReadAsArray(0, 0, imageninicio.RasterXSize, imageninicio.RasterYSize)
		datostot[datostot==-99]=0
		print datostot	
	i=0
	for img in imgs:
			print 'Valor del indice de A:',i
			print args.path_img+img
			# Abro el archivo correspondiente
			imagen = gdal.Open(args.path_img+img)
			#Leo la banda 1 que es la única en este tipo de archivo
			bandaimagen = imagen.GetRasterBand(1)
			datos = bandaimagen.ReadAsArray(0, 0, imagen.RasterXSize, imagen.RasterYSize)
			if args.prom:
				print 'Meto los datos en A[',i,']'
				A[i]= datos
			if args.tot:
				print 'Meto los datos en Tot[',i,']'
				Tot[i]= datos
			if args.maxi:
				#print 'Comparo para datos maximos'
				datosmaximos = numpy.fmax(datosmaximos, datos)
			if args.mini:
				#print 'Comparo para datos minimos'
				datosm=datos
				datosm[datosm==-99]=9999
				datosminimos = numpy.fmin(datosminimos, datosm)
				print datosminimos
			i=i+1
	#Finalizada la comparación grabo el archivo final
	if args.prom:
		print 'Genero la matriz B, con los valores válidos para el promedio'
		A= ma.masked_values(A, -99.0)
		B=numpy.mean(A, axis=0)
		archivo= args.path_img+args.fecha+'AVG'+args.variable+elevacion+'.tif'
		save_imgcomp(imagen, archivo, B, -99)
	if args.tot:
		B=numpy.sum(Tot, axis=0)
		archivo= args.path_img+args.fecha+'TOT'+args.variable+elevacion+'.tif'
		save_imgcomp(imagen, archivo, B, -99)	
	if args.maxi:
		archivo= args.path_img+args.fecha+'MAX'+args.variable+elevacion+'.tif'
		save_imgcomp(imagen, archivo, datosmaximos, -99)
	if args.mini:
		archivo= args.path_img+args.fecha+'MIN'+args.variable+elevacion+'.tif'
		save_imgcomp(imagen, archivo, datosminimos, 9999)
	return 

def gen_horaria(imgs, args):
	#Cada resumen se debe generar de cada paso horario.  Asi que mientras sea la misma hora hago los calculos...
	#Inicializo las variables previas al bucle
	hora = imgs[0][8:12]

	# Abro el archivo correspondiente
	imageninicio = gdal.Open(args.path_img+imgs[0])

	#Leo la banda 1 que es la única en este tipo de archivo
	bandaimagen = imageninicio.GetRasterBand(1)
	
	#Los paso a una matriz
	# Esto es la matriz NxM de datos de la imagen, acá están TODOS los 
	# valores de pixeles de la imagen
	if args.maxi:
		#print 'Abro para datos maximos'
		datosmaximos = bandaimagen.ReadAsArray(0, 0, imageninicio.RasterXSize, imageninicio.RasterYSize)
	if args.mini:
		#print 'Abro para datos minimos'
		datosminimos = bandaimagen.ReadAsArray(0, 0, imageninicio.RasterXSize, imageninicio.RasterYSize)
		datosminimos[datosminimos==-99]=9999
	if args.tot:
		datostot = bandaimagen.ReadAsArray(0, 0, imageninicio.RasterXSize, imageninicio.RasterYSize)
		datostot[datosminimos==-99]=0
	i=0
	j=0
	#Creo las variables necesarias para el calculo del promedio
	print 'Creo A con 12 lugares, dentro de la funcion gen_horaria, ind = 0'
	ind=0
	A = ma.zeros((12,505,487))
	Tot = ma.zeros((12,505,487))
	#print 'Inicio procesamiento volúmenes '+args.variable+'...'
	for img in imgs: 
		print 'Valor del indice de A:',ind
		if hora==img[8:12]:
			# Abro el archivo correspondiente
			imagen = gdal.Open(args.path_img+img)
			#Leo la banda 1 que es la única en este tipo de archivo
			bandaimagen = imagen.GetRasterBand(1)
			datos = bandaimagen.ReadAsArray(0, 0, imagen.RasterXSize, imagen.RasterYSize)
			if args.prom:
				#print 'Compararo para promedio'
				A[ind]= datos
			if args.tot:
				Tot[ind]= datos	
			if args.maxi:
				#print 'Comparo para datos maximos'
				datosmaximos = numpy.fmax(datosmaximos, datos)
			if args.mini:
				#print 'Comparo para datos minimos'
				datosm=datos
				datosm[datosm==-99]=9999 #Agregado
				datosminimos = numpy.fmin(datosminimos, datosm)
				print datosminimos
			j=j+1
			ind=ind+1
			#print 'Procesando volumen número= ',j, ' correspondiente al archivo ', args.path_img+img, ' y a la hora ', hora 
		else:
			#Finalizada la comparación grabo el archivo final
			if args.maxi:
				#print 'Grabo para datos maximos'
				archivo= args.path_img+args.fecha+hora+'MAX'+args.variable+'.tif'
				save_imgcomp(imagen, archivo, datosmaximos, -99)
			if args.mini:
				#print 'Grabo para datos minimos'
				archivo= args.path_img+args.fecha+hora+'MIN'+args.variable+'.tif'
				save_imgcomp(imagen, archivo, datosminimos, 9999)
			if args.prom:	
				#print 'Grabo para promedio'
				archivo= args.path_img+args.fecha+hora+'AVG'+args.variable+'.tif'
				A= ma.masked_values(A, -99.0)
				B=numpy.mean(A, axis=0)
				save_imgcomp(imagen, archivo, B, -99)
			if args.tot:
				archivo= args.path_img+args.fecha+hora+'TOT'+args.variable+'.tif'	
				B=numpy.sum(Tot, axis=0)
				save_imgcomp(imagen, archivo, B, -99)
			i=i+1
			#print 'Almacenando imágen número ',i
			hora = img[8:12]
			imagen = B = ind = 0
			bandaimagen= 0
			datosmaximos=-99
			datosminimos=9999
			datostot=0
			datosm=0
			datos = 0
			A= ma.zeros((12,505,487))
			Tot=ma.zeros((12,505,487))
	#Guardo la ultima imágen, cuando sale del for.

	if args.prom:	
		#print 'Grabo para promedio, ultima imagen'
		archivo= args.path_img+args.fecha+hora+'AVG'+args.variable+'.tif'
		A= ma.masked_values(A, -99.0)
		B=numpy.mean(A, axis=0)
		save_imgcomp(imagen, archivo, B, -99)
	if args.maxi:
		#print 'Grabo para datos maximos, ultima imagen.'
		archivo= args.path_img+args.fecha+hora+'MAX'+args.variable+'.tif'
		save_imgcomp(imagen, archivo, datosmaximos, -99)
	if args.mini:
		#print 'Grabo para datos minimos, ultima imagen'
		archivo= args.path_img+args.fecha+hora+'MIN'+args.variable+'.tif'
		save_imgcomp(imagen, archivo, datosminimos, 9999)
	if args.tot:
		archivo= args.path_img+args.fecha+hora+'TOT'+args.variable+'.tif'	
		B=numpy.sum(Tot, axis=0)
		save_imgcomp(imagen, archivo, B, -99)
	i=i+1
	#print 'Almacenando imágen número ',i
	#print 'Cantidad de imágenes procesadas: ', j
	#print 'Cantidad de imágenes generadas: ', i
	j=i=ind=0
	datosmaximos=-99
	datosminimos=9999
	datostot=0
	datosm=0
	A = ma.zeros((12,505,487))
	Tot=ma.zeros((12,505,487))
	B=0
	return
 
 
parser = argparse.ArgumentParser(description="Calcula imágenes compuesta con datos del RADAR Meteorológico")

parser.add_argument("path_img", 
                    help="Ubicación de los archivos raster a procesar")
parser.add_argument ("fecha", help="Fecha a procesar, formato: aaaammdd")
parser.add_argument ("extension", default="tif", help="Extensión de los archivos a procesar, para imágenes valor x defecto: tif")
parser.add_argument("variable", default="dBZ", choices=["dBZ", "ZDR", "KDP","RhoHV", "PhiDP","E","EW"],help="Variable a procesar. Posibles valores dBZ, ZDR, RhoHV, KDP, PhiDP. Valor por defecto: dBZ")

group = parser.add_mutually_exclusive_group()
group.add_argument("-mto", action="store_true", help="Calcula imágenes compuestas x cada paso de toma de datos (default: 10 minutos). Para todas las elevaciones.")
parser.add_argument("-ele", type=int, default=0, choices=[1,2,3,4,5,6,7,8,9,10,11,12],help="Número de elevación a procesar. Posibles valores: 0 (todas), 1 a 12.")
group.add_argument("-d", action="store_true", help="Indica que no hace falta generar las imágenes horarias para la imágen compuesta de 24 horas y todas las elevaciones.")

parser.add_argument("-maxi", action='store_true', help="Genera la imágen compuesta con el valor máximo")
parser.add_argument("-mini", action='store_true', help="Genera la imágen compuesta con el valor mínimo")
parser.add_argument("-prom", action='store_true', help="Genera la imágen compuesta con el valor promedio")
parser.add_argument("-tot", action='store_true', help="Genera la imágen compuesta con el valor promedio")

args = parser.parse_args()


# Si la opción es generar x minuto no puede seleccionar la elevación (porque las imágenes se crean con otro script)
if args.mto:
	elevacion = ""
else:
	#Las imágenes a generar son compuestas de 24 horas.  Puede ser de todas o de una elevación específica.
	#Genero la elevación correspondiente
	if args.ele == 0:
		elevacion = "x12elevaciones"
	if args.ele == 1:
		elevacion = ".vol_1."
	if args.ele == 2:
		elevacion = ".vol_3."
	if args.ele == 3:
		elevacion = ".vol_5."
	if args.ele == 4:
		elevacion = ".vol_7."
	if args.ele == 5:
		elevacion = ".vol_9."
	if args.ele == 6:
		elevacion = ".vol_11."
	if args.ele == 7:
		elevacion = ".vol_13."
	if args.ele == 8:
		elevacion = ".vol_15."
	if args.ele == 9:
		elevacion = ".vol_17."
	if args.ele == 10:
		elevacion = ".vol_19."
	if args.ele == 11:
		elevacion = ".vol_21."
	if args.ele == 12:
		elevacion = ".vol_23."

# Armo una lista con todos los nombres de las imagenes que están en el directorio "path_img" que cumplen con los parámetros 
#Se filtra con la fecha, la extensión, la elevación y el tipo de variable. Todos son parámetros del programa.

#Defino el tipo de imágen compuesta a generar.

if args.mto:
	#Es por paso de cada minuto (son todas las elevaciones)
	#print 'Es por paso de cada minuto (son todas las elevaciones)'
	if args.ele==0:
		#Aca necesita un try por si el dato del directorio es incorrecto
		imgs = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find(args.variable) >0 and i.find('MAX') == -1 and i.find('MIN') == -1 and i.find('AVG') == -1 and i.endswith(args.extension)]
		try:
			gen_horaria(imgs, args)
		except IndexError:
			raise IndexError,"No hay archivos para los parámetros indicados."
			
else:
	#Es de 24 horas
	#print 'Es de 24 horas'
	if args.ele == 0:
		#print 'Son todas las elevaciones'
		#Son todas las elevaciones
		#Como es necesario contar con las imágenes de resumen de cada hora
		#primero ejecuto gen_horaria, a menos que el usuario haya indicado lo contrario
		if args.d:
			#Aca necesita un try por si el dato del directorio es incorrecto
			imgs = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find(args.variable) >0 and i.find('MAX') == -1 and i.find('MIN') == -1 and i.find('AVG') == -1 and i.endswith(args.extension)]
			try:
				gen_horaria(imgs,args)
			except IndexError:
				raise IndexError,"No hay archivos para los parámetros indicados."	
		#luego ejecuto el resumen del día
		imgsmax = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find('MAX'+args.variable) >0 and i.find('vol') == -1 and i.find('elevaciones') == -1 and i.endswith(args.extension)]	
		imgsmin = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find('MIN'+args.variable) >0 and i.find('vol') == -1 and i.find('elevaciones') == -1 and i.endswith(args.extension)]	
		imgsprom = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find('AVG'+args.variable) >0 and i.find('vol') == -1 and i.find('elevaciones') == -1 and i.endswith(args.extension)]	
		imgstot = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find('TOT'+args.variable) >0 and i.find('vol') == -1 and i.find('elevaciones') == -1 and i.endswith(args.extension)]	
		if args.mini:
			try:
				gen_unaelevacion(imgsmin, args)
			except IndexError:
				raise IndexError,"No hay archivos para los parámetros indicados."	
		if args.maxi:
			try:
				gen_unaelevacion(imgsmax,args)
			except IndexError:
				raise IndexError,"No hay archivos para los parámetros indicados."
		if args.prom:
			try:
				gen_unaelevacion(imgsprom,args)
			except IndexError:
				raise IndexError,"No hay archivos para los parámetros indicados."		
		if args.tot:
			try:
				gen_unaelevacion(imgstot,args)
			except IndexError:
				raise IndexError,"No hay archivos para los parámetros indicados."		

	else:
		#print 'Es una elevación en particular:', elevacion
		#Es una elevación en particular
		#Aca necesita un try por si el dato del directorio es incorrecto
		imgs = [i for i in os.listdir(args.path_img) if i.startswith(args.fecha.replace('-','')) and i.find(args.variable) >0 and i.find(elevacion) >0 and i.find('MAX') == -1 and i.find('MIN') == -1 and i.find('AVG') == -1 and i.endswith(args.extension)]
		print imgs
		try:
			gen_unaelevacion(imgs, args)
		except IndexError:
			raise IndexError,"No hay archivos para los parámetros indicados."	
