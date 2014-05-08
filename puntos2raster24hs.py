# -*- encoding: utf8
# Autores: Bellini Saibene Yanina;Banchero, Santiago

import argparse
import pyodbc
import traceback
try:
	from identify import Identify
except ImportError:
	raise ImportError,"Se requiere el modulo Identify: https://github.com/INTA-Radar/ImgCompuestas/blob/master/identify.py"	
try:
	import numpy 
except ImportError:
	raise ImportError,"Se requiere el modulo numpy. http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy"
	


parser = argparse.ArgumentParser(description="Calcula las variables del DataSet de entrenamiento y testeo para cada caso")

parser.add_argument("path_img", 
                    help="Ubicación de los archivos raster a procesar")
parser.add_argument ("fecha", help="Fecha a procesar, formato: aaaammdd")
parser.add_argument("-dBZ", action='store_true', help="Genera las variables relacionadas con dBZ")
parser.add_argument("-ZDR", action='store_true', help="Genera la imágen relacionadas con ZDR")
parser.add_argument("-KDP", action='store_true', help="Genera las variables relacionadas con KDP")
parser.add_argument("-RhoHV", action='store_true', help="Genera la imágen relacionadas con RhoHV")
parser.add_argument("-PhiDP", action='store_true', help="Genera la imágen relacionadas con PhiDP")

args = parser.parse_args()

#Todo: que la conexion y la base de datos sean parámetros
#Realizar la conexion al sql server
con = pyodbc.connect('DRIVER={SQL Server};SERVER=USUARIO-PC\SQLEXPRESS2008R2;DATABASE=NombreBD;UID=usuario;PWD=contraseña')
conins = pyodbc.connect('DRIVER={SQL Server};SERVER=USUARIO-PC\SQLEXPRESS2008R2;DATABASE=NombreBD;UID=usuario;PWD=contraseña')
#Obtiene el Id del Evento a partir de la fecha
anio=args.fecha[0:4]
mes=args.fecha[4:6]
dia=args.fecha[6:8]
querystring = "SELECT IdEvento FROM Eventos where year(FechaEvento)="+anio+" and MONTH(FechaEvento)=" +mes+ " and DAY(FechaEvento)="+dia
cur = con.cursor()
res=cur.execute(querystring)
for r in res:
	evento = r
	
# Obtiene todos los puntos de lotes de campo 
querystring = "select latitud, longitud, granizo, danio, porcentajedanio, idevento, IdLocXEvento from LocalizacionxEvento where IdEvento="+str(evento[0])+" and Observacion not like '%Fuera del area de cobertura%'"
# and Observacion like '%Sin procesar%'
print str(evento[0]) 
# respuesta del query que trae todos los puntos
resp = cur.execute(querystring)

# Creo los objetos Identify con las imagenes a procesar
	
# Bloque de imagenes de Primera Elevación: en el nombre dice .vol_1.
# Bloque de imágenes de Todas las Elevaciones, el prefijo TE en las variables significa Todas las Elevaciones. 

f = 25 # Numero de filas: 12 elevaciones máximo, 12 elevaciones mínimo, total 24 hs máximo, total 24 horas mínimo
c = 2 # Numero de columnas
fm = [1,3,5,7,9,11,13,15,17,19,21,23] #Número de filas de valores máximos o mínimos (1 por cada elevación)
	
