import ssl
import socket


HOST_SERVIDOR = "192.168.56.101"
PORTA = 8443
ARQUIVO_CERTIFICADO_SERVIDOR = "servidor.crt"
COMANDO_SECRETO = "AUTH_TOKEN:XYZ123:CMD:REBOOT_SERVER"


def criar_contexto_ssl() -> ssl.SSLContext:
    """
    Cria e configura o contexto SSL do cliente para validar o certificado do servidor

    Returns:
        ssl.SSLContext: Contexto configurado com verificação do certificado autoassinado
    """

    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    contexto.load_verify_locations(ARQUIVO_CERTIFICADO_SERVIDOR)
    contexto.check_hostname = False

    return contexto


def enviar_comando() -> None:
    """
    Conecta ao servidor via TLS e envia o comando seguro
    """

    contexto = criar_contexto_ssl()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_base:
        with contexto.wrap_socket(socket_base, server_hostname=HOST_SERVIDOR) as socket_tls:
            print(f"[Cliente] Conectando ao servidor {HOST_SERVIDOR}:{PORTA}...")
            socket_tls.connect((HOST_SERVIDOR, PORTA))

            print(f"[Cliente] Conexão TLS estabelecida")
            print(f"[Cliente] Protocolo negociado: {socket_tls.version()}")
            print(f"[Cliente] Cifra negociada: {socket_tls.cipher()[0]}")
            print(f"[Cliente] Enviando comando: {COMANDO_SECRETO}")

            socket_tls.sendall(COMANDO_SECRETO.encode("utf-8"))
            print("[Cliente] Comando enviado com sucesso")


enviar_comando()
