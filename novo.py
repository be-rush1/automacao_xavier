import numpy as np
import xarray as xr
import os

# Abrir os arquivos NetCDF

os.system("cdo detrend dados_cortados_media_pr_20010101_20240320_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc dados_cortados_media_pr_20010101_20240320_BR-DWGD_UFES_UTEXAS_v_3.2.3_st.nc")
os.system("cdo detrend dados_cortados_media_pr_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc dados_cortados_media_pr_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_3.2.3_st.nc")
os.system("cdo detrend dados_cortados_media_pr_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc dados_cortados_media_pr_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_3.2.3_st.nc")

arquivos = [
    'dados_cortados_media_pr_20010101_20240320_BR-DWGD_UFES_UTEXAS_v_3.2.3_st.nc',
    'dados_cortados_media_pr_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_3.2.3_st.nc',
    'dados_cortados_media_pr_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_3.2.3_st.nc'
]

dataset_combinado = xr.open_mfdataset(arquivos, combine='by_coords')

# Selecionar a variável de precipitação
pr = dataset_combinado['pr']

# Definir o período de referência (1991-2020)
precip_ref = pr.sel(time=slice("19910101", "20201231"))

# Calcular a média climatológica mensal
media_climatologica = precip_ref.groupby('time.month').mean(dim='time', skipna=True)

#media_climatologica_janeiro = media_climatologica.sel(month=1)
media_anual = media_climatologica.mean(dim="month")



print(f"Mínimo média: {np.nanmin(media_climatologica)}")
print(f"Máximo média: {np.nanmax(media_climatologica)}")




# Função para calcular a anomalia
def calcular_anomalia(dados, media_climatologica):
    anomalia = dados.groupby('time.month') - media_climatologica

    return anomalia

# Calcular anomalias normalizadas
''' anomalia_1961_1980 = calcular_anomalia(
    pr.sel(time=slice("19610101", "19801231")), media_climatologica)
anomalia_1981_2000 = calcular_anomalia(
    pr.sel(time=slice("19810101", "20001231")), media_climatologica)
anomalia_2001_2024 = calcular_anomalia(
    pr.sel(time=slice("20010101", "20241231")), media_climatologica
) '''

anomalia_1961_2024 = calcular_anomalia(
    pr.sel(time=slice("19610101", "20241231")), media_climatologica
)





min_anomalia = anomalia_1961_2024.min()
max_anomalia = anomalia_1961_2024.max()

anomalia_norm = 2 * ((anomalia_1961_2024 - min_anomalia) / (max_anomalia - min_anomalia)) - 1


#print("Valor máximo normalizado:", np.nanmax(anomalia_norm_combinada.values))


# Salvar todas as anomalias normalizadas (1961-2024)

anomalia_norm.to_netcdf("anomalias_1961_2024_norm.nc")
print("Arquivo salvo: anomalias_normalizadas_1961_2024.nc")






# Selecionar a anomalia de 2020 (do verão)


# Plotar anomalia normalizada de 2020


'''anomalia_1961_2024.plot(
    ax=ax,
    cmap="coolwarm",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": "Precipitação média janeiro região sudeste"}
)'''

# Adicionar o shapefile da Região Sudeste