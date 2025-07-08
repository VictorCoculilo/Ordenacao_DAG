import time
from grafo import Graph, testar_algoritmos

def exibir_resultados(resultados, nome_arquivo):
    print(nome_arquivo)
    for algoritmo, (ordem, tempo) in resultados.items():
        print(f"Algoritmo: {algoritmo}")
        print(f"Tempo: {tempo:.6f} segundos")
        print("-" * 40)

def main():
    arquivos = ['entrada_pequena.txt', 'entrada_media.txt', 'entrada_grande.txt', 'entrada_muito_grande.txt', 'entrada_gigante.txt']

    for arquivo in arquivos:
        grafo = Graph()
        try:
            grafo.load_from_file(arquivo)  
            resultados = testar_algoritmos(grafo)  
            exibir_resultados(resultados, arquivo) 
        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo}: {e}")
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()
