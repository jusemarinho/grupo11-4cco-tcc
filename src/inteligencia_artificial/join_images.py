import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def listar_arquivos(diretorio, extensao=".jpg"):
    arquivos = []
    for root, _, files in os.walk(diretorio):
        for file in files:
            if file.endswith(extensao):
                arquivos.append(os.path.join(root, file))
    return arquivos

diretorio_principal = "/pets_tests_clean"

num_colunas = 10

arquivos_imagem = listar_arquivos(diretorio_principal)

tamanho_miniatura = (50, 50)

imagem_composta = np.zeros((tamanho_miniatura[1] * (len(arquivos_imagem) // num_colunas + 1),
                            tamanho_miniatura[0] * num_colunas, 3), dtype=np.uint8)

for i, caminho_imagem in enumerate(arquivos_imagem):
    imagem = cv2.imread(caminho_imagem)
    miniatura = cv2.resize(imagem, tamanho_miniatura)
    
    linha = i // num_colunas
    coluna = i % num_colunas
    
    x_inicio = coluna * tamanho_miniatura[0]
    y_inicio = linha * tamanho_miniatura[1]
    
    imagem_composta[y_inicio:y_inicio+tamanho_miniatura[1], x_inicio:x_inicio+tamanho_miniatura[0]] = miniatura

plt.imshow(imagem_composta)
plt.axis('off')
plt.show()