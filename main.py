import numpy as np
import xarray as xr





# Abrir o arquivo NetCDF

arquivos = ['./dados_cortados_media_pr_20010101_20240320_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc',
            './dados_cortados_media_pr_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc',
            './dados_cortados_media_pr_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc']

dataset_combinado = xr.open_mfdataset(arquivos, combine='by_coords')
dataset_combinado.to_netcdf('arquivo_final.nc')

#netcdf_path = "/Users/elizabetenunes/Desktop/dados_cortados_media_pr_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc"
#xrds = xr.open_dataset(netcdf_path)

xrds = xr.open_dataset('arquivo_final.nc')
# Selecionar a variável de precipitação
pr = xrds['pr']
#print(pr)
# Selecionar o período de referência
precip_ref = pr.sel(time=slice("19910101", "20201231"))

# Calcular a média climatológica
media_climatologica = precip_ref.groupby('time.month').mean(dim='time', skipna=True)

# Calcular a anomalia de precipitação
anomalia_precip = precip_ref.groupby('time.month') - media_climatologica

# Converter para NumPy e remover os NaN
anomalia_numpy = anomalia_precip.values
anomalia_sem_nan = anomalia_numpy[~np.isnan(anomalia_numpy)]

min_val = np.min(anomalia_sem_nan)
max_val = np.max(anomalia_sem_nan)

# Aplicar a fórmula de normalização entre -1 e 1
anomalia_normalizada = 2 * (anomalia_sem_nan - min_val) / (max_val - min_val) - 1

anomalia_normalizada_full = np.full_like(anomalia_numpy, np.nan)
anomalia_normalizada_full[~np.isnan(anomalia_numpy)] = anomalia_normalizada

# Criar um novo DataArray com as dimensões e coordenadas originais
anomalia_normalizada_da = xr.DataArray(
    anomalia_normalizada_full,
    dims=anomalia_precip.dims,
    coords=anomalia_precip.coords,
    name="anomalia_normalizada"
)

# Criar um novo dataset com a anomalia normalizada
dataset_anomalia = xr.Dataset({"anomalia_normalizada": anomalia_normalizada_da})

# Salvar no formato NetCDF
dataset_anomalia.to_netcdf('dados_tratados_xavier.nc')

print("Anomalia normalizada salva em 'dados_tratados_xavier.nc'")
# Exibir os valores sem NaN
#print(anomalia_normalizada)

# Se quiser exibir com as coordenadas:
#anomalia_stack = anomalia_precip.stack(z=('lat', 'lon')).dropna(dim='z')
#print(anomalia_stack)