if args.dBZ:
	
	#Bloque de imágenes que tiene que ver con la variable dBZ
	print 'Procesando datos dBZ'
	dBZv=[range(c) for i in range(f)]
	
	for i in xrange(f-2):
		# Las filas de 1 a 12 tienen los valores máximos de cada elevación
		if i < 12:
			try:
				img_tif_name=args.path_img+args.fecha+"MAXdBZ.vol_"+str(fm[i])+"..tif"
				img = file(img_tif_name)
				dBZv[i][0]= Identify(img_tif_name)
				dBZv[i][1]= img_tif_name
			except IOError:
				dBZv[i][0]= None
				dBZv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
		# Las filas de 13 a 24 tienen los valores mínimos de cada elevación
		if i>10:
			try:
				img_tif_name=args.path_img+args.fecha+"MINdBZ.vol_"+str(fm[i-11])+"..tif"
				img = file(img_tif_name)
				dBZv[i][0]= Identify(img_tif_name)
				dBZv[i][1]= img_tif_name
			except IOError:
				dBZv[i][0]= None
				dBZv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
	try:
		img_tif_name=args.path_img+args.fecha+"MAXdBZx12elevaciones.tif"
		img = file(img_tif_name)
		dBZv[23][0]= Identify(img_tif_name)
		dBZv[23][1]= img_tif_name
	except IOError:
		dBZv[23][0]= None
		dBZv[23][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name
	try:
		img_tif_name=args.path_img+args.fecha+"MINdBZx12elevaciones.tif"
		img = file(img_tif_name)
		dBZv[24][0]= Identify(img_tif_name)
		dBZv[24][1]= img_tif_name
	except IOError:
		dBZv[24][0]= None
		dBZv[24][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name	
else:
	dBZv=[range(c) for i in range(f)]
	dBZv=None
	
if args.ZDR:
	#Bloque de imágenes que tiene que ver con la variable ZDR
	print 'Procesando datos ZDR'
	ZDRv=[range(c) for i in range(f)]
	for i in xrange(f-2):
		# Las filas de 1 a 12 tienen los valores máximos de cada elevación
		if i < 12:
			try:
				img_tif_name=args.path_img+args.fecha+"MAXZDR.vol_"+str(fm[i])+"..tif"
				img = file(img_tif_name)
				ZDRv[i][0]= Identify(img_tif_name)
				ZDRv[i][1]= img_tif_name
			except IOError:
				ZDRv[i][0]= None
				ZDRv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
		# Las filas de 13 a 24 tienen los valores mínimos de cada elevación
		if i>10:
			try:
				img_tif_name=args.path_img+args.fecha+"MINZDR.vol_"+str(fm[i-11])+"..tif"
				img = file(img_tif_name)
				ZDRv[i][0]= Identify(img_tif_name)
				ZDRv[i][1]= img_tif_name
			except IOError:
				ZDRv[i][0]= None
				ZDRv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
	try:
		img_tif_name=args.path_img+args.fecha+"MAXZDRx12elevaciones.tif"
		img = file(img_tif_name)
		ZDRv[23][0]= Identify(img_tif_name)
		ZDRv[23][1]= img_tif_name
	except IOError:
		ZDRv[23][0]= None
		ZDRv[23][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name
	try:
		img_tif_name=args.path_img+args.fecha+"MINZDRx12elevaciones.tif"
		img = file(img_tif_name)
		ZDRv[24][0]= Identify(img_tif_name)
		ZDRv[24][1]= img_tif_name
	except IOError:
		ZDRv[24][0]= None
		ZDRv[24][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name	
else:
	ZDRv=[range(c) for i in range(f)]
	ZDRv=None

if args.RhoHV:
	#Bloque de imágenes que tiene que ver con la variable RhoHV
	print 'Procesando datos RhoHV'
	RhoHVv=[range(c) for i in range(f)]
	for i in xrange(f-2):
		# Las filas de 1 a 12 tienen los valores máximos de cada elevación
		if i < 12:
			try:
				img_tif_name=args.path_img+args.fecha+"MAXRhoHV.vol_"+str(fm[i])+"..tif"
				img = file(img_tif_name)
				RhoHVv[i][0]= Identify(img_tif_name)
				RhoHVv[i][1]= img_tif_name
			except IOError:
				RhoHVv[i][0]= None
				RhoHVv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
		# Las filas de 13 a 24 tienen los valores mínimos de cada elevación
		if i>10:
			try:
				img_tif_name=args.path_img+args.fecha+"MINRhoHV.vol_"+str(fm[i-11])+"..tif"
				img = file(img_tif_name)
				RhoHVv[i][0]= Identify(img_tif_name)
				RhoHVv[i][1]= img_tif_name
			except IOError:
				RhoHVv[i][0]= None
				RhoHVv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
	try:
		img_tif_name=args.path_img+args.fecha+"MAXRhoHVx12elevaciones.tif"
		img = file(img_tif_name)
		RhoHVv[23][0]= Identify(img_tif_name)
		RhoHVv[23][1]= img_tif_name
	except IOError:
		RhoHVv[23][0]= None
		RhoHVv[23][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name
	try:
		img_tif_name=args.path_img+args.fecha+"MINRhoHVx12elevaciones.tif"
		img = file(img_tif_name)
		RhoHVv[24][0]= Identify(img_tif_name)
		RhoHVv[24][1]= img_tif_name
	except IOError:
		RhoHVv[24][0]= None
		RhoHVv[24][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name	
else:
	RhoHVv=[range(c) for i in range(f)]
	RhoHVv=None

if args.PhiDP:
	#Bloque de imágenes que tiene que ver con la variable RhoHV
	PhiDPv=[range(c) for i in range(f)]
	print 'Procesando datos PhiDP'
	for i in xrange(f-2):
		# Las filas de 1 a 12 tienen los valores máximos de cada elevación
		if i < 12:
			try:
				img_tif_name=args.path_img+args.fecha+"MAXPhiDP.vol_"+str(fm[i])+"..tif"
				img = file(img_tif_name)
				PhiDPv[i][0]= Identify(img_tif_name)
				PhiDPv[i][1]= img_tif_name
			except IOError:
				PhiDPv[i][0]= None
				PhiDPv[i][1]= img_tif_name
				print "No se encuentra el archivo: "+img_tif_name
				raw_input()
		# Las filas de 13 a 24 tienen los valores mínimos de cada elevación
		if i>10:
			try:
				img_tif_name=args.path_img+args.fecha+"MINPhiDP.vol_"+str(fm[i-11])+"..tif"
				img = file(img_tif_name)
				PhiDPv[i][0]= Identify(img_tif_name)
				PhiDPv[i][1]= img_tif_name
			except IOError:
				PhiDPv[i][0]= None
				PhiDPv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
	try:
		img_tif_name=args.path_img+args.fecha+"MAXPhiDPx12elevaciones.tif"
		img = file(img_tif_name)
		PhiDPv[23][0]= Identify(img_tif_name)
		PhiDPv[23][1]= img_tif_name
	except IOError:
		PhiDPv[23][0]= None
		PhiDPv[23][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name
	try:
		img_tif_name=args.path_img+args.fecha+"MINPhiDPx12elevaciones.tif"
		img = file(img_tif_name)
		PhiDPv[24][0]= Identify(img_tif_name)
		PhiDPv[24][1]= img_tif_name
	except IOError:
		PhiDPv[24][0]= None
		PhiDPv[24][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name	
else:
	PhiDPv=[range(c) for i in range(f)]
	PhiDPv=None
	
if args.KDP:
	#Bloque de imágenes que tiene que ver con la variable RhoHV
	print 'Procesando datos KDP'
	KDPv=[range(c) for i in range(f)]
	for i in xrange(f-2):
		# Las filas de 1 a 12 tienen los valores máximos de cada elevación
		if i < 12:
			try:
				img_tif_name=args.path_img+args.fecha+"MAXKDP.vol_"+str(fm[i])+"..tif"
				img = file(img_tif_name)
				KDPv[i][0]= Identify(img_tif_name)
				KDPv[i][1]= img_tif_name
			except IOError:
				KDPv[i][0]= None
				KDPv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
		# Las filas de 13 a 24 tienen los valores mínimos de cada elevación
		if i>10:
			try:
				img_tif_name=args.path_img+args.fecha+"MINKDP.vol_"+str(fm[i-11])+"..tif"
				img = file(img_tif_name)
				KDPv[i][0]= Identify(img_tif_name)
				KDPv[i][1]= img_tif_name
			except IOError:
				KDPv[i][0]= None
				KDPv[i][1]= img_tif_name
				print "No se encuetra el archivo: "+img_tif_name
				raw_input()
	try:
		img_tif_name=args.path_img+args.fecha+"MAXKDPx12elevaciones.tif"
		img = file(img_tif_name)
		KDPv[23][0]= Identify(img_tif_name)
		KDPv[23][1]= img_tif_name
	except IOError:
		KDPv[23][0]= None
		KDPv[23][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name
	try:
		img_tif_name=args.path_img+args.fecha+"MINKDPx12elevaciones.tif"
		img = file(img_tif_name)
		KDPv[24][0]= Identify(img_tif_name)
		KDPv[24][1]= img_tif_name
	except IOError:
		KDPv[24][0]= None
		KDPv[24][1]= img_tif_name
		print "No se encuetra el archivo: "+img_tif_name	
else:
	KDPv=[range(c) for i in range(f)]
	KDPv= None
#---- Bloque de procesamiento de los datos de imagenes compuestas: 24 hs ---------#
#recorro todos los puntos

print 'Iniciando recuperación de datos de los lotes de campo.'
for r in resp:
	
	# leo un registro
	lat,lon,granizo,danio,pordanio,idevento,idlocxevento = r
	print "Registro:", r
	dbz0 = 0
	dbz45 = 0
	dbz55 = 0
	dbz60 = 0	
	dbz45b = False
	dbz55b = False
	dbz60b = False
	pxdBZ=[range(c) for i in range(f)]
	pxZDR=[range(c) for i in range(f)]
	pxPhi=[range(c) for i in range(f)]
	pxRho=[range(c) for i in range(f)]
	pxKDP=[range(c) for i in range(f)]
	
	for i in xrange(f-2):
		try:
			#al obj identify le pide el valor de pixel a partir del x y
			pxdBZ[i] = dBZv[i][0].get_pixel_value(lon,lat)
			if np.isnan(pxdBZ[i]):
				pxdBZ[i] = None
		except :
			pxdBZ[i] = None
	
		try :
			#al obj identify le pide el valor de pixel a partir del x y	
			pxZDR[i] = ZDRv[i][0].get_pixel_value(lon,lat)
			if np.isnan(pxZDR[i]):
				pxZDR[i] = None
		except :
			pxZDR[i] = None
			
		try:
			#al obj identify le pide el valor de pixel a partir del x y
			pxRho[i] = RhoHVv[i][0].get_pixel_value(lon,lat)
			if np.isnan(pxRho[i]):
				pxRho[i] = None
		except :
			pxRho[i] = None	
		
		try:
			#al obj identify le pide el valor de pixel a partir del x y
			pxPhi[i] = PhiDPv[i][0].get_pixel_value(lon,lat)
			if np.isnan(pxPhi[i]):
				pxPhi[i] = None
		except :
			pxPhi[i] = None	
		
		try:
			#al obj identify le pide el valor de pixel a partir del x y
			pxKDP[i] = KDPv[i][0].get_pixel_value(lon,lat)
			if np.isnan(pxKDP[i]):
				pxKDP[i] = None
		except :
			pxKDP[i] = None	
						
		
		
		if i < 12:
			if pxdBZ[i] > 0:
				dbz0= dbz0 + 1
			if pxdBZ[i] > 44:
				if i == 0:
					dbz45b = True
				dbz45 = dbz45 + 1
		
			if pxdBZ[i] > 54:
				if i == 0:
					dbz55b = True
				dbz55 = dbz55 + 1
			
			if pxdBZ[i] >= 59:
				if i == 0:
					dbz60b = True
				dbz60 = dbz60 + 1

	#Bloque de imágenes de Todas las elevaciones, el sufijo TE en las variables indica Todas las Elevaciones.
	try:
		pxdBZ[23] = dBZv[23][0].get_pixel_value(lon,lat)
		pxdBZ[24] = dBZv[24][0].get_pixel_value(lon,lat)
		if np.isnan(pxdBZ[23]):
			pxdBZ[23] = None
		if np.isnan(pxdBZ[24]):		
			pxdBZ[24] = None
	except:
		print 'Error dBZ' 
		pxdBZ[23] = None 
		pxdBZ[24] = None 
	
	try:
		pxZDR[23] = ZDRv[23][0].get_pixel_value(lon,lat)
		pxZDR[24] = ZDRv[24][0].get_pixel_value(lon,lat)
		if np.isnan(pxZDR[23]):
			pxZDR[23] = None
		if np.isnan(pxZDR[24]):		
			pxZDR[24] = None
		
	except:
		print 'Error ZDR'
		pxZDR[23] = None	
		pxZDR[24] = None
	
	try:
		pxRho[23] = RhoHVv[23][0].get_pixel_value(lon,lat)
		pxRho[24] = RhoHVv[24][0].get_pixel_value(lon,lat)
		if np.isnan(pxRho[23]):
			pxRho[23] = None
		if np.isnan(pxRho[24]):		
			pxRho[24] = None

	except:
		print 'Error RhoHV'
		pxRho[23] = None	
		pxRho[24] = None
	
	try:
		pxPhi[23] = PhiDPv[23][0].get_pixel_value(lon,lat)
		pxPhi[24] = PhiDPv[24][0].get_pixel_value(lon,lat)
		if np.isnan(pxPhi[23]):
			pxPhi[23] = None
		if np.isnan(pxPhi[24]):		
			pxPhi[24] = None

	except:
		print 'Error PhiDP'
		pxPhi[23] = None	
		pxPhi[24] = None
	
	try:
		pxKDP[23] = KDPv[23][0].get_pixel_value(lon,lat)
		pxKDP[24] = KDPv[24][0].get_pixel_value(lon,lat)
		if np.isnan(pxKDP[23]):
			pxKDP[23] = None
		if np.isnan(pxKDP[24]):		
			pxKDP[24] = None

	except:
		print 'Error KDP'
		pxKDP[23] = None	
		pxKDP[24] = None
			
	dbz45TE = False
	dbz55TE = False
	dbz60TE = False
	
	if pxdBZ[23] > 44:
		dbz45TE = True
	if pxdBZ[23] > 54:
		dbz55TE = True
	if pxdBZ[23] > 59:
		dbz60TE = True

	
	print 'Obtención de datos finalizada'
	
	print 'Primera elevacion: DBZ:',pxdBZ[0],pxdBZ[12],' 40:',dbz45b,' 60:',dbz60b,' 55: ', dbz55b, ' ZDR:',pxZDR[0],pxZDR[12],' KDP:',pxKDP[0],pxKDP[12],' Phi:', pxPhi[0],pxPhi[12], ' Rho:', pxRho[0],pxRho[12], lon,lat,granizo,danio, pordanio, idevento,idlocxevento
	print 'Totales: dBZ:',pxdBZ[23],pxdBZ[24],' ZDR:',pxZDR[23],pxZDR[24],' KDP:',pxKDP[23],pxKDP[24],' Phi:', pxPhi[23],pxPhi[24], ' Rho:', pxRho[23],pxRho[24]  
	print 'Iniciando almacenamiento de datos en base de datos'
	#print 'DBZ:',pxdBZ[23],pxdBZ[24],' 40:',dbz45TE,' 60:',dbz60TE #,' ZDR:',pxZDRTE,' KDP:',pxKDPTE,' Phi:', pxPhiTE, ' Rho:', pxRhoTE, lon,lat,granizo,idevento,idlocxevento 

	# Actualizo la tabla de 24 horas con todos los datos calculados
	instr1= 'INSERT INTO DatosRadarProcesados24horas ([IdLocXEvento],[IdEvento],[Latitud],[Longitud],[Granizo],[Porcentaje],[Danio]'
	instr2= ",[MxDbz1],[MxZDR1],[MxRho1],[MxPhi1],[MxKDP1],[Dbz451],[Dbz601],[MxDbzT],[MxZDRT],[MxRhoT],[MxPhiT],[MxKDPT]"
	instr3= ",[Dbz45T],[Dbz60T],[MnDBZ1],[MnZDR1],[MnRho1],[MnPhi1],[MnKDP1],[Dbz551],[Dbz0c]"
	instr4= ",[Dbz45c],[Dbz55c],[Dbz60c],[MnDBZT],[MnZDRT],[MnRhoT],[MnPhiT],[MnKDPT],[Dbz55T])"
	instr5= " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
	insertstring= instr1+instr2+instr3+instr4+instr5
    
	curins = conins.cursor()
	curins.execute(insertstring, idlocxevento,idevento,lat,lon,granizo,pordanio,danio,pxdBZ[0], pxZDR[0], pxRho[0], pxPhi[0], pxKDP[0], dbz45b, dbz60b, pxdBZ[23], pxZDR[23], pxRho[23], pxPhi[23], pxKDP[23],dbz45TE, dbz60TE, pxdBZ[12], pxZDR[12], pxRho[12], pxPhi[12], pxKDP[12], dbz55b, dbz0, dbz45, dbz55, dbz60,pxdBZ[24], pxZDR[24], pxRho[24], pxPhi[24], pxKDP[24], dbz55TE)
	
	curins.commit()

# Cierro la conexión con la base de datos
print "Almacenamiento finalizado"
con.close()
conins.close()

