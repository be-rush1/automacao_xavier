import rioxarray
import xarray as xr
import geopandas
import sys
import os
from shapely.geometry import mapping

path = sys.argv[1]
data = xr.open_dataset(path)

# Define dimensões espaciais
data.rio.set_spatial_dims(x_dim="latitude", y_dim="longitude", inplace=True)
data.rio.write_crs("epsg:4326", inplace=True)

# Remove variáveis que podem dar erro
data = data.drop_vars("time_bnds", errors="ignore")

# Lê shapefile e reprojeta
sudeste = geopandas.read_file('BR_região_sudeste_2022.shp')
sudeste = sudeste.to_crs("EPSG:4326")

# Corta com geometria
clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)

# Verifica se há dados temporais
if "time" not in clipped or clipped.time.size == 0:
    print(f"Nenhum dado espacial/temporal presente após o corte em {path}.")
    sys.exit(0)

# Salva o resultado
output_name = "dados_cortados_" + os.path.basename(path)
clipped.to_netcdf(output_name)
print(f"Dados de {path} cortados com sucesso!")
