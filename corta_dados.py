import rioxarray
import xarray as xr
import geopandas
import sys
import os
from shapely.geometry import mapping

# Caminho do arquivo NetCDF recebido como argumento
path = sys.argv[1]

# Abre o dataset
data = xr.open_dataset(path)

# Configura as dimensões espaciais
data.rio.set_spatial_dims(x_dim="latitude", y_dim="longitude", inplace=True)

# Define o CRS do NetCDF como WGS84 (EPSG:4326)
data.rio.write_crs("EPSG:4326", inplace=True)

# Remove a variável de tempo, se existir
data = data.drop_vars("time_bnds", errors="ignore")

# Carrega o shapefile da região Sudeste
sudeste = geopandas.read_file("BR_região_sudeste_2022.shp")

# Verifica e define/reprojeta o CRS corretamente
if sudeste.crs is None:
    print("Shapefile sem CRS. Atribuindo EPSG:4326.")
    sudeste = sudeste.set_crs("EPSG:4326")
else:
    sudeste = sudeste.to_crs("EPSG:4326")

# Faz o recorte espacial usando a geometria do shapefile
clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)

# Verifica se há dados após o recorte
if clipped.time.size == 0:
    print(f"Nenhum dado encontrado após o recorte para o arquivo {path}. Verifique se os dados e o shapefile se sobrepõem.")
    sys.exit(1)

# Salva o novo NetCDF recortado
output_path = f"dados_cortados_{os.path.basename(path)}"
clipped.to_netcdf(output_path)

print(f"Dados de {path} cortados com sucesso e salvos em {output_path}")
