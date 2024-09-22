import gdown

# URL do arquivo do Google Drive
url = 'https://drive.google.com/uc?id=1DLkySuH0S8C4pTaSxNgn8zRFP4Wlc3kk'  # Substitua pelo ID correto
output = 'arquivo_baixado.zip'  # Nome do arquivo de saída

# Baixar o arquivo
gdown.download(url, output, quiet=False)
