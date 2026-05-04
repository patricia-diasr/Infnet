#include <algorithm>
#include <atomic>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <memory>
#include <mutex>
#include <numeric>
#include <random>
#include <vector>
#include <omp.h>


static constexpr int CAPACIDADE_NO = 50;
static constexpr int CUTOFF_TASK = 500;
static constexpr int PROFUNDIDADE_PRESPLIT = 3;
static constexpr double ESPACO_MIN = 0.0;
static constexpr double ESPACO_MAX = 1000.0;
static constexpr int N_PARTICULAS = 100'000;
static constexpr size_t ALINHAMENTO_CACHE = 64;


/**
 * Representa uma particula no espaco 2D com posicao e identificador unico. Alinhada ao tamanho da linha de cache para evitar false sharing em acessos paralelos
 *
 * Attributes:
 *   x: Coordenada horizontal da particula
 *   y: Coordenada vertical da particula
 *   id: Identificador unico da particula
 */
struct alignas(ALINHAMENTO_CACHE) Particula {
    double x;
    double y;
    int id;
};


/**
 * Define uma regiao retangular do espaco 2D e fornece operacoes geometricas sobre ela
 *
 * Attributes:
 *   x_min: Limite esquerdo da regiao
 *   x_max: Limite direito da regiao
 *   y_min: Limite inferior da regiao
 *   y_max: Limite superior da regiao
 */
struct Regiao {
    double x_min, x_max;
    double y_min, y_max;

    /**
     * Calcula a coordenada x do centro da regiao
     *
     * @return Valor medio entre x_min e x_max
     */
    double cx() const { 
        return (x_min + x_max) * 0.5; 
    }
    
    /**
     * Calcula a coordenada y do centro da regiao
     *
     * @return: Valor medio entre y_min e y_max
     */
    double cy() const { 
        return (y_min + y_max) * 0.5; 
    }

    /**
     * Verifica se uma particula esta contida dentro dos limites da regiao
     *
     * @param p: Particula a ser testada
     * @return true se a particula estiver dentro da regiao, false caso contrario
     */
    bool contem(const Particula& p) const {
        return p.x >= x_min && p.x < x_max && p.y >= y_min && p.y < y_max;
    }

    /**
     * Verifica se a regiao intercepta um circulo definido por centro e raio. Utiliza a projecao do centro do circulo sobre o retangulo para calcular a distancia minima
     *
     * @param cx_: Coordenada x do centro do circulo
     * @param cy_: Coordenada y do centro do circulo
     * @param raio: Raio do circulo
     * @return true se houver qualquer intersecao entre a regiao e o circulo
     */
    bool intercepta_circulo(double cx_, double cy_, double raio) const {
        double dx = std::max(x_min, std::min(cx_, x_max)) - cx_;
        double dy = std::max(y_min, std::min(cy_, y_max)) - cy_;
        return (dx * dx + dy * dy) <= (raio * raio);
    }

    /**
     * Verifica se a regiao esta completamente contida dentro de um circulo
     * 
     * @param cx_: Coordenada x do centro do circulo
     * @param cy_: Coordenada y do centro do circulo
     * @param raio: Raio do circulo
     * @return true se todos os vertices da regiao estiverem dentro do circulo
     */
    bool dentro_circulo(double cx_, double cy_, double raio) const {
        double r2 = raio * raio;

        auto d2 = [&](double px, double py) {
            return (px - cx_) * (px - cx_) + (py - cy_) * (py - cy_);
        };
        
        return d2(x_min, y_min) <= r2 && d2(x_max, y_min) <= r2 && d2(x_min, y_max) <= r2 && d2(x_max, y_max) <= r2;
    }
};


struct NoQuadtree;


/**
 * Pool de nos pre-alocados para a Quadtree, reduzindo fragmentacao de memoria e overhead de alocacao dinamica
 *
 * Attributes:
 *   bloco: Vetor contiguo de nos pre-alocados
 *   proximo: Indice atomico do proximo no livre, seguro para uso em contexto paralelo
 */
