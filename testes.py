from grafo import Graph, gerar_entrada_aleatoria, testar_algoritmos

def exibir_resultados(resultados, nome_arquivo):
    print(f"\nResultados para: {nome_arquivo}")
    for algoritmo, (ordem, tempo_medio) in resultados.items():
        print(f"Algoritmo: {algoritmo}")
        print(f"Tempo: {tempo_medio:.8f} segundos")
        print("-" * 40)

def main():
    arquivos = [
        'entrada_pequena.txt',
        'entrada_media.txt',
        'entrada_grande.txt',
        'entrada_muito_grande.txt',
        'entrada_gigante.txt',
        'entrada_aleatoria.txt'
    ]

    # Gerar grafo aleatório de teste
    gerar_entrada_aleatoria('entrada_aleatoria.txt')

    for arquivo in arquivos:
        grafo = Graph()
        try:
            grafo.load_from_file(arquivo)
            print(f"Executando testes em {arquivo}...")
            resultados = testar_algoritmos(grafo, repeticoes=100)
            exibir_resultados(resultados, arquivo)
        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo}: {e}")
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()
