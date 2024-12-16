import gdown

# URL do arquivo do Google Drive
url = 'https://drive.google.com/uc?id=11yTPRMF9RgyF4irAWWydm8IKzlr3eI8_'  
output = 'pr_Tmax_Tmin_NetCDF_Files.zip' 

# Baixar o arquivo
gdown.download(url, output, quiet=False)