struct PoolMemoria {
    std::vector<NoQuadtree> bloco;
    std::atomic<int> proximo{0};

    explicit PoolMemoria(int capacidade): bloco(capacidade) {}
    NoQuadtree* alocar();
};


/**
 * No interno da Quadtree, representando uma regiao do espaco com seus indices de particulas e filhos
 *
 * Attributes:
 *   regiao: Regiao espacial coberta por este no
 *   indices: Indices das particulas contidas neste no (valido apenas em nos folha)
 *   filhos: Ponteiros para os quatro filhos (NW, NE, SW, SE), nulos se nao subdividido
 *   subdividido: Indica se este no foi subdividido em quatro quadrantes filhos
 *   mtx: Mutex para proteger insercoes concorrentes neste no
 */
struct alignas(ALINHAMENTO_CACHE) NoQuadtree {
    Regiao regiao;
    std::vector<int> indices;
    NoQuadtree* filhos[4]{};
    bool subdividido{false};
    std::mutex mtx;

    NoQuadtree() = default;
    NoQuadtree(const NoQuadtree&) = delete;
    NoQuadtree& operator=(const NoQuadtree&) = delete;

    /**
     * Verifica se este no e uma folha, ou seja, nao foi subdividido
     *
     * @return true se o no for folha, false se possuir filhos
     */
    bool e_folha() const { 
        return !subdividido; 
    }

    /**
     * Reinicializa o no com uma nova regiao, limpando indices, filhos e o estado de subdivisao
     *
     * @param r: Nova regiao espacial a ser atribuida a este no
     */
    void configurar(const Regiao& r) {
        regiao = r;
        subdividido = false;
        indices.clear();
        
        for (auto& f: filhos) {
            f = nullptr;
        }
    }
};


NoQuadtree* PoolMemoria::alocar() {
    int idx = proximo.fetch_add(1, std::memory_order_relaxed);
    return &bloco[static_cast<size_t>(idx)];
}


/**
 * Quadtree paralela para particulas 2D com suporte a construcao e consulta com OpenMP
 */
class Quadtree {
public:
    /**
     * Constroi a Quadtree alocando o pool de memoria e inicializando o no raiz
     *
     * @param n_particulas: Numero total de particulas que serao inseridas, usado para dimensionar o pool (fator 4x para nos internos)
     */
    explicit Quadtree(int n_particulas): _pool(std::make_unique<PoolMemoria>(n_particulas * 4)), _particulas(nullptr), _n(0) {
        _raiz = _pool->alocar();
        _raiz->configurar({ESPACO_MIN, ESPACO_MAX, ESPACO_MIN, ESPACO_MAX});
    }

    /**
     * Constroi a arvore inserindo todas as particulas do vetor fornecido
     *
     * @param particulas: Vetor de particulas a serem inseridas na Quadtree
     */
    void construir(const std::vector<Particula>& particulas) {
        _particulas = particulas.data();
        _n = static_cast<int>(particulas.size());

        std::vector<int> todos(_n);
        std::iota(todos.begin(), todos.end(), 0);
        _presplit(_raiz, todos, 0);

        std::vector<NoQuadtree*> folhas;
        _coletar_folhas(_raiz, folhas);

        #pragma omp parallel
        #pragma omp single
        {
            #pragma omp taskgroup
            {
                for (NoQuadtree* folha: folhas) {
                    #pragma omp task firstprivate(folha)
                    {
                        _inserir_recursivo(folha, folha->indices, 0);
                    }
                }
            }
        }
    }

