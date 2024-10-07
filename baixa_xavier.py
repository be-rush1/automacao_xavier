import gdown

# URL do arquivo do Google Drive
url = 'https://drive.google.com/uc?id=1ATAtgnG2_zSfar1TAKu3SIn5c0RsBHJG'  
output = 'pr_Tmax_Tmin_NetCDF_Files.zip' 

# Baixar o arquivo
gdown.download(url, output, quiet=False)
