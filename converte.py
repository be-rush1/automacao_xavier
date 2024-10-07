import numpy as np
import xarray as xr
import pandas as pd

# Carregar o arquivo .npy
fname = "data.npy"
arr = np.load(fname)

# Criar um DataFrame com as colunas "lon", "lat" e "data"
df = pd.DataFrame({"lon": arr[:, 0], "lat": arr[:, 1], "data": arr[:, 3]})

# Remover duplicatas baseadas nas colunas "lat" e "lon"
df = df.drop_duplicates(subset=["lat", "lon"])

# Converter o DataFrame para um xarray.Dataset
ds = df.set_index(["lat", "lon"]).to_xarray()

# Salvar como arquivo .nc (NetCDF)
ds.to_netcdf("data.nc")
