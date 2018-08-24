ImgCompuestas
=============

Serie de scripts Python para generar y trabajar con las imágenes del radar (plataformas Windows y Linux)
Este script es parte del set de software desarrollado por INTA para el tratamiento de los datos de los radares meteorológicos.

	
Esta versión permite el cálculo de imágenes compuestas en el rango de 240 km para las variables Z (dBZ), ZDR, PhiDP, KDP y RhoHV.

Los argumentos son: 
	
	path_img: "Ubicación de los archivos raster a procesar"
	fecha: "Fecha a procesar, formato: aaaammdd"
	extension: "Extensión de los archivos a procesar, para imágenes valor x defecto: tif"
	variable: "Variable a procesar. Posibles valores dBZ, ZDR, RhoHV, KDP, PhiDP, E. Valor por defecto: dBZ"
	-mto: "Calcula imágenes compuestas x cada paso de toma de datos (default: 10 minutos). Para todas las elevaciones."
	-ele: "Número de elevación a procesar. Posibles valores: 0 (todas), 1 a 12."
	-d: "Indica que no hace falta generar las imágenes horarias para la imágen compuesta de 24 horas y todas las elevaciones."
	-maxi: "Genera la imágen compuesta con el valor máximo"
	-mini: "Genera la imágen compuesta con el valor mínimo"
	-prom: "Genera la imágen compuesta con el valor promedio"
	-tot: "Genera la imágen compuesta con el valor total"


Modo de uso
=============

Este ejemplo procesa las imágenes `tif` del primero de Marzo de 2013 (`20130301`) de la variable `dBZ` y la primera elevación (`ele 1`) para calcular el valor mínimo (`mini`)
~~~
python GIC.py lugar\donde\se\encuentran\los\datos 20130301 tif dBZ -ele 1 -mini

~~~
