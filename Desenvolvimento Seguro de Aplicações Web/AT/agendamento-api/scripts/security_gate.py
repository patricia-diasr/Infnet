import json
import sys


SEVERIDADE_BLOQUEANTE = {"HIGH", "CRITICAL"}
RISCOS_ACEITOS = {
    "PYSEC-2026-1325": ("Dependência transitiva de python-jose. O ataque explora especificamente ecdsa.SigningKey.sign_digest() (assinatura via ECDSA); Essa aplicação usa exclusivamente HS256 (HMAC) para assinar JWTs, nunca ECDSA. Sem correção disponível upstream. Risco residual, monitorado."),
}


def checar_bandit(caminho: str) -> list[dict]:
    with open(caminho) as f:
        dados = json.load(f)

    bloqueantes = []

    for r in dados.get("results", []):
        severidade = r.get("issue_severity", "").upper()
        segredo_em_security = r.get("test_id") == "B105" and "app/security" in r.get("filename", "")

        if severidade in SEVERIDADE_BLOQUEANTE or segredo_em_security:
            bloqueantes.append(r)

    return bloqueantes


def checar_pip_audit(caminho: str) -> list[dict]:
    with open(caminho) as f:
        dados = json.load(f)

    bloqueantes = []

    for dep in dados.get("dependencies", []):
        for vuln in dep.get("vulns", []):
            if vuln.get("id") in RISCOS_ACEITOS:
                continue

            bloqueantes.append({**vuln, "package": dep["name"], "version": dep["version"]})

    return bloqueantes


def main() -> None:
    bandit_path = sys.argv[1] if len(sys.argv) > 1 else "reports/bandit-report.json"
    pip_audit_path = sys.argv[2] if len(sys.argv) > 2 else "reports/pip-audit-report.json"

    achados_sast = checar_bandit(bandit_path)
    achados_sca = checar_pip_audit(pip_audit_path)

    if not achados_sast and not achados_sca:
        print("OK: nenhum achado bloqueante em SAST ou SCA.")
        sys.exit(0)

    if achados_sast:
        print(f"BLOQUEADO (SAST): {len(achados_sast)} achado(s) de severidade HIGH/CRITICAL, ou segredo em app/security/.")
        for a in achados_sast:
            print(f"  - [{a['test_id']}] {a['test_name']} em {a['filename']}:{a['line_number']} (severidade: {a['issue_severity']})")

    if achados_sca:
        print(f"BLOQUEADO (SCA): {len(achados_sca)} CVE(s) sem risco aceito documentado.")
        for a in achados_sca:
            print(f"  - {a['id']} em {a['package']}=={a['version']}")

    sys.exit(1)


if __name__ == "__main__":
    main()
