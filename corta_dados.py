import rioxarray
import xarray as xr
import geopandas
import sys
import os
from shapely.geometry import mapping
path = sys.argv[1]
data = xr.open_dataset(path)
data.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude", inplace=True)
data.rio.write_crs("epsg:4326", inplace=True)
data = data.drop_vars("time_bnds", errors="ignore")
sudeste = geopandas.read_file('BR_região_sudeste_2022.shp', crs="epsg:4326")
clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)
clipped.to_netcdf("dados_cortados_" + sys.argv[1])
print("Dados de " + sys.argv[1] + " cortados com sucesso!")
