import pandas as pd
import numpy as np

from hash_table import HashTable
from linked_list import Node, LinkedList
from employee import Employee
import time


def preenche_busca(buscas, numero_registros, tamanho, indice_busca, elemento, tempo):
    buscas['numero_registros'].append(numero_registros)
    buscas['tamanho_hash'].append(tamanho)
    buscas['indice_busca'].append(indice_busca)
    buscas['elemento'].append(elemento)
    buscas['tempo'].append(tempo)

    return buscas

for numero_registros in [5000, 20000, 100000]:

    dados = {
        'tamanho_hash': [],
        'numero_registros': [],
        'numero_colisoes': [],
        'ocupacao_media_chaves': [],
        'ocupacao_std_chaves': []
    }

    buscas = {
        'tamanho_hash': [],
        'numero_registros': [],
        'elemento': [],
        'indice_busca': [],
        'tempo': []
    }

    print(f"Iniciando para número de registros {numero_registros}.")
    counter = 0
    numero_comparacoes = 5
    for execucao in range(numero_comparacoes):  # execuções independentes
        print(f"Iniciando execução no. {execucao+1}/{numero_comparacoes}.")
        df = pd.read_csv(f"dados/dados_aula03_faed_1000000.csv")
        df.drop_duplicates(subset=['matricula'], keep='last', inplace=True)
        df = df.sample(numero_registros)

        for tamanho in [1000, 10000, 100000]:
            print(f"Iniciando teste com hash tamanho {tamanho}.")
            # Alimentar Tabela Hash
            ht = HashTable(tamanho, LinkedList)  # Hashtable com Lista ligada
            ht_list = HashTable(tamanho)  # Hashtable com lista comum
            lista_comum = []  # Lista comum apenas

            print(f"Iniciando alimentação das estruturas.")
            for i, v in df.iterrows():
                employee = Employee(v['matricula'], v['salario'], v['setor'])
                node = Node(employee, index=employee.matricula)

                ht.push(employee.matricula, node)
                ht_list.push(employee.matricula, node)
                lista_comum.append(node)

            # Informações globais
            dados['tamanho_hash'].append(tamanho)
            dados['numero_registros'].append(numero_registros)
            dados['numero_colisoes'].append(ht.collisions_number)
            dados['ocupacao_media_chaves'].append(np.mean(ht.occupation))
            dados['ocupacao_std_chaves'].append(np.std(ht.occupation))

            # Pesquisar na Tabela Hash
            ## Selecionar 100k matrículas aleatórias
            print(f"Iniciando 100k comparações.")
            comparacoes = 20000  # * 5 execucoes independentes = 100k
            matriculas = np.random.choice(df['matricula'].values, comparacoes)

            tempos_hash_linkedlist = []
            tempos_hash_list = []
            tempos_lista_comum = []
            for idx, i in enumerate(matriculas):
                if idx % (comparacoes / 10) == 0:
                    print(f"{idx} comparações realizadas.")
                inicio = time.time()
                ht.find(i)
                tempos_hash_linkedlist.append(time.time() - inicio)

                inicio = time.time()
                ht_list.find(i)
                tempos_hash_list.append(time.time() - inicio)

                inicio = time.time()
                for j in lista_comum:
                    if j.index == i:
                        break
                tempos_lista_comum.append(time.time() - inicio)

            buscas = preenche_busca(buscas, numero_registros, tamanho, counter, "hash+linkedlist",
                                    np.mean(tempos_hash_linkedlist))
            buscas = preenche_busca(buscas, numero_registros, tamanho, counter, "hash+list",
                                    np.mean(tempos_hash_list))
            buscas = preenche_busca(buscas, numero_registros, tamanho, counter, "list",
                                    np.mean(tempos_lista_comum))

            counter += 1

            print(f"\nCenário: Número de registros {numero_registros}, tamanho {tamanho}")
            print(f"Número de colisões: {ht.collisions_number}")
            print(f"Taxa de ocupação: {np.mean(ht.occupation)} +/- {np.std(ht.occupation)}")

            print(
                f"Tempos hash + lista ligada: {np.mean(tempos_hash_linkedlist):.50f} +/- {np.std(tempos_hash_linkedlist):.20f}")
            print(f"Tempos hash + list: {np.mean(tempos_hash_list):.50f} +/- {np.std(tempos_hash_list):.20f}")
            print(f"Tempos lista comum: {np.mean(tempos_lista_comum):.50f} +/- {np.std(tempos_lista_comum):.20f}")

    df_buscas = pd.DataFrame(buscas)
    df_buscas.to_csv(f"resultados/tempos_busca_{numero_registros}.csv", index=False)
    df_dados = pd.DataFrame(dados)
    df_dados.to_csv(f"resultados/dados_gerais_{numero_registros}.csv", index=False)