    /**
     * Busca por forca bruta todos os indices de particulas dentro de um circulo
     *
     * @param cx: Coordenada x do centro do circulo de busca
     * @param cy: Coordenada y do centro do circulo de busca
     * @param raio: Raio do circulo de busca
     * @return Vetor com os indices de todas as particulas dentro do circulo
     */
    std::vector<int> buscar_vizinhos(double cx, double cy, double raio) const {
        std::vector<std::vector<int>> resultados_por_thread;
        int num_threads = 0;

        #pragma omp parallel
        {
            #pragma omp single
            {
                num_threads = omp_get_num_threads();
                resultados_por_thread.resize(num_threads);
            }

            int tid = omp_get_thread_num();

            #pragma omp for schedule(dynamic, 64)
            for (int i = 0; i < _n; ++i)
            {
                const Particula& p = _particulas[i];
                double dx = p.x - cx;
                double dy = p.y - cy;

                if (dx * dx + dy * dy <= raio * raio) {
                    resultados_por_thread[tid].push_back(i);
                }
            }
        }

        std::vector<int> resultado;
        for (auto& v: resultados_por_thread) {
            resultado.insert(resultado.end(), v.begin(), v.end());
        }

        return resultado;
    }

    /**
     * Busca por traversal da Quadtree todos os indices de particulas dentro de um circulo
     *
     * @param cx: Coordenada x do centro do circulo de busca
     * @param cy: Coordenada y do centro do circulo de busca
     * @param raio: Raio do circulo de busca
     * @return Vetor com os indices de todas as particulas dentro do circulo
     */
    std::vector<int> buscar_vizinhos_quadtree(double cx, double cy, double raio) const {
        std::vector<std::vector<int>> resultados_por_thread;
        int num_threads = 0;

        std::vector<NoQuadtree*> folhas_candidatas;
        _coletar_candidatas(_raiz, cx, cy, raio, folhas_candidatas);

        #pragma omp parallel
        {
            #pragma omp single
            {
                num_threads = omp_get_num_threads();
                resultados_por_thread.resize(num_threads);
            }

            int tid = omp_get_thread_num();

            #pragma omp for schedule(dynamic)
            for (int f = 0; f < static_cast<int>(folhas_candidatas.size()); ++f)
            {
                const NoQuadtree* folha = folhas_candidatas[f];

                if (folha->regiao.dentro_circulo(cx, cy, raio)) {
                    for (int idx: folha->indices) {
                        resultados_por_thread[tid].push_back(idx);
                    }
                }

                else {
                    for (int idx: folha->indices) {
                        const Particula& p = _particulas[idx];
                        double dx = p.x - cx;
                        double dy = p.y - cy;

                        if (dx * dx + dy * dy <= raio * raio) {
                            resultados_por_thread[tid].push_back(idx);
                        }
                    }
                }
            }
        }

        std::vector<int> resultado;
        for (auto& v: resultados_por_thread) {
            resultado.insert(resultado.end(), v.begin(), v.end());
        }

        return resultado;
    }

    /**
     * Conta o total de particulas armazenadas em todos os nos folha da arvore
     *
     * @return Numero total de particulas indexadas na Quadtree
     */
    int contar_particulas() const {
        return _contar_recursivo(_raiz);
    }

    /**
     * Retorna o numero de nos efetivamente alocados no pool de memoria
     *
     * @return Total de nos em uso, incluindo nos internos e folhas
     */
    int contar_nos() const {
        return _pool->proximo.load();
    }

    /**
     * Calcula a profundidade maxima da arvore a partir da raiz
     *
     * @return Numero de niveis de subdivisao do caminho mais longo da raiz ate uma folha
     */
    int profundidade_maxima() const {
        return _profundidade_recursiva(_raiz);
    }

private:
    /**
     * Calcula a sub-regiao correspondente a um dos quatro quadrantes de uma regiao pai
     *
     * @param r: Regiao pai a ser subdividida
     * @param filho: Indice do quadrante filho (0 a 3)
     * @return Regiao correspondente ao quadrante solicitado
     */
    static Regiao _sub_regiao(const Regiao& r, int filho) {
        double mx = r.cx();
        double my = r.cy();
        switch (filho) {
            case 0: 
                return {r.x_min, mx, my, r.y_max};
            case 1: 
                return {mx, r.x_max, my, r.y_max};
            case 2: 
                return {r.x_min, mx, r.y_min, my};
            default:
                return {mx, r.x_max, r.y_min, my};
        }
    }

