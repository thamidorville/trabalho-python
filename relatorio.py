#relatorio - produtos vendidos por período
# criar gráfico
# que apresente qtd de produto vendido em determinado periodo de dias
# o usuario informa a data inicial e final e o prograam
#irá salvar um arquivo .png
# eixo X é a Descrição do Produto e o eixo Y é quantidade de
# produtos vendidos no período.

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def criar_grafico_produtos_vendidos(df_produtos_venda, df_vendas, df_estoque,
                                    data_inicial, data_final):
  data_inicial = datetime.combine(data_inicial, datetime.min.time())
  data_final = datetime.combine(data_final, datetime.max.time())

  vendas_periodo_dias = df_vendas[(df_vendas['Data'] >= data_inicial)
                                  & (df_vendas['Data'] <= data_final)]
  #mergeando dois dataframes, combinando os dados das duas tabelas
  #merge pra fazer uma tabela com as duas colunas e dados combinados das suas tabelas
  dados_mesclados = pd.merge(
      df_produtos_venda,
      vendas_periodo_dias,
      left_on='Código Venda',
      right_on='Código'
  )  #meslando os produtos vendidos com vendas por periodo de dias

  qtd_prod_vend = dados_mesclados.groupby('Código Produto').agg({
      'Quantidade':
      'sum'
  }).reset_index()

  #sum pra calcular a quantidade de produtos vendidos total

  descricao_produtos = pd.merge(
      qtd_prod_vend,
      df_estoque[['Código', 'Descrição']],
      left_on='Código Produto',
      right_on='Código'
  )  #combinando os produros do estoqye com a quantidade deles que foi vendida pra aparecer no grafico a descricao do produto no x e a quantidade no y

  plt.bar(descricao_produtos['Descrição'], descricao_produtos['Quantidade'])
  plt.xlabel('Descrição do Produto')
  plt.ylabel('Quantidade de Produtos Vendidos')
  plt.title('Quantidade de Produtos Vendidos por período')
  plt.xticks(rotation=45, ha='right')
  plt.tight_layout()

  arquivo_png = f'produtos_vendidos_{data_inicial}_{data_final}.png'
  plt.savefig(arquivo_png)

  # plt.close(arquivo_png)

  print("Gráfico gerado com sucesso!")


df_produtos_venda = pd.read_csv(
    '/home/runner/Python/pca_av2/PRODUTOS_VENDA.csv')
df_vendas = pd.read_csv('/home/runner/Python/pca_av2/VENDAS.csv')
df_estoque = pd.read_csv('/home/runner/Python/pca_av2/CONTROLE_ESTOQUE.csv')

df_vendas['Data'] = pd.to_datetime(df_vendas['Data'])

data_inicial = datetime.today().date()
data_final = df_vendas['Data'].max().date()

criar_grafico_produtos_vendidos(df_produtos_venda, df_vendas, df_estoque,
                                data_inicial, data_final)
