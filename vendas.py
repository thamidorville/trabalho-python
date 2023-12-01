#VENDA efetuar uma venda (venda, valor e data)
# salvando os dados num arquivo vendas.csv

# - O Código deve ser gerado automaticamente e a
# data será a data e hora do momento em que a venda for salva no arquivo.

# o valor será a soma dos valores de todos os produtos inseridos na venda.

# Todo os produtos de uma venda devem estar especificados no arquivo PRODUTOS_VENDA.csv (Código Venda, Código do Produto, Quantidade).

import pandas as pd
import os
from datetime import datetime


#funcao pra criar o codigo automatico. se estiver vazio
# ele retorna 1 (uma venda feita)
def criar_codigo_venda_automa(df_vendas):
  if df_vendas.empty:
    return 1
  else:
    return df_vendas['Código'].max(
    ) + 1  #senao a partir do ultimo valor maximo e adiciona mais 1, ou seja a soma do ultimo numero + 1


def efetuar_venda():
  arquivo_estoque = 'CONTROLE_ESTOQUE.csv'
  arquivo_precos = 'PRECO_PRODUTO.csv'
  arquivo_vendas = 'VENDAS.csv'
  arquivo_produtos_venda = 'PRODUTOS_VENDA.csv'
  diretorio = '/home/runner/Python/pca_av2'

  df_estoque = pd.read_csv(os.path.join(diretorio, arquivo_estoque))
  df_precos = pd.read_csv(os.path.join(diretorio, arquivo_precos))

  #verificando se o arquivo de estoque está vazio
  if df_estoque.empty:
    print("Não há produtos no estoque.")
    return

  if not os.path.exists(os.path.join(diretorio, arquivo_vendas)):
    df_vendas = pd.DataFrame(columns=['Código', 'Valor', 'Data'])
    df_vendas.to_csv(os.path.join(diretorio, arquivo_vendas), index=False)
  else:
    df_vendas = pd.read_csv(os.path.join(diretorio, arquivo_vendas))

    #produtos venda aqui
  if not os.path.exists(os.path.join(diretorio, arquivo_produtos_venda)):
    df_produtos_venda = pd.DataFrame(
      columns=['Código Venda', 'Código Produto', 'Quantidade'])
    df_produtos_venda.to_csv(os.path.join(diretorio, arquivo_produtos_venda),
                             index=False)
  else:
    df_produtos_venda = pd.read_csv(
      os.path.join(diretorio, arquivo_produtos_venda))

  codigo_da_venda = criar_codigo_venda_automa(
    df_vendas)  #invocando a função que gera o codigo automaticamentr

  valor_total_da_venda = 0

  while True:
    print("Produtos disponíveis em Estoque: ")
    print(df_estoque[['Código', 'Descrição', 'Quantidade']])

    codigo_produto_a_ser_vendido = int(
      input("Digite o código do produto que você deseja vender: "))

    if codigo_produto_a_ser_vendido == 0:
      break

    if codigo_produto_a_ser_vendido not in df_estoque['Código'].values:
      print("Produto não encontrado no estoque!")
      continue

    preco_produto = df_precos.loc[
      df_precos['Código'] == codigo_produto_a_ser_vendido, 'Preço'].values[0]

    quantidade_a_ser_vendida = int(
      input(
        f"Digite a quantidade de '{df_estoque.loc[df_estoque['Código'] == codigo_produto_a_ser_vendido, 'Descrição'].values[0]}' que deseja vender: "
      ))

    #if pra verificar se existe produto suficiente no arquivo de estoque
    if quantidade_a_ser_vendida > df_estoque.loc[df_estoque['Código'] ==
                                                 codigo_produto_a_ser_vendido,
                                                 'Quantidade'].values[0]:
      print("Não há quantidade suficiente de produto no estoque.")

  #   #O
  # valor será a soma dos valores de todos os produtos inseridos na venda. T
    valor_produto = preco_produto * quantidade_a_ser_vendida
    valor_total_da_venda += valor_produto

    df_estoque.loc[
      df_estoque['Código'] == codigo_produto_a_ser_vendido,
      'Quantidade'] -= quantidade_a_ser_vendida  #atualiza o estoque diminuindo a quantidade que foi vendida do codigodo produto vendido

    df_produtos_venda = pd.concat([
      df_produtos_venda,
      pd.DataFrame({
        'Código Venda': [codigo_da_venda],
        'Código Produto': [codigo_produto_a_ser_vendido],
        'Quantidade': [quantidade_a_ser_vendida]
      })
    ],
                                  ignore_index=True)

    #cada produto vendido deve ser inserido e VENDAS.csv com o valor total
    # da venda (calculado a partir de PRECO_PRODUTO.csv e
    # PRODUTOS_VENDA.csv) e a respectiva data.
    df_vendas = pd.concat([
      df_vendas,
      pd.DataFrame({
        'Código': [codigo_da_venda],
        'Valor': [valor_total_da_venda],
        'Data': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
      })
    ],
                          ignore_index=True)
    df_estoque.to_csv(os.path.join(diretorio, arquivo_estoque), index=False)
    df_produtos_venda.to_csv(os.path.join(diretorio, arquivo_produtos_venda),
                             index=False)
    df_vendas.to_csv(os.path.join(diretorio, arquivo_vendas), index=False)

    print("Venda executada com sucesso!")
    break 


while True:
  efetuar_venda()
  menu_opcao = input(
    "Deseja realizar mais uma venda? Em caso positivo, digite sim, senão, encerrar: "
  ).lower()

  if menu_opcao == "encerrar":
    print("Encerrando o programa.")
    break
  elif menu_opcao != "sim":
    print(
      "Opção inválida. Digite 'sim' para realizar nova venda ou 'encerrar' para sair do programa."
    )
  else:
    efetuar_venda()


def main():

  if __name__ == "__main__":
    main()
