import rioxarray
import xarray as xr
import geopandas
import sys
import os
from shapely.geometry import mapping

# Argumentos: 1 = arquivo NetCDF, 2 = shapefile
path = sys.argv[1]
shapefile = sys.argv[2]

# Carrega os dados climáticos
data = xr.open_dataset(path)

# Define as dimensões espaciais e sistema de referência
data.rio.set_spatial_dims(x_dim="latitude", y_dim="longitude", inplace=True)
data.rio.write_crs("epsg:4326", inplace=True)

# Remove a variável 'time_bnds' se existir
data = data.drop_vars("time_bnds", errors="ignore")

# Lê o shapefile passado como argumento
sudeste = geopandas.read_file(shapefile)

# Garante que o shapefile tenha um CRS definido
if sudeste.crs is None:
    sudeste.set_crs("epsg:4326", inplace=True)

# Converte o CRS do shapefile para o mesmo do dataset
sudeste = sudeste.to_crs(data.rio.crs)

# Recorta os dados
clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)

# Salva o arquivo recortado
saida = "dados_cortados_" + os.path.basename(path)
clipped.to_netcdf(saida)

print("Dados de " + path + " cortados com sucesso!")
