import rioxarray
import xarray as xr
import geopandas
import sys
from shapely.geometry import mapping
path = sys.argv[1]
data = xr.open_dataset(path)
data.rio.set_spatial_dims(x_dim="latitude", y_dim="longitude", inplace=True)
data.rio.write_crs("epsg:4326", inplace=True)
sudeste = geopandas.read_file('BR_região_sudeste_2022.shp', crs="epsg:4326")
clipped = data.rio.clip(sudeste.geometry.apply(mapping), sudeste.crs, drop=True)
clipped.to_netcdf("dados_cortados_" + arquivo + ".nc")
