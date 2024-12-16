import gdown

# URL do arquivo do Google Drive
url = 'https://drive.google.com/uc?id=11yTPRMF9RgyF4irAWWydm8IKzlr3eI8_'  
output = 'pr.npz' 

# Baixar o arquivo
gdown.download(url, output, quiet=False)
