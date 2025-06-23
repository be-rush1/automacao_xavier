import rioxarray
import xarray as xr
import geopandas
import sys
import os
from shapely.geometry import mapping

# Arquivo NetCDF passado como argumento
path = sys.argv[1]
data = xr.open_dataset(path)

# Detecta os nomes corretos das dimensões espaciais
dims = list(data.dims)
x_dim = None
y_dim = None

for dim in dims:
    if dim.lower() in ["lon", "longitude"]:
        x_dim = dim
    elif dim.lower() in ["lat", "latitude"]:
        y_dim = dim

if not x_dim or not y_dim:
    print(f"Erro: Dimensões espaciais não encontradas no arquivo {path}.")
    sys.exit(1)

# Define as dimensões espaciais corretamente
data.rio.set_spatial_dims(x_dim=x_dim, y_dim=y_dim, inplace=True)
data.rio.write_crs("EPSG:4326", inplace=True)

# Remove variável auxiliar de tempo, se existir
data = data.drop_vars("time_bnds", errors="ignore")

# Carrega o shapefile da região Sudeste
sudeste = geopandas.read_file("BR_região_sudeste_2022.shp")

# Garante que o CRS esteja definido
if sudeste.crs is None:
    print("Shapefile sem CRS. Atribuindo EPSG:4326.")
    sudeste = sudeste.set_crs("EPSG:4326")
else:
    sudeste = sudeste.to_crs("EPSG:4326")

# Faz o recorte espacial com base na geometria
clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)

# Verifica se o recorte retornou dados
if "time" in clipped.dims and clipped.time.size == 0:
    print(f"Nenhum dado encontrado após o recorte em {path}. Verifique a sobreposição geográfica.")
    sys.exit(1)

# Gera nome de saída
basename = os.path.basename(path)
if basename.startswith("dados_cortados_"):
    basename = basename.replace("dados_cortados_", "")

output_path = f"dados_cortados_{basename}"
clipped.to_netcdf(output_path)

print(f"Dados de {path} cortados com sucesso e salvos em {output_path}")
