import rioxarray
import xarray as xr
import geopandas
import sys
from shapely.geometry import mapping
import numpy as np

path = sys.argv[1]
data = xr.open_dataset(path)

# Atenção aqui: longitude e latitude no lugar certo
data.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude", inplace=True)
data.rio.write_crs("EPSG:4326", inplace=True)
data = data.drop_vars("time_bnds", errors="ignore")

sudeste = geopandas.read_file("BR_regiao_sudeste_2022.shp")

# Reprojeta shapefile se CRS diferente
if sudeste.crs != data.rio.crs:
    sudeste = sudeste.to_crs(data.rio.crs)

print("Limites dos dados:")
print(f"lon: {data.longitude.min().values} a {data.longitude.max().values}")
print(f"lat: {data.latitude.min().values} a {data.latitude.max().values}")

print("Limites do shapefile sudeste:")
print(sudeste.total_bounds)

clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)

if clipped.dims['latitude'] == 0 or clipped.dims['longitude'] == 0 or clipped.dims.get('time', 1) == 0:
    print(f"Atenção: recorte de {path} retornou dataset vazio. Criando dataset nulo para salvar.")
    dims = {
        'time': data.dims.get('time', 1),
        'latitude': 1,
        'longitude': 1
    }
    clipped = xr.Dataset({
        'pr': (('time', 'latitude', 'longitude'), np.full((dims['time'], 1, 1), np.nan))
    }, coords={
        'time': data.coords.get('time', [0]),
        'latitude': [0],
        'longitude': [0]
    })
    clipped.rio.write_crs(data.rio.crs)

clipped.to_netcdf("dados_cortados_" + path)
print(f"Dados de {path} cortados com sucesso!")
