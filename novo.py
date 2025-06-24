import numpy as np
import xarray as xr
import os

# Caminhos dos arquivos originais e de saída
caminhos_originais = [
    "./dados_cortados_media_pr_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc",
    "./dados_cortados_media_pr_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc",
    "./dados_cortados_media_pr_20010101_20240320_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc"
]

caminhos_detrended = [
    caminho.replace(".nc", "_st.nc") for caminho in caminhos_originais
]

# Remover tendência com precisão de ponto flutuante
#for entrada, saida in zip(caminhos_originais, caminhos_detrended):
#    os.system(f"cdo -b F64 detrend {entrada} {saida}")

# Abrir os arquivos detrended (sem dask)
ds = xr.open_mfdataset(caminhos_detrended, combine='by_coords', chunks={})

# Selecionar a variável de precipitação
pr = ds['pr']

# Definir período de referência (1991-2020) para normalização
periodo_ref = pr.sel(time=slice("1991-01-01", "2020-12-31"))
media_climatologica = periodo_ref.groupby('time.month').mean('time')

# Função para calcular anomalia
def calcular_anomalia(dados, media_clima):
    return dados.groupby('time.month') - media_clima

# Calcular anomalia para toda a série (1961-2024)
anomalia = calcular_anomalia(pr.sel(time=slice("1961-01-01", "2024-12-31")), media_climatologica)

# Normalização entre -1 e 1
min_val = anomalia.min()
max_val = anomalia.max()
anomalia_normalizada = 2 * ((anomalia - min_val) / (max_val - min_val)) - 1

# Salvar resultado em NetCDF
saida_nc = "./anomalias_1961_2024_normalizada_sem_tendencia.nc"
anomalia_normalizada.to_netcdf(saida_nc)

print(f"Arquivo salvo com sucesso em: {saida_nc}")
