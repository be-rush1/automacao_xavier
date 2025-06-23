import rioxarray
import xarray as xr
import geopandas
import sys
import os
from shapely.geometry import mapping
os.system("ls")
# Caminho para o arquivo NetCDF (passado via linha de comando)
path = sys.argv[1]

# Abre o dataset NetCDF
data = xr.open_dataset(path)

# Define os eixos espaciais para o rioxarray
data.rio.set_spatial_dims(x_dim="latitude", y_dim="longitude", inplace=True)

# Define o CRS do NetCDF (caso ainda não tenha)
data.rio.write_crs("EPSG:4326", inplace=True)

# Remove a variável time_bnds se existir
data = data.drop_vars("time_bnds", errors="ignore")

# Lê o shapefile da região sudeste
sudeste = geopandas.read_file("./BR_região_sudeste_2022.shp")

# Verifica e define CRS do shapefile, se necessário
if sudeste.crs is None:
    sudeste.set_crs("EPSG:4326", inplace=True)

# Reprojeta o shapefile para coincidir com o CRS do NetCDF
sudeste = sudeste.to_crs(data.rio.crs)

# Faz o recorte dos dados com base no shapefile
clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)

# Verifica se o recorte resultou em dados vazios
if clipped.time.size == 0:
    raise ValueError(f"O recorte do arquivo {path} resultou em um dataset vazio.")

# Salva o recorte em um novo arquivo NetCDF
saida = "dados_cortados_" + os.path.basename(path)
clipped.to_netcdf(saida)

print(f"Dados de {path} cortados com sucesso!")