    /**
     * Determina em qual quadrante de uma regiao uma particula se encontra
     *
     * @param r: Regiao a ser subdivida em quadrantes
     * @param p: Particula cuja posicao sera avaliada
     * @return Indice do quadrante (0=NW, 1=NE, 2=SW, 3=SE)
     */
    static int _quadrante(const Regiao& r, const Particula& p) {
        bool leste = p.x >= r.cx();
        bool norte = p.y >= r.cy();

        if (!leste && norte) {
            return 0;
        }

        if ( leste && norte) {
            return 1;
        }

        if (!leste && !norte) {
            return 2;
        }

        return 3;
    }

    /**
     * Subdivide um no em quatro filhos e redistribui seus indices pelos quadrantes correspondentes
     *
     * @param no: No a ser subdividido; deve ser uma folha antes da chamada
     */
    void _subdividir(NoQuadtree* no) {
        for (int q = 0; q < 4; ++q) {
            no->filhos[q] = _pool->alocar();
            no->filhos[q]->configurar(_sub_regiao(no->regiao, q));
        }

        no->subdividido = true;

        for (int idx: no->indices) {
            int q = _quadrante(no->regiao, _particulas[idx]);
            no->filhos[q]->indices.push_back(idx);
        }

        no->indices.clear();
        no->indices.shrink_to_fit();
    }

    /**
     * Realiza o pre-split deterministico da arvore ate uma profundidade limite
     *
     * @param no: No atual a ser processado
     * @param indices_entrada: Indices das particulas a serem atribuidos a este no
     * @param prof: Profundidade atual na arvore (0 na raiz)
     */
    void _presplit(NoQuadtree* no, const std::vector<int>& indices_entrada, int prof) {
        no->indices = indices_entrada;

        if (prof >= PROFUNDIDADE_PRESPLIT || static_cast<int>(indices_entrada.size()) <= CAPACIDADE_NO) {
            return;
        }

        _subdividir(no);

        for (int q = 0; q < 4; ++q) {
            _presplit(no->filhos[q], no->filhos[q]->indices, prof + 1);
        }
    }

    /**
     * Insere recursivamente um conjunto de indices a partir de um no, subdividindo quando necessario
     *
     * @param no: No atual onde os indices serao inseridos
     * @param indices: Indices das particulas a serem distribuidas a partir deste no
     * @param prof: Profundidade atual na arvore
     */
    void _inserir_recursivo(NoQuadtree* no, const std::vector<int>& indices, int prof) {
        no->indices = indices;

        if (static_cast<int>(indices.size()) <= CAPACIDADE_NO) {
            return;
        }

        _subdividir(no);

        if (static_cast<int>(indices.size()) >= CUTOFF_TASK && prof < 8) {
            #pragma omp taskgroup
            {
                for (int q = 0; q < 4; ++q) {
                    NoQuadtree* filho = no->filhos[q];

                    #pragma omp task firstprivate(filho, prof)
                    {
                        _inserir_recursivo(filho, filho->indices, prof + 1);
                    }
                }
            }
        }

        else {
            for (int q = 0; q < 4; ++q) {
                _inserir_recursivo(no->filhos[q], no->filhos[q]->indices, prof + 1);
            }
        }
    }

    /**
     * Coleta recursivamente todos os nos folha da subarvore enraizada em no
     *
     * @param no: No raiz da subarvore a percorrer
     * @param folhas: Vetor de saida onde os ponteiros para folhas serao acumulados
     */
    void _coletar_folhas(NoQuadtree* no, std::vector<NoQuadtree*>& folhas) const {
        if (!no) {
            return;
        }

        if (no->e_folha()) { 
            folhas.push_back(no); 
            return; 
        }
        
        for (int q = 0; q < 4; ++q) {
            _coletar_folhas(no->filhos[q], folhas);
        }
    }

