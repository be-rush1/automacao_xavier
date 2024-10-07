import gdown

# URL do arquivo do Google Drive
url = 'https://drive.google.com/uc?id=1ATAtgnG2_zSfar1TAKu3SIn5c0RsBHJG'  
output = 'pr.npz' 

# Baixar o arquivo
gdown.download(url, output, quiet=False)
