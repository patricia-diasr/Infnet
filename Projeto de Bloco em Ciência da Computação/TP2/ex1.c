#include <stdio.h>
#include <omp.h>

#define NUM_PASSOS 100000000


/*
 * Calcula o valor de pi usando integração numérica pelo método dos retângulos
 */
int main() {
    long i;
    double passo;
    double x;
    double sum;
    double pi;
    double t_inicio;
    double t_fim;
    int num_threads;

    passo = 1.0 / (double) NUM_PASSOS;
    sum = 0.0;
    t_inicio = omp_get_wtime();

    #pragma omp parallel for reduction(+:sum) private(x)
    for (i = 0; i < NUM_PASSOS; i++) {
        x = (i + 0.5) * passo;
        sum += 4.0 / (1.0 + x * x);
    }

    pi = sum * passo;
    t_fim = omp_get_wtime();

    #pragma omp parallel 
    {
        #pragma omp single
        num_threads = omp_get_num_threads();
    }

    printf("\n===== Calculo de Pi por Integracao Numerica =====\n\n");
    printf("Numero de passos: %d\n",  NUM_PASSOS);
    printf("Numero de threads: %d\n",  num_threads);
    printf("Pi aproximado: %.15f\n", pi);
    printf("Pi referencia: 3.141592653589793\n");
    printf("Erro absoluto: %.2e\n", pi - 3.14159265358979323846);
    printf("Tempo de execucao: %.4f segundos\n\n", t_fim - t_inicio);

    return 0;
}
