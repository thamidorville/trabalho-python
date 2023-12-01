import pandas as pd
import os
from preco_produto import criar_arq_preco_produto


#controle de estoque: INSERIR - permite que o usuário cadastre um produto e salve os dados do produto usando um arquivo. codigo (int) descricao do produto (string) qtde(int)

# usuário irá informar a quantidade e a descrição do produto.


#O Código do Produto deve ser gerado automaticamente pelo programa.
#o codigo deve ser unico; se já existe um código de 157 no arquivo, não
# pode cadastrar o número 157 novamente. Crie um arquivo chamado
# CONTROLE_ESTOQUE.csv para salvar estas informações.
def inserir_produto():
  arquivo = 'CONTROLE_ESTOQUE.csv'
  diretorio = '/home/runner/Python/pca_av2'
  # df = pd.DataFrame(columns=['Código', 'Descrição', 'Quantidade'])
  # df.to_csv(os.path.join(diretorio, arquivo), index=False)

  if not os.path.exists(
      os.path.join(diretorio, arquivo)
  ):  #verificar se arquivo de controle de estoque existe, se nao existir ele cria
    df = pd.DataFrame(columns=['Código', 'Descrição', 'Quantidade'])
    df.to_csv(os.path.join(diretorio, arquivo), index=False)
  else:
    df = pd.read_csv(
      os.path.join(diretorio, arquivo)
    )  #do contrario, se exiostir o arquivo, read_csv vai ler o CONTROLE_ESTOQUE.csv que está na variavel arquivo
  # df = pd.read_csv(
  #   arquivo)  #se existir ele carrega o arquivo de controle de estoque

  # usuário irá informar a quantidade e a descrição do produto.
  descricao = input("Digite o nome do produto: ")
  quantidade = int(input("Digite a quantidade do produto: "))

  #o codigo do produto deve ser gerado automaticamente pelo programa e deve ser único
  if len(df) == 0:  #se a quantidade do dataframe df estiver = 0 ou seja, vazio
    codigo = 1  #atribua o codigo 1 ao produto
  else:
    codigo = df['Código'].max() + 1 if pd.notna(
      df['Código'].max()
    ) else 1  #se tiver um numero na coluna codigo entao ele vai adicionar mais 1 ao numerio ja existente, senao existir numero, entao ele começa acionando 1

  # for novo_codigo in range(
  #     df['Código'].max() + 1, float('inf')
  # ):  #codigo atual + 1 // e esse float inf é pra garantir que o codigo busque um codigo unicoinfinitamente
  #   if novo_codigo not in df[
  #       'Código'].values:  #se nao tiver o numero gerado então vai verificar e
  #     codigo = novo_codigo
  #     break
  # else:
  #   codigo = df['Código'].max(
  #   ) + 1  #senao pegue o valor maximo e adicione 1 para o proximo codigo

  while codigo in df['Código'].values:
    print('Este código já existe. Gerando um novo código de produto...')
    codigo += 1  # o laco continua ate encontrar um unico

  novo_produto = {
    'Código': codigo,
    'Descrição': descricao,
    'Quantidade': quantidade
  }
  # df = df.append(novo_produto, ignore_index=True)
  df = pd.concat([df, pd.DataFrame([novo_produto])], ignore_index=True)
  df.to_csv(
    os.path.join(diretorio, arquivo), index=False
  )  #to_csv = enviar/salvar/mandar pra o arquivo csv que no caso é o controle_estoque.csv. vai mandar o produto e quantidade p´ra la

  # inserri produto no df

  # dicionario_produtos = {
  #   'Código': codigo,
  #   'Descrição': descricao,
  #   'Quantidade': quantidade
  # }
  # df = df.append(
  #   dicionario_produtos
  # )  #adicionando o produto ao df. aqui é adicionada as chaves(codigo, descricao e quantidade, como uma linha na tabela (df
  return df
  # df = pd.concat([df, pd.DataFrame([dicionario_produtos])], ignore_index=True)

  # df.to_csv(os.path.join(diretorio, arquivo),
  #           index=False)  #salvando o arquivo como Controle_estoque.csv


resultado = inserir_produto()
print(resultado)

#  PESQUISAR
# permitir que o usuário pesquise por um produto cadastrado por:
# - codigo do produto
# - descricao do produto
# - resultado da busca deve ser apresentado na tela caso exista e uma mensagem informando que nao existe caso nao exista


