import numpy as np

# Carrega o arquivo .npz
data = np.load('pr.npz')

# Exibe as chaves (nomes dos arrays contidos no arquivo)
print(data.files)

# Acessa cada array pelo nome da chave
for key in data.files:
    print(f"Array '{key}':\n{data[key]}\n")

for key in data.files:
    np.save(f'{key}.npy', data[key])  # Salva cada array em formato .npy
