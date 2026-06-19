from job_bot.database import (
    salvar_candidatura as _db_salvar,
    ja_candidatou as _db_ja_candidatou,
)


def salvar_candidatura(vaga, empresa, plataforma, link):
    _db_salvar(vaga, empresa, plataforma, link)
    print(f"  [SALVO] {vaga} - {empresa} ({plataforma})")


def ja_candidatou(link):
    return _db_ja_candidatou(link)