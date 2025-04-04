import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Abrir os arquivos NetCDF
arquivos = [
    '/Users/elizabetenunes/Desktop/dados_cortados_media_pr_20010101_20240320_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc',
    '/Users/elizabetenunes/Desktop/dados_cortados_media_pr_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc',
    '/Users/elizabetenunes/Desktop/dados_cortados_media_pr_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc'
]

dataset_combinado = xr.open_mfdataset(arquivos, combine='by_coords')

# Selecionar a variável de precipitação
pr = dataset_combinado['pr']

# Definir o período de referência (1991-2020)
precip_ref = pr.sel(time=slice("19910101", "20201231"))

# Calcular a média climatológica mensal
media_climatologica = precip_ref.groupby('time.month').mean(dim='time', skipna=True)

# Função para calcular a anomalia
def calcular_anomalia(dados, media_climatologica):
    anomalia = dados.groupby('time.month') - media_climatologica


    return anomalia

# Calcular anomalias normalizadas
anomalia_1961_1980 = calcular_anomalia(
    pr.sel(time=slice("19610101", "19801231")), media_climatologica)
anomalia_1981_2000 = calcular_anomalia(
    pr.sel(time=slice("19810101", "20001231")), media_climatologica)
anomalia_2001_2024 = calcular_anomalia(
    pr.sel(time=slice("20010101", "20241231")), media_climatologica
)

# Concatenar as anomalias
anomalia_combinada = xr.concat(
    [anomalia_1961_1980, anomalia_1981_2000, anomalia_2001_2024], dim='time'
)

min_anomalia = np.nanmin(anomalia_combinada.values)
max_anomalia = np.nanmax(anomalia_combinada.values)
anomalia_norm_combinada = 2 * ((anomalia_combinada - min_anomalia) / (max_anomalia - min_anomalia)) - 1

print("Valor mínimo normalizado:", np.nanmin(anomalia_norm_combinada.values))
print("Valor máximo normalizado:", np.nanmax(anomalia_norm_combinada.values))


# Salvar todas as anomalias normalizadas (1961-2024)
anomalia_norm_combinada.to_netcdf("/Users/elizabetenunes/Desktop/anomalias_normalizadas_1961_2024.nc")
print("Arquivo salvo: anomalias_normalizadas_1961_2024.nc")

# Selecionar a anomalia de 2020 (média anual)
anomalia_norm_2020 = anomalia_norm_combinada.sel(time=slice("20200101", "20200331")).mean(dim='time')

# Salvar a anomalia normalizada de 2020
anomalia_norm_2020.to_netcdf("/Users/elizabetenunes/Desktop/anomalia_normalizada_2020.nc")
print("Arquivo salvo: anomalia_normalizada_2020.nc")

print("\nVerificação dos dados:")
print(f"Valor mínimo: {np.nanmin(anomalia_norm_2020.values):.4f}")
print(f"Valor máximo: {np.nanmax(anomalia_norm_2020.values):.4f}")
print(f"Média: {np.nanmean(anomalia_norm_2020.values):.4f}")

# Carregar o shapefile da região Sudeste
shapefile_path = "/Users/elizabetenunes/Desktop/BR_regiao_sudeste_2022/BR_região_sudeste_2022.shp"
regiao_sudeste = gpd.read_file(shapefile_path)

# Criar o mapa
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': ccrs.PlateCarree()})

# Adicionar feições ao mapa
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=1)
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.set_extent([-55, -35, -25, -10])  # Limites aproximados da Região Sudeste

# Plotar anomalia normalizada de 2020
anomalia_norm_2020.plot(
    ax=ax,
    cmap="coolwarm",
    transform=ccrs.PlateCarree(),
    cbar_kwargs={"label": "Anomalia Normalizada"}
)

# Adicionar o shapefile da Região Sudeste
regiao_sudeste.boundary.plot(ax=ax, color="black", linewidth=1, transform=ccrs.PlateCarree())

# Título e exibição
plt.title("Anomalia Normalizada de Precipitação - 2020 (Região Sudeste)")
plt.show()
