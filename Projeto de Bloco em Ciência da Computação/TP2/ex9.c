#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define LINHAS       10000
#define COLUNAS      10000
#define BRILHO       50
#define VALOR_MAX    255


/*
 * Aloca dinamicamente uma matriz de inteiros com dimensoes LINHAS x COLUNAS
 *
 * Returns:
 *   int**: Ponteiro para a matriz alocada
 */
int **alocar_matriz() {
    int i;
    int **matriz = (int **) malloc(LINHAS * sizeof(int *));

    for (i = 0; i < LINHAS; i++) {
        matriz[i] = (int *) malloc(COLUNAS * sizeof(int));
    }

    return matriz;
}


/*
 * Libera a memoria de uma matriz alocada dinamicamente
 *
 * Args:
 *   matriz (int**): Ponteiro para a matriz a ser liberada
 */
void liberar_matriz(int **matriz) {
    int i;

    for (i = 0; i < LINHAS; i++) {
        free(matriz[i]);
    }

    free(matriz);
}


/*
 * Preenche a matriz com valores aleatorios no intervalo [0, 255]
 *
 * Args:
 *   matriz (int**): Matriz a ser preenchida
 */
void preencher_matriz(int **matriz) {
    int i, j;

    for (i = 0; i < LINHAS; i++) {
        for (j = 0; j < COLUNAS; j++) {
            matriz[i][j] = rand() % (VALOR_MAX + 1);
        }
    }
}


/*
 * Aplica ajuste de brilho em cada pixel de forma sequencial
 *
 * Args:
 *   matriz (int**): Matriz de pixels a ser ajustada
 */
void ajustar_brilho_sequencial(int **matriz) {
    int i, j;

    for (i = 0; i < LINHAS; i++) {
        for (j = 0; j < COLUNAS; j++) {
            matriz[i][j] += BRILHO;

            if (matriz[i][j] > VALOR_MAX) {
                matriz[i][j] = VALOR_MAX;
            }
        }
    }
}


/*
 * Aplica ajuste de brilho em cada pixel usando OpenMP para paralelizar o loop externo
 *
 * Args:
 *   matriz (int**): Matriz de pixels a ser ajustada
 */
void ajustar_brilho_paralelo(int **matriz) {
    int i, j;

    #pragma omp parallel for shared(matriz) private(i, j)
    for (i = 0; i < LINHAS; i++) {
        for (j = 0; j < COLUNAS; j++) {
            matriz[i][j] += BRILHO;

            if (matriz[i][j] > VALOR_MAX) {
                matriz[i][j] = VALOR_MAX;
            }
        }
    }
}


/*
 * Calcula a soma total dos pixels da matriz para fins de verificacao
 *
 * Args:
 *   matriz (int**): Matriz a ser somada
 *
 * Returns:
 *   long long: Soma de todos os elementos
 */
long long somar_pixels(int **matriz) {
    int i, j;
    long long soma = 0;

    for (i = 0; i < LINHAS; i++) {
        for (j = 0; j < COLUNAS; j++) {
            soma += matriz[i][j];
        }
    }

    return soma;
}


int main() {
    int num_threads;
    double t_inicio, t_fim;
    double tempo_seq, tempo_par;
    long long soma_seq, soma_par;
    int **matriz;

    printf("\n===== Ajuste de Brilho com OpenMP =====\n\n");
    printf("Dimensoes da matriz: %d x %d pixels\n", LINHAS, COLUNAS);
    printf("Valor de brilho: +%d\n", BRILHO);
    printf("Total de pixels: %lld\n\n", (long long) LINHAS * COLUNAS);

    #pragma omp parallel 
    {
        #pragma omp single
        num_threads = omp_get_num_threads();
    }

    printf("Threads disponiveis: %d\n\n", num_threads);


    printf("---- Execucao Sequencial ----\n\n");

    matriz = alocar_matriz();
    preencher_matriz(matriz);

    t_inicio = omp_get_wtime();
    ajustar_brilho_sequencial(matriz);
    t_fim = omp_get_wtime();
    tempo_seq = t_fim - t_inicio;
    soma_seq = somar_pixels(matriz);

    printf("Soma dos pixels: %lld\n", soma_seq);
    printf("Tempo sequencial: %.4f segundos\n\n", tempo_seq);

    liberar_matriz(matriz);


    printf("---- Execucao Paralela (%d threads) ----\n\n", num_threads);

    matriz = alocar_matriz();
    preencher_matriz(matriz);

    t_inicio = omp_get_wtime();
    ajustar_brilho_paralelo(matriz);
    t_fim = omp_get_wtime();
    tempo_par = t_fim - t_inicio;
    soma_par = somar_pixels(matriz);

    printf("Soma dos pixels: %lld\n", soma_par);
    printf("Tempo paralelo: %.4f segundos\n\n", tempo_par);

    liberar_matriz(matriz);

    printf("---- Comparativo ----\n\n");
    printf("Speedup obtido: %.2fx\n", tempo_seq / tempo_par);
    printf("Reducao de tempo: %.1f%%\n\n", (1.0 - tempo_par / tempo_seq) * 100.0);

    return 0;
}
