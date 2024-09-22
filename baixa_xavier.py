import gdown

# URL do arquivo do Google Drive
url = 'https://drive.google.com/uc?id=1DLkySuH0S8C4pTaSxNgn8zRFP4Wlc3kk'  
output = 'pr_Tmax_Tmin_NetCDF_Files.zip' 

# Baixar o arquivo
gdown.download(url, output, quiet=False)
