import pandas as pd
import os

# ##############   VENDAS    #############

#preço - permitir que cada produto tenha yum preco
# ler o CONTROLE_ESTOQUE.csv para obter os codigos dos produtos
# e associar um preco a cada um deles

# - criar arquivo PRECO_PRODUTO.csv PARA SALVAR o código do produto e o preço


def criar_arq_preco_produto():
  arquivo_estoque = 'CONTROLE_ESTOQUE.csv'
  arquivo_precos = 'PRECO_PRODUTO.csv'
  diretorio = '/home/runner/Python/pca_av2'
  #se nao existir cria o dataframe preco_produto
  if not os.path.exists(os.path.join(diretorio, arquivo_precos)):
    df_preco = pd.DataFrame(columns=['Código', 'Preço'])
    df_preco.to_csv(os.path.join(diretorio, arquivo_precos), index=False)
  else:
    df_preco = pd.read_csv(os.path.join(diretorio, arquivo_precos))

  df_estoque = pd.read_csv(os.path.join(diretorio, arquivo_estoque))
  #itera sobre cada codigo unico e junta cada codigo com o preco com concat
  for codigo_produto in df_estoque['Código'].unique():
    if codigo_produto not in df_preco['Código'].values:
      df_preco = pd.concat(
        [df_preco,
         pd.DataFrame({
           'Código': [codigo_produto],
           'Preço': [0.0]
         })],
        ignore_index=True)

  df_preco.to_csv(os.path.join(diretorio, arquivo_precos), index=False)


if __name__ == "__main__":
  criar_arq_preco_produto()

# EDITAR:
# 1. Permite alterar o preço do produto. Mas não deve permitir
# apagar um produto por aqui. Somente na opção de Controle
# de Estoque


def editar_preco_produto():
  arquivo_estoque = 'CONTROLE_ESTOQUE.csv'
  arquivo_precos = 'PRECO_PRODUTO.csv'
  diretorio = '/home/runner/Python/pca_av2'

  df_preco = pd.read_csv(os.path.join(diretorio, arquivo_precos))
  df_estoque = pd.read_csv(
    os.path.join(diretorio, arquivo_estoque)
  )  #estou lendo os dados dos arquivos e convertendo eles em um dataframe
  print("Listagem de produtos por Código e preço: ")
  print(df_preco[['Código', 'Preço']])

  codigo_produto = int(input("Digite o código do produto que deseja editar: "))
  if codigo_produto not in df_preco['Código'].values:
    print(
      "Código não encontrado. Por favor, digite um código de produto disponível: "
    )
    return

  preco_editado = float(input("Digite aqui o novo preço do produto:  "))

  #loc vai localizar a linha do dataframe que seja a do codigo do produto e vai atribuir o valor digitado do usuario da variavel preco_editado a coluna preco exatamente ao codigo que o usuario digitou
  df_preco.loc[df_preco['Código'] == codigo_produto, 'Preço'] = preco_editado

  # e em seguida salva a edicao com o to_csv

  df_preco.to_csv(os.path.join(diretorio, arquivo_precos), index=False)
  print("editado com sucesso!")
  print(df_preco[['Código', 'Preço']])


if __name__ == "__main__":
  editar_preco_produto()