def pesquisar_produto():
  arquivo = 'CONTROLE_ESTOQUE.csv'
  diretorio = '/home/runner/Python/pca_av2'

  df = pd.read_csv(
    os.path.join(diretorio, arquivo)
  )  #read_csv() carrega os dados do arquivo. vai ler os dados e carregá-los

  while True:
    resultado_pesquisa = input(
      "Digite o nome do produto ou o número do código do produto que deseja buscar: "
    ).lower()

    if resultado_pesquisa == "sair":
      break

    if resultado_pesquisa.isdigit():  #se o usuario digitar numeros
      resultado_pesquisa = int(
        resultado_pesquisa
      )  #converte pra numero pra que seja possivel pesquisarf o codigo
      resultado_df = df[
        df['Código'] ==
        resultado_pesquisa]  #comparando o que o usuario digitou com o que tem na coluna do df codigo, cria um novo dataframe com o resultado digitado pelo usuario
    else:
      resultado_df = df[df['Descrição'].str.contains(
        resultado_pesquisa, case=False, regex=False
      )]  #filtra onde a condição seja true para o que o usuario digitou no caso de true (existir no dataframe) o produto

    if not resultado_df.empty:
      print(resultado_df)
      escolher_editar_ou_remover(df, resultado_pesquisa)
      break  #sai dpo looop depois do produto ser editado
    else:
      print('Produto não cadastrado')
      inserir_novo_produto = input(
        'Deseja adicionar um novo produto? sim ou não').lower()
      if inserir_novo_produto == "sim":
        return True
      else:
        return False


#alterar a descrição do produto ou a quantidade
# EDITAR / REMOVER
def escolher_editar_ou_remover(df, codigo_produto):
  menu_opcoes = input("Você quer editar, remover ou sair deste menu?").lower()
  if menu_opcoes == "editar":
    editar_produto(df, codigo_produto)
  elif menu_opcoes == 'remover':
    remover_produto(df, codigo_produto)
  elif menu_opcoes == 'sair':
    pass
  else:
    print("Opção inválida. Você precisa escolher dentre as opções sugeridas. ")


def editar_produto(df, codigo_produto):
  nova_descricao_produto = input("Edite o novo nome para o produto: ")
  nova_quantidade_produto = input("Edite o número da quantidade do produto: ")

  nova_quantidade_produto = int(nova_quantidade_produto)

  df.loc[df['Código'] == codigo_produto, 'Descrição'] = nova_descricao_produto
  df.loc[df['Código'] == codigo_produto,
         'Quantidade'] = nova_quantidade_produto

  df.to_csv('CONTROLE_ESTOQUE.csv', index=False)
  print("Seu produto foi editado!")


def remover_produto(df, codigo_produto):
  # df = df[df['Código'] != codigo_produto]
  # df.to_csv('CONTROLE_ESTOQUE.csv', index=False)
  # print("Produto removido!")
  codigo_remocao_produto = input(
    "Digite o código do produto que deseja remover: ")

  try:  #exceção pro caso do usuario digitar um codigo invalido
    codigo_remocao_produto = int(codigo_remocao_produto)
  except ValueError:
    print("Código inexistente. Insira um código de produto válido.")
    return

  if codigo_remocao_produto in df['Código'].values:
    df = df[df['Código'] != codigo_remocao_produto]
    df.to_csv('CONTROLE_ESTOQUE.csv', index=False)
    print("Produto removido!")
  else:
    print("produto não localizado.")


arquivo = 'CONTROLE_ESTOQUE.csv'
diretorio = '/home/runner/Python/pca_av2'
df = pd.read_csv(os.path.join(diretorio, arquivo))

# def inserir_produto(df):
#   pass

# pesquisar_produto()
# inserir_produto()

codigo_produto = pesquisar_produto()

if codigo_produto is not None:
  remover_produto(df, codigo_produto)


def main():
  criar_arq_preco_produto()

  while True:
    df_inserir_produto = inserir_produto()
    print(df_inserir_produto)

    codigo_produto = pesquisar_produto()

    if not codigo_produto:
      break  #pra parar de pedir pra pesquisar produto depois de editar, remover e excluior

    remover_produto(df, codigo_produto)


#   # inserir_produto()
#   # criar_arq_preco_produto()
#   # pesquisar_produto()
#   df_inserir_produto = inserir_produto()
#   print(df_inserir_produto)

#   codigo_produto = pesquisar_produto()

#   if codigo_produto is not None:
#     remover_produto(df, codigo_produto)

# if __name__ == "__main__":
#   main()
