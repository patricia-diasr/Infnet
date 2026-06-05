import ssl
import socket


HOST = "0.0.0.0"
PORTA = 8443
ARQUIVO_CERTIFICADO = "servidor.crt"
ARQUIVO_CHAVE = "servidor.key"
TAMANHO_BUFFER = 4096


def criar_contexto_ssl() -> ssl.SSLContext:
    """
    Cria e configura o contexto SSL do servidor com certificado autoassinado

    Returns:
        ssl.SSLContext: Contexto configurado com certificado e chave privada
    """

    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexto.load_cert_chain(certfile=ARQUIVO_CERTIFICADO, keyfile=ARQUIVO_CHAVE)

    return contexto


def iniciar_servidor() -> None:
    """
    Inicia o servidor TLS, aguarda conexões e exibe os comandos recebidos
    """

    contexto = criar_contexto_ssl()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_base:
        socket_base.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_base.bind((HOST, PORTA))
        socket_base.listen(5)

        print(f"[Servidor] Aguardando conexões TLS na porta {PORTA}...")

        with contexto.wrap_socket(socket_base, server_side=True) as socket_tls:
            while True:
                conexao, endereco = socket_tls.accept()

                with conexao:
                    print(f"[Servidor] Conexão estabelecida com {endereco}")
                    print(f"[Servidor] Protocolo negociado: {conexao.version()}")
                    print(f"[Servidor] Cifra negociada: {conexao.cipher()[0]}")
                    dados = conexao.recv(TAMANHO_BUFFER)

                    if dados:
                        mensagem = dados.decode("utf-8")
                        print(f"[Servidor] Comando Seguro Recebido: {mensagem}")


iniciar_servidor()
