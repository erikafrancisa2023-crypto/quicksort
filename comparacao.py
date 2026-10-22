import random
import time
import statistics
import csv
import matplotlib.pyplot as plt


def insercao(lista):
    for i in range(1, len(lista)):
        valor = lista[i]
        j = i - 1

        while j >= 0 and lista[j] > valor:
            lista[j + 1] = lista[j]
            j = j - 1

        lista[j + 1] = valor

    return lista


def quicksort(lista):
    if len(lista) <= 1:
        return lista

    pivo = random.choice(lista)

    menores = []
    iguais = []
    maiores = []

    for valor in lista:
        if valor < pivo:
            menores.append(valor)
        elif valor == pivo:
            iguais.append(valor)
        else:
            maiores.append(valor)

    menores = quicksort(menores)
    maiores = quicksort(maiores)

    return menores + iguais + maiores


def quicksort_hibrida(lista, corte):
    if len(lista) <= 1:
        return lista

    if len(lista) < corte:
        return insercao(lista)

    pivo = random.choice(lista)

    menores = []
    iguais = []
    maiores = []

    for valor in lista:
        if valor < pivo:
            menores.append(valor)
        elif valor == pivo:
            iguais.append(valor)
        else:
            maiores.append(valor)

    menores = quicksort_hibrida(menores, corte)
    maiores = quicksort_hibrida(maiores, corte)

    return menores + iguais + maiores


def medir_tempo(lista_original, corte, hibrida=True):
    tempos = []

    for i in range(3):
        lista = lista_original.copy()

        random.seed(42)

        inicio = time.perf_counter()

        if hibrida:
            resultado = quicksort_hibrida(lista, corte)
        else:
            resultado = quicksort(lista)

        fim = time.perf_counter()

        if resultado != sorted(lista_original):
            print("Erro: lista não ordenada corretamente!")
            return None

        if i > 0:
            tempos.append(fim - inicio)

    return statistics.median(tempos)


random.seed(42)

dados = []

for i in range(20000):
    dados.append(random.randint(0, 100000))


cortes = [1, 5, 10, 16, 20, 32, 50, 100, 200]

resultados = []

print("TEMPOS DA QUICKSORT HÍBRIDA")
print()

for corte in cortes:
    tempo = medir_tempo(dados, corte)

    resultados.append((corte, tempo))

    print("Corte:", corte, "-", round(tempo, 6), "segundos")


tempo_puro = medir_tempo(dados, 1, False)

print()
print("Quicksort pura:", round(tempo_puro, 6), "segundos")


arquivo = open("tempos.csv", "w", newline="", encoding="utf-8")
escritor = csv.writer(arquivo)

escritor.writerow(["corte", "tempo_segundos"])

for corte, tempo in resultados:
    escritor.writerow([corte, tempo])

escritor.writerow(["Quicksort pura", tempo_puro])

arquivo.close()


melhor_corte = resultados[0][0]
melhor_tempo = resultados[0][1]

for corte, tempo in resultados:
    if tempo < melhor_tempo:
        melhor_corte = corte
        melhor_tempo = tempo

ganho = ((tempo_puro - melhor_tempo) / tempo_puro) * 100

print()
print("Melhor corte:", melhor_corte)
print("Melhor tempo:", round(melhor_tempo, 6), "segundos")
print("Ganho sobre a Quicksort pura:", round(ganho, 2), "%")


cortes_grafico = []
tempos_grafico = []

for corte, tempo in resultados:
    cortes_grafico.append(corte)
    tempos_grafico.append(tempo)

plt.plot(cortes_grafico, tempos_grafico, marker="o",
         label="Quicksort híbrida")

plt.axhline(y=tempo_puro, linestyle="--",
            label="Quicksort pura")

plt.xlabel("Valor do corte")
plt.ylabel("Tempo em segundos")
plt.title("Comparação dos tempos de ordenação")
plt.legend()
plt.grid(True)

plt.savefig("grafico_cortes.png")
plt.show()
