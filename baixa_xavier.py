import gdown

# URL do arquivo do Google Drive
url = 'https://drive.google.com/uc?id=11-qnvwojirAtaQxSE03N0_SUrbcsz44N'  
output = 'pr.npz' 

# Baixar o arquivo
gdown.download(url, output, quiet=False)
