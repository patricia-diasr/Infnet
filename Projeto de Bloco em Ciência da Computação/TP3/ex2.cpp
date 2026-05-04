#include <algorithm>
#include <atomic>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory>
#include <numeric>
#include <queue>
#include <random>
#include <string>
#include <vector>
#include <cstdio>
#include <omp.h>


static constexpr size_t TAMANHO_BUFFER_IO = 1 << 16;
static std::atomic<int> contador_global{0};


/**
 * Gera um nome unico para arquivo temporario com base em um prefixo e um contador atomico global
 *
 * @param prefixo: Prefixo textual para identificar o tipo de arquivo temporario (ex: "run", "merge")
 * @return Caminho completo do arquivo temporario no diretorio /tmp
 */
std::string nome_temporario(const std::string& prefixo) {
    int id = contador_global.fetch_add(1, std::memory_order_relaxed);
    return "/tmp/kwaymerge_" + prefixo + "_" + std::to_string(id) + ".bin";
}


/**
 * Serializa um vetor de inteiros em um arquivo binario
 *
 * @param caminho: Caminho do arquivo de saida a ser criado ou sobrescrito
 * @param dados: Vetor de inteiros a ser escrito no arquivo
 */
void escrever_binario(const std::string& caminho, const std::vector<int>& dados) {
    std::ofstream f(caminho, std::ios::binary);
    f.write(reinterpret_cast<const char*>(dados.data()), static_cast<std::streamsize>(dados.size() * sizeof(int)));
}


/**
 * Deserializa um arquivo binario em um vetor de inteiros
 *
 * @param caminho: Caminho do arquivo binario a ser lido
 * @return Vetor de inteiros contendo todos os elementos lidos do arquivo
 */
std::vector<int> ler_binario(const std::string& caminho) {
    std::ifstream f(caminho, std::ios::binary | std::ios::ate);
    std::streamsize bytes = f.tellg();
    f.seekg(0);
    std::vector<int> dados(static_cast<size_t>(bytes) / sizeof(int));

    if (!dados.empty()) {
        f.read(reinterpret_cast<char*>(dados.data()), bytes);
    }

    return dados;
}


/**
 * Buffer de leitura com cache interno para reducao de chamadas de I/O em arquivos binarios
 *
 * Attributes:
 *   arquivo: Fluxo de entrada do arquivo binario
 *   buffer: Bloco de memoria usado como cache de leitura
 *   pos_buffer: Posicao atual de leitura dentro do buffer
 *   elementos_no_buffer: Quantidade de elementos validos carregados no buffer
 *   fim: Indica se o arquivo foi completamente consumido
 */
struct BufferLeitura {
    std::ifstream arquivo;
    std::vector<int> buffer;
    size_t pos_buffer{0};
    size_t elementos_no_buffer{0};
    bool fim{false};

    /**
     * Constroi o BufferLeitura abrindo o arquivo e realizando a carga inicial do buffer
     *
     * @param caminho: Caminho do arquivo binario a ser lido
     */
    explicit BufferLeitura(const std::string& caminho): buffer(TAMANHO_BUFFER_IO / sizeof(int), 0) {
        arquivo.open(caminho, std::ios::binary);
        carregar();
    }

    /**
     * Carrega o proximo bloco de dados do arquivo para o buffer interno, define fim como true se nenhum dado adicional estiver disponivel
     */
    void carregar() {
        arquivo.read(reinterpret_cast<char*>(buffer.data()), static_cast<std::streamsize>(buffer.size() * sizeof(int)));
        elementos_no_buffer = static_cast<size_t>(arquivo.gcount()) / sizeof(int);
        pos_buffer = 0;

        if (elementos_no_buffer == 0) {
            fim = true;
        }
    }

    /**
     * Retorna o proximo inteiro disponivel no buffer, recarregando-o se necessario
     *
     * @param v: Referencia onde o valor lido sera armazenado
     * @return true se um valor foi lido com sucesso, false se o arquivo foi esgotado
     */
    bool proximo(int& v) {
        if (fim) {
            return false;
        }

        if (pos_buffer >= elementos_no_buffer) {
            carregar();
            if (fim) {
                return false;
            }
        }

        v = buffer[pos_buffer++];
        return true;
    }
};


/**
 * Buffer de escrita com cache interno para reducao de chamadas de I/O em arquivos binarios
 *
 * Attributes:
 *   arquivo: Fluxo de saida do arquivo binario
 *   buffer: Bloco de memoria usado como cache de escrita
 *   pos: Posicao atual de insercao dentro do buffer
 */
struct BufferEscrita {
    std::ofstream arquivo;
    std::vector<int> buffer;
    size_t pos{0};

    /**
     * Constroi o BufferEscrita abrindo o arquivo de saida para escrita binaria
     *
     * @param caminho: Caminho do arquivo binario a ser criado ou sobrescrito
     */
    explicit BufferEscrita(const std::string& caminho): buffer(TAMANHO_BUFFER_IO / sizeof(int), 0) {
        arquivo.open(caminho, std::ios::binary);
    }

    /**
     * Insere um inteiro no buffer, descarregando-o automaticamente ao atingir a capacidade maxima
     *
     * @param v: Valor inteiro a ser escrito
     */
    void escrever(int v) {
        buffer[pos++] = v;

        if (pos == buffer.size()) {
            descarregar();
        }
    }

    /**
     * Persiste o conteudo atual do buffer no arquivo e reinicia o ponteiro de posicao. Nao realiza nenhuma operacao se o buffer estiver vazio
     */
    void descarregar() {
        if (pos == 0) {
            return;
        }

        arquivo.write(reinterpret_cast<const char*>(buffer.data()), static_cast<std::streamsize>(pos * sizeof(int)));
        pos = 0;
    }

    /**
     * Destrutor que garante o descarregamento de quaisquer dados residuais no buffer antes do fechamento
     */
    ~BufferEscrita() {
        descarregar();
    }
};


/**
 * Realiza o merge de dois arquivos binarios ordenados em um unico arquivo de saida tambem ordenado
 *
 * @param esq: Caminho do arquivo binario contendo a sequencia ordenada da esquerda
 * @param dir: Caminho do arquivo binario contendo a sequencia ordenada da direita
 * @param saida: Caminho do arquivo binario de saida com o resultado do merge
 */
void merge_arquivos(const std::string& esq, const std::string& dir, const std::string& saida) {
    std::vector<int> a = ler_binario(esq);
    std::vector<int> b = ler_binario(dir);
    std::vector<int> resultado(a.size() + b.size());

    std::merge(a.begin(), a.end(), b.begin(), b.end(),resultado.begin());
    escrever_binario(saida, resultado);
}


/**
 * Realiza o k-way merge sequencial de multiplos arquivos ordenados usando um heap minimo
 *
 * @param arquivos: Vetor com os caminhos dos arquivos binarios ordenados a serem mesclados
 * @param saida: Caminho do arquivo binario de saida com todos os elementos em ordem
 */
void kway_merge_sequencial(const std::vector<std::string>& arquivos, const std::string& saida) {
    using Par = std::pair<int, int>;

    std::priority_queue<Par, std::vector<Par>, std::greater<Par>> heap;
    std::vector<std::unique_ptr<BufferLeitura>> leitores;
    leitores.reserve(arquivos.size());

    for (int i = 0; i < static_cast<int>(arquivos.size()); ++i) {
        leitores.emplace_back(std::make_unique<BufferLeitura>(arquivos[i]));

        int v = 0;
        if (leitores.back()->proximo(v)) {
            heap.push({v, i});
        }
    }

    BufferEscrita bw(saida);

    while (!heap.empty()) {
        auto [valor, idx] = heap.top();
        heap.pop();
        bw.escrever(valor);

        int v = 0;
        if (leitores[idx]->proximo(v)) {
            heap.push({v, idx});
        }
    }
}


/**
 * Estrutura que representa o resultado de uma operacao de merge
 *
 * Attributes:
 *   arquivo: Caminho do arquivo final contendo o resultado mesclado
 *   temporarios: Lista de caminhos de arquivos intermediarios gerados durante o processo, a serem removidos apos a conclusao do merge
 */
struct ResultadoMerge {
    std::string arquivo;
    std::vector<std::string> temporarios;
};


/**
 * Realiza o merge em arvore de forma recursiva e paralela sobre um subintervalo de arquivos
 *
 * @param arqs: Vetor com os caminhos de todos os arquivos ordenados a serem mesclados
 * @param ini: Indice inicial do subintervalo a processar (inclusivo)
 * @param fim: Indice final do subintervalo a processar (inclusivo)
 * @return ResultadoMerge contendo o arquivo mesclado e a lista de temporarios gerados
 */
ResultadoMerge merge_tree_recursivo(const std::vector<std::string>& arqs, int ini, int fim) {
    if (ini == fim) {
        return { arqs[ini], {} };
    }

    int meio = (ini + fim) / 2;
    ResultadoMerge esq;
    ResultadoMerge dir;

    #pragma omp task shared(esq) firstprivate(ini, meio) shared(arqs)
    {
        esq = merge_tree_recursivo(arqs, ini, meio);
    }

    #pragma omp task shared(dir) firstprivate(meio, fim) shared(arqs)
    {
        dir = merge_tree_recursivo(arqs, meio + 1, fim);
    }

    #pragma omp taskwait
    std::string saida = nome_temporario("merge");
    merge_arquivos(esq.arquivo, dir.arquivo, saida);

    ResultadoMerge r;
    r.arquivo = saida;

    r.temporarios.insert(r.temporarios.end(), esq.temporarios.begin(), esq.temporarios.end());
    r.temporarios.insert(r.temporarios.end(), dir.temporarios.begin(), dir.temporarios.end());

    if (ini != meio) {
        r.temporarios.push_back(esq.arquivo);
    }

    if (meio + 1 != fim) {
        r.temporarios.push_back(dir.arquivo);
    }

    return r;
}


/**
 * Ponto de entrada para o k-way merge paralelo baseado em arvore de merge com OpenMP
 *
 * @param arqs: Vetor com os caminhos dos arquivos binarios ordenados a serem mesclados
 * @param nt: Numero de threads OpenMP a utilizar
 * @return Caminho do arquivo binario final contendo todos os elementos em ordem
 */
std::string kway_merge_paralelo(const std::vector<std::string>& arqs, int nt) {
    ResultadoMerge resultado;

    #pragma omp parallel num_threads(nt)
    {
        #pragma omp single
        {
            resultado = merge_tree_recursivo(arqs, 0, static_cast<int>(arqs.size()) - 1);
        }
    }

    for (const auto& t: resultado.temporarios) {
        std::remove(t.c_str());
    }

    return resultado.arquivo;
}


/**
 * Divide um vetor de inteiros em k particoes, ordena cada uma e as persiste em arquivos binarios temporarios
 *
 * @param dados: Vetor de inteiros de entrada a ser particionado
 * @param k: Numero de particoes (runs) a gerar
 * @return Vetor com os caminhos dos arquivos binarios gerados, um por particao ordenada
 */
std::vector<std::string> gerar_runs(const std::vector<int>& dados, int k) {
    std::vector<std::string> arquivos;
    arquivos.reserve(static_cast<size_t>(k));

    size_t total = dados.size();
    size_t tam = (total + static_cast<size_t>(k) - 1) / static_cast<size_t>(k);

    for (int i = 0; i < k; ++i) {
        size_t ini = static_cast<size_t>(i) * tam;
        size_t fim = std::min(ini + tam, total);

        if (ini >= total) {
            break;
        }

        std::vector<int> run(dados.begin() + static_cast<long>(ini), dados.begin() + static_cast<long>(fim));
        std::sort(run.begin(), run.end());
        std::string p = nome_temporario("run");

        escrever_binario(p, run);
        arquivos.push_back(p);
    }

    return arquivos;
}


/**
 * Verifica se o conteudo de um arquivo binario esta em ordem nao decrescente
 *
 * @param caminho: Caminho do arquivo binario a ser verificado
 * @return true se os elementos estiverem ordenados, false caso contrario
 */
bool verificar_ordenado(const std::string& caminho) {
    auto d = ler_binario(caminho);
    return std::is_sorted(d.begin(), d.end());
}


/**
 * Verifica se o conteudo de um arquivo binario e uma permutacao ordenada do vetor original
 *
 * @param original: Vetor de inteiros original antes do merge
 * @param caminho: Caminho do arquivo binario com o resultado do merge a ser verificado
 * @return true se os conteudos forem identicos apos ordenacao, false caso contrario
 */
bool verificar_conteudo_igual(const std::vector<int>& original, const std::string& caminho) {
    auto res = ler_binario(caminho);

    if (res.size() != original.size())
        return false;

    auto copia = original;
    std::sort(copia.begin(), copia.end());

    return res == copia;
}


/**
 * Estrutura que agrega os resultados de um cenario de benchmark entre as versoes sequencial e paralela
 *
 * Attributes:
 *   ts: Tempo de execucao da versao sequencial em segundos
 *   tp: Tempo de execucao da versao paralela em segundos
 *   speedup: Razao ts/tp indicando o ganho de desempenho da versao paralela
 *   cs: Indica se o resultado sequencial passou na verificacao de corretude
 *   cp: Indica se o resultado paralelo passou na verificacao de corretude
 */
struct ResultadoTeste {
    double ts;
    double tp;
    double speedup;
    bool cs;
    bool cp;
};


/**
 * Executa um cenario completo de benchmark gerando dados aleatorios, realizando o merge nas versoes sequencial e paralela e verificando a corretude de ambos os resultados
 *
 * @param n: Quantidade total de elementos a gerar e ordenar
 * @param k: Numero de runs (particoes) a dividir os dados antes do merge
 * @param nt: Numero de threads OpenMP para a versao paralela
 * @return ResultadoTeste com os tempos, speedup e flags de corretude de ambas as versoes
 */
ResultadoTeste executar_cenario(int n, int k, int nt) {
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, n * 10);
    std::vector<int> dados(n);

    std::generate(dados.begin(), dados.end(),[&] { return dist(rng); });
    auto runs_s = gerar_runs(dados, k);
    auto runs_p = gerar_runs(dados, k);
    std::string out_s = nome_temporario("seq");

    double t0s = omp_get_wtime();
    kway_merge_sequencial(runs_s, out_s);
    double ts = omp_get_wtime() - t0s;

    double t0p = omp_get_wtime();
    std::string out_p = kway_merge_paralelo(runs_p, nt);
    double tp = omp_get_wtime() - t0p;

    bool cs = verificar_ordenado(out_s) && verificar_conteudo_igual(dados, out_s);

    bool cp = verificar_ordenado(out_p) && verificar_conteudo_igual(dados, out_p);

    std::remove(out_s.c_str());
    std::remove(out_p.c_str());

    return { ts, tp, ts / tp, cs, cp };
}