    /**
     * Coleta recursivamente as folhas candidatas cujas regioes interceptam o circulo de consulta
     *
     * @param no: No raiz da subarvore a percorrer
     * @param cx: Coordenada x do centro do circulo de consulta
     * @param cy: Coordenada y do centro do circulo de consulta
     * @param raio: Raio do circulo de consulta
     * @param candidatas: Vetor de saida onde os ponteiros para folhas candidatas serao acumulados
     */
    void _coletar_candidatas(const NoQuadtree* no, double cx, double cy, double raio, std::vector<NoQuadtree*>& candidatas) const {
        if (!no) {
            return;
        }

        if (!no->regiao.intercepta_circulo(cx, cy, raio)) {
            return;
        }

        if (no->e_folha()) {
            candidatas.push_back(const_cast<NoQuadtree*>(no));
            return;
        }

        for (int q = 0; q < 4; ++q) {
            _coletar_candidatas(no->filhos[q], cx, cy, raio, candidatas);
        }
    }

    /**
     * Conta recursivamente o total de particulas armazenadas na subarvore enraizada em no
     *
     * @param no: No raiz da subarvore a ser contabilizada
     * @return Numero total de indices armazenados em todos os nos folha da subarvore
     */
    int _contar_recursivo(const NoQuadtree* no) const {
        if (!no) {
            return 0;
        }

        if (no->e_folha()) {
            return static_cast<int>(no->indices.size());
        }

        int total = 0;
        for (int q = 0; q < 4; ++q) {
            total += _contar_recursivo(no->filhos[q]);
        }

        return total;
    }

    /**
     * Calcula recursivamente a profundidade maxima da subarvore enraizada em no
     *
     * @param no: No raiz da subarvore a ser medida
     * @return Numero de niveis do caminho mais longo da raiz ate uma folha
     */
    int _profundidade_recursiva(const NoQuadtree* no) const {
        if (!no || no->e_folha()) {
            return 0;
        }

        int max_filho = 0;
        for (int q = 0; q < 4; ++q) {
            max_filho = std::max(max_filho, _profundidade_recursiva(no->filhos[q]));
        }

        return 1 + max_filho;
    }

    std::unique_ptr<PoolMemoria> _pool;
    NoQuadtree* _raiz;
    const Particula* _particulas;
    int _n;
};


/**
 * Gera um vetor de particulas com posicoes distribuidas uniformemente dentro de um espaco retangular
 *
 * @param n: Numero de particulas a gerar
 * @param xmin: Limite esquerdo do espaco de geracao
 * @param xmax: Limite direito do espaco de geracao
 * @param ymin: Limite inferior do espaco de geracao
 * @param ymax: Limite superior do espaco de geracao
 * @param seed: Semente para o gerador de numeros aleatorios (padrao: 42)
 * @return Vetor de n particulas com posicoes aleatorias e ids sequenciais
 */
std::vector<Particula> gerar_particulas(int n, double xmin, double xmax, double ymin, double ymax, unsigned seed = 42) {
    std::mt19937 rng(seed);
    std::uniform_real_distribution<double> dist_x(xmin, xmax);
    std::uniform_real_distribution<double> dist_y(ymin, ymax);
    std::vector<Particula> particulas(n);

    for (int i = 0; i < n; ++i) {
        particulas[i] = {dist_x(rng), dist_y(rng), i};
    }

    return particulas;
}


