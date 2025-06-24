import rioxarray
import xarray as xr
import geopandas as gpd
import sys
import os
from shapely.geometry import mapping

# Caminho do arquivo NetCDF passado via linha de comando
path = sys.argv[1]

# Abrir o dataset
data = xr.open_dataset(path)

# Corrigir a ordem das dimensões espaciais: longitude = x, latitude = y
data.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude", inplace=True)

# Definir o sistema de referência de coordenadas (CRS)
data.rio.write_crs("EPSG:4326", inplace=True)

# Remover variável de limites de tempo, se existir
data = data.drop_vars("time_bnds", errors="ignore")

# Ler o shapefile da região sudeste (corrigir possível problema de codificação no nome)
shapefile_path = 'BR_região_sudeste_2022.shp'
sudeste = gpd.read_file(shapefile_path)

# Clipping com geometria do shapefile
clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)

# Nome do arquivo de saída
output_name = "dados_cortados_" + os.path.basename(path)
clipped.to_netcdf(output_name)

print("Dados de " + path + " cortados com sucesso! Arquivo salvo como " + output_name)
