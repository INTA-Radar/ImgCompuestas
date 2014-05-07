#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Autores: Santiago Banchero, Yanina Bellini Saibene
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

try:
	from osgeo import gdal
except ImportError:
	raise ImportError,"Se requiere el modulo osgeo.  Se puede descargar de http://www.lfd.uci.edu/~gohlke/pythonlibs/"

class Identify:
    
    def __init__(self, ruta):
		
		self.i = gdal.Open(ruta)
		
		# Tamaño de la imagen
		self.rows = self.i.RasterYSize
		self.cols = self.i.RasterXSize
		self.bands = self.i.RasterCount

		# información de la georeferenciación
		self.transform = self.i.GetGeoTransform()
		self.xOrigin = self.transform[0]
		self.yOrigin = self.transform[3]
		self.pixelWidth = self.transform[1]
		self.pixelHeight = self.transform[5]
		
		# recupera la banda 1: OJO esto si hay más bandas!!
		self.band = self.i.GetRasterBand(1)
		# Esto es la matriz NxM de datos de la imagen, acá están TODOS los 
		# valores de pixeles de la imagen
		self.data = self.band.ReadAsArray(0, 0, self.cols, self.rows)
		     
    def get_pixel_value(self,x,y):
        # transforma de coordenadas geo a cordenadas de la matriz
        xOffset = int((float(x) - self.xOrigin) / self.pixelWidth)
        yOffset = int((float(y) - self.yOrigin) / self.pixelHeight)
        
        return self.data[yOffset, xOffset] 

    def get_pixel_data(self,y,x):
		# devuelve el dato del pixel
        return self.data[y][x]
		
	
		
def main():
	
	return 0

if __name__ == '__main__':
	main()
