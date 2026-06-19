from job_bot import config
from job_bot.database import init_db, salvar_vagas_batch, ja_candidatou, salvar_candidatura
from job_bot.platforms import vagas_com, infojobs, indeed

SCRAPERS = [
    ("vagas.com", vagas_com),
    ("infojobs", infojobs),
    ("indeed", indeed),
]


def executar_busca(palavras_chave=None, localizacao=None, max_vagas=None, log_callback=None):
    init_db()

    if palavras_chave is None:
        palavras_chave = config.PALAVRAS_CHAVE
    if localizacao is None:
        localizacao = config.LOCALIZACAO
    if max_vagas is None:
        max_vagas = config.MAX_CANDIDATURAS

    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    total_encontradas = 0
    total_novas = 0
    todas_vagas = []

    for palavra in palavras_chave:
        log(f"\n{'='*50}")
        log(f"[BUSCA] '{palavra}' em {localizacao}")
        log(f"{'='*50}")

        for nome_plataforma, scraper in SCRAPERS:
            log(f"\n  -> {nome_plataforma}...")
            try:
                vagas = scraper.buscar_vagas(palavra, localizacao, log_callback=log_callback)
            except Exception as e:
                log(f"  [ERRO] {nome_plataforma}: {e}")
                continue

            for vaga in vagas:
                vaga["palavra_chave"] = palavra

            total_encontradas += len(vagas)
            salvar_vagas_batch(vagas)

            for vaga in vagas:
                if ja_candidatou(vaga["link"]):
                    continue
                total_novas += 1
                todas_vagas.append(vaga)
                if not config.MODO_TESTE and total_novas <= max_vagas:
                    salvar_candidatura(
                        vaga["titulo"], vaga["empresa"],
                        vaga["plataforma"], vaga["link"]
                    )

    log(f"\nRESUMO: {total_encontradas} encontradas, {total_novas} novas")
    return {
        "total_encontradas": total_encontradas,
        "total_novas": total_novas,
        "vagas": todas_vagas,
    }