int main() {
    int nt = omp_get_max_threads();

    std::cout << "\n===== K-Way Merge Paralelo (Merge Tree + OpenMP) =====\n";
    std::cout << "Threads disponiveis: " << nt << "\n";
    std::cout << "Buffer de I/O: " << TAMANHO_BUFFER_IO / 1024 << " KB\n";
    
    std::cout << "\n\n===== Teste 1 - Corretude com Dataset Pequeno =====\n\n";
    std::vector<int> pequeno = {9,3,7,1,5,2,8,4,6,0,15,11,13,10,12,14,19,16,18,17};
    auto rsp = gerar_runs(pequeno, 4);
    auto rpp = gerar_runs(pequeno, 4);
    std::string ssp = nome_temporario("pequeno_seq");
    kway_merge_sequencial(rsp, ssp);
    std::string spp = kway_merge_paralelo(rpp, nt);
    auto rs = ler_binario(ssp);
    auto rp = ler_binario(spp);

    std::cout << "Entrada: ";
    for (int v: pequeno) {
        std::cout << v << " ";
    }

    std::cout << "\nSeq.: ";
    for (int v: rs) {
        std::cout << v << " ";
    }

    std::cout << "\nPar.: ";
    for (int v: rp) {
        std::cout << v << " ";
    }

    std::cout << "\nCorretude seq: "
    << (std::is_sorted(rs.begin(), rs.end()) ? "OK" : "FALHA")
    << "  par: "
    << (std::is_sorted(rp.begin(), rp.end()) ? "OK" : "FALHA")
    << "\n";

    std::remove(ssp.c_str());
    std::remove(spp.c_str());
    
    std::cout << "\n\n===== Teste 2 - Comparacao Sequencial vs Paralelo =====\n\n";

    struct Cen {
        std::string nome;
        int n;
        int k;
    };

    std::vector<Cen> cenarios = {
        {"Pequeno", 100000, 8},
        {"Medio", 500000, 16},
        {"Grande", 2000000, 16},
        {"K alto", 500000, 32}
    };

    std::cout << std::left
    << std::setw(10) << "Cenario"
    << std::setw(10) << "N"
    << std::setw(6) << "K"
    << std::setw(12) << "Seq (ms)"
    << std::setw(12) << "Par (ms)"
    << std::setw(10) << "Speedup"
    << std::setw(8) << "Seq OK"
    << std::setw(8) << "Par OK"
    << "\n";

    std::cout << std::string(76, '-') << "\n";

    for (const auto& c: cenarios) {
        auto r = executar_cenario(c.n, c.k, nt);

        std::cout << std::left
        << std::setw(10) << c.nome
        << std::setw(10) << c.n
        << std::setw(6) << c.k
        << std::setw(12) << std::fixed << std::setprecision(2)
        << r.ts * 1000
        << std::setw(12) << r.tp * 1000
        << std::setw(10) << r.speedup
        << std::setw(8) << (r.cs ? "OK" : "FALHA")
        << std::setw(8) << (r.cp ? "OK" : "FALHA")
        << "\n";
    }

    std::cout << "\n\n===== Teste 3 - Impacto do Numero de Threads (N=1M, K=16) =====\n\n";
    int nf = 1'000'000;
    int kf = 16;

    std::mt19937 rng2(99);
    std::uniform_int_distribution<int> dist2(0, nf * 10);
    std::vector<int> dados_base(nf);
    std::generate(dados_base.begin(), dados_base.end(), [&] { return dist2(rng2); });

    auto runs_base = gerar_runs(dados_base, kf);
    std::string out_base = nome_temporario("baseline");
    double t0 = omp_get_wtime();
    kway_merge_sequencial(runs_base, out_base);
    double tempo_base = omp_get_wtime() - t0;

    std::remove(out_base.c_str());
    std::cout << std::left
    << std::setw(10) << "Threads"
    << std::setw(14) << "Tempo (ms)"
    << std::setw(10) << "Speedup"
    << std::setw(14) << "Corretude"
    << "\n";

    std::cout << std::string(48, '-') << "\n";
    std::cout << std::setw(10) << 1
    << std::setw(14) << std::fixed << std::setprecision(2)
    << tempo_base * 1000
    << std::setw(10) << "1.00"
    << std::setw(14) << "OK (baseline)"
    << "\n";

    std::vector<int> threads_teste = {2, 4};

    if (nt > 4) {
        threads_teste.push_back(nt);
    }

    std::sort(threads_teste.begin(), threads_teste.end());
    threads_teste.erase(std::unique(threads_teste.begin(), threads_teste.end()), threads_teste.end());

    for (int t: threads_teste) {
        if (t > nt) {
            continue;
        }

        auto runs_t = gerar_runs(dados_base, kf);
        double ti = omp_get_wtime();
        std::string out_t = kway_merge_paralelo(runs_t, t);
        double tp = omp_get_wtime() - ti;
        bool ok = verificar_ordenado(out_t) && verificar_conteudo_igual(dados_base, out_t);

        std::cout << std::setw(10) << t
        << std::setw(14) << tp * 1000
        << std::setw(10) << std::setprecision(2)
        << tempo_base / tp
        << std::setw(14) << (ok ? "OK" : "FALHA")
        << "\n";
        std::remove(out_t.c_str());
    }

    return 0;
}