int main() {
    int num_threads = omp_get_max_threads();

    std::cout << "\n===== Quadtree Paralela com OpenMP =====\n";
    std::cout << "Threads disponiveis: " << num_threads << "\n";
    std::cout << "Particulas: " << N_PARTICULAS << "\n";
    std::cout << "Capacidade por no: " << CAPACIDADE_NO << "\n";
    std::cout << "Cutoff de task: " << CUTOFF_TASK << "\n";
    std::cout << "Profundidade pre-split: " << PROFUNDIDADE_PRESPLIT << "\n\n";

    auto particulas = gerar_particulas(N_PARTICULAS, ESPACO_MIN, ESPACO_MAX, ESPACO_MIN, ESPACO_MAX);
    std::cout << "\n===== Teste 1 - Construcao da Quadtree =====\n\n";

    omp_set_num_threads(1);
    Quadtree qt_seq(N_PARTICULAS);
    double t0 = omp_get_wtime();
    qt_seq.construir(particulas);
    double tempo_construcao_seq = omp_get_wtime() - t0;

    omp_set_num_threads(num_threads);
    Quadtree qt_par(N_PARTICULAS);
    t0 = omp_get_wtime();
    qt_par.construir(particulas);
    double tempo_construcao_par = omp_get_wtime() - t0;

    int total_seq = qt_seq.contar_particulas();
    int total_par = qt_par.contar_particulas();

    std::cout << std::left
    << std::setw(30) << "Metodo"
    << std::setw(14) << "Tempo (ms)"
    << std::setw(10) << "Speedup"
    << std::setw(12) << "Nos alocados"
    << std::setw(10) << "Prof. max"
    << std::setw(14) << "Particulas OK"
    << "\n";
    std::cout << std::string(90, '-') << "\n";

    std::cout << std::setw(30) << "Sequencial (1 thread)"
    << std::setw(14) << std::fixed << std::setprecision(2) << tempo_construcao_seq * 1000
    << std::setw(10) << "1.00"
    << std::setw(12) << qt_seq.contar_nos()
    << std::setw(10) << qt_seq.profundidade_maxima()
    << std::setw(14) << (total_seq == N_PARTICULAS ? "OK (" + std::to_string(total_seq) + ")" : "FALHA")
    << "\n";

    std::cout << std::setw(30) << ("Paralelo (" + std::to_string(num_threads) + " threads)")
    << std::setw(14) << tempo_construcao_par * 1000
    << std::setw(10) << std::setprecision(2) << tempo_construcao_seq / tempo_construcao_par
    << std::setw(12) << qt_par.contar_nos()
    << std::setw(10) << qt_par.profundidade_maxima()
    << std::setw(14) << (total_par == N_PARTICULAS ? "OK (" + std::to_string(total_par) + ")" : "FALHA")
    << "\n\n";

    std::cout << "\n\n===== Teste 2 - Consulta de Vizinhos (Forca Bruta vs Quadtree) =====\n\n";
    struct CasoConsulta { double cx, cy, raio; std::string descricao; };

    std::vector<CasoConsulta> consultas = {
        {500.0, 500.0, 10.0, "Centro, raio pequeno"},
        {500.0, 500.0, 50.0, "Centro, raio medio"},
        {500.0, 500.0, 100.0, "Centro, raio grande"},
        {0.0, 0.0, 20.0, "Canto NW, raio medio"},
        {999.0, 999.0, 20.0, "Canto SE, raio medio"},
        {250.0, 750.0, 75.0, "Regiao densa, raio grande"},
    };

    std::cout << std::left
    << std::setw(28) << "Consulta"
    << std::setw(8)  << "Raio"
    << std::setw(10) << "Vizinhos"
    << std::setw(14) << "Bruta (ms)"
    << std::setw(14) << "Quadtree (ms)"
    << std::setw(10) << "Speedup"
    << std::setw(8)  << "OK"
    << "\n";
    std::cout << std::string(92, '-') << "\n";

    omp_set_num_threads(num_threads);

    for (auto& c: consultas) {
        double t_bruta0 = omp_get_wtime();
        auto res_bruta = qt_par.buscar_vizinhos(c.cx, c.cy, c.raio);
        double t_bruta = omp_get_wtime() - t_bruta0;

        double t_qt0 = omp_get_wtime();
        auto res_qt = qt_par.buscar_vizinhos_quadtree(c.cx, c.cy, c.raio);
        double t_qt = omp_get_wtime() - t_qt0;

        std::sort(res_bruta.begin(), res_bruta.end());
        std::sort(res_qt.begin(), res_qt.end());
        bool correto = (res_bruta == res_qt);

        std::cout << std::setw(28) << c.descricao
        << std::setw(8)  << c.raio
        << std::setw(10) << res_bruta.size()
        << std::setw(14) << std::fixed << std::setprecision(3) << t_bruta * 1000
        << std::setw(14) << t_qt * 1000
        << std::setw(10) << std::setprecision(2) << t_bruta / t_qt
        << std::setw(8)  << (correto ? "OK" : "FALHA")
        << "\n";
    }


    std::cout << "\n\n===== Teste 3 - Impacto do Numero de Threads na Construcao =====\n\n";
    std::cout << std::left
    << std::setw(10) << "Threads"
    << std::setw(14) << "Tempo (ms)"
    << std::setw(10) << "Speedup"
    << std::setw(14) << "Particulas OK"
    << "\n";
    std::cout << std::string(48, '-') << "\n";

    double tempo_base = tempo_construcao_seq;

    for (int t: {1, 2, 4, 8, num_threads}) {
        if (t > num_threads && t != num_threads) {
            continue;
        }

        if (t == 1 && num_threads == 1) {
            continue;
        }

        omp_set_num_threads(t);
        Quadtree qt_t(N_PARTICULAS);
        double t0_t = omp_get_wtime();
        qt_t.construir(particulas);
        double tempo_t = omp_get_wtime() - t0_t;

        int contagem = qt_t.contar_particulas();
        std::cout << std::setw(10) << t
        << std::setw(14) << std::fixed << std::setprecision(2) << tempo_t * 1000
        << std::setw(10) << std::setprecision(2) << tempo_base / tempo_t
        << std::setw(14) << (contagem == N_PARTICULAS ? "OK" : "FALHA")
        << "\n";
    }


    std::cout << "\n\n===== Teste 4 - Distribuicao Nao Uniforme (Cluster) =====\n\n";
    std::vector<Particula> cluster;
    cluster.reserve(N_PARTICULAS);

    std::mt19937 rng2(7);
    std::normal_distribution<double> gauss_x(300.0, 30.0);
    std::normal_distribution<double> gauss_y(700.0, 30.0);
    std::uniform_real_distribution<double> unif(ESPACO_MIN, ESPACO_MAX);

    for (int i = 0; i < N_PARTICULAS / 2; ++i) {
        double x = std::clamp(gauss_x(rng2), ESPACO_MIN, ESPACO_MAX);
        double y = std::clamp(gauss_y(rng2), ESPACO_MIN, ESPACO_MAX);
        cluster.push_back({x, y, i});
    }

    for (int i = N_PARTICULAS / 2; i < N_PARTICULAS; ++i) {
        cluster.push_back({unif(rng2), unif(rng2), i});
    }

    omp_set_num_threads(num_threads);
    Quadtree qt_cluster(N_PARTICULAS);
    double t_cluster0 = omp_get_wtime();
    qt_cluster.construir(cluster);
    double t_cluster = omp_get_wtime() - t_cluster0;

    std::cout << "Construcao com cluster: " << std::fixed << std::setprecision(2)
    << t_cluster * 1000 << " ms\n";
    std::cout << "Profundidade maxima: " << qt_cluster.profundidade_maxima() << "\n";
    std::cout << "Nos alocados: " << qt_cluster.contar_nos() << "\n";
    std::cout << "Particulas contadas: " << qt_cluster.contar_particulas()
    << (qt_cluster.contar_particulas() == N_PARTICULAS ? " (OK)" : " (FALHA)") << "\n\n";

    auto res_bruta_c = qt_cluster.buscar_vizinhos(300.0, 700.0, 50.0);
    auto res_qt_c = qt_cluster.buscar_vizinhos_quadtree(300.0, 700.0, 50.0);
    std::sort(res_bruta_c.begin(), res_bruta_c.end());
    std::sort(res_qt_c.begin(), res_qt_c.end());

    std::cout << "Consulta no cluster (raio=50, cx=300, cy=700):\n";
    std::cout << "Vizinhos encontrados: " << res_bruta_c.size() << "\n";
    std::cout << "Corretude quadtree: " << (res_bruta_c == res_qt_c ? "OK" : "FALHA") << "\n";

    return 0;
}
