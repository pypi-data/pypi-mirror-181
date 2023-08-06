import requests
import time
from abc import ABC, abstractmethod
import json
from datetime import datetime, timedelta
import typer


class ReExecution(ABC):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        self.user = user
        self._parser_request(id_arquivos, sleep_time)

    @property
    @abstractmethod
    def get_etl_step(self) -> str:
        pass

    @property
    @abstractmethod
    def get_name_ids(self) -> str:
        pass

    @staticmethod
    def countdown(t: int):
        typer.echo("\n")
        while t >= 0:
            typer.echo(f'Aguardando {t} segundos para enviar o proximo lote.    \r', nl=False)
            time.sleep(1)
            t -= 1
        typer.echo('                                                    \r', nl=False)

    def _parser_request(self, id_arquivos: list, sleep_time: int = 30):
        self.set_id_arquivos = set(id_arquivos)
        self.sleep_time = sleep_time

        # Measure time to finish:
        total_seconds = len(self.set_id_arquivos) * self.sleep_time
        m, s = divmod(total_seconds, 60)
        h, m = divmod(m, 60)

        currently_time = datetime.now()
        time_add = timedelta(hours=h, minutes=m, seconds=s)
        typer.echo(f"\n<> Há {len(self.set_id_arquivos)} {self.get_name_ids}")
        typer.echo(f"<> Previsão de hora: {(currently_time + time_add).strftime('%H:%M:%S')}")

        h, m, s = list(
            map(
                lambda x: f"0{x}" if len(str(x)) == 1 else x, [h, m, s]
            )
        )

        typer.echo(f"<> Tempo estimado: {h}h {m}min {s}s\n")

    def run(self, prioritario: bool = True, printar_ids: bool = False):
        try:
            c = 0
            enviados = []
            with typer.progressbar(enumerate(self.set_id_arquivos), len(self.set_id_arquivos)) as progress:
                for idx, id_ in progress:
                    url = 'https://v8wcnj1p11.execute-api.us-east-1.amazonaws.com/Prod/'
                    headers = {
                        "x-api-key": "GfkRdSHPM5rNBHgX2b4FVzuqDma7jhTT5utt7mY9kQ735pWekGp8jV6AayRSYF8q",
                        "Content-Type": "application/json"
                    }
                    body = {
                        "endpoint": "icdb-prod",
                        "input-type": "multiple-id",
                        "input": [id_],
                        "etl-step": self.get_etl_step,
                        "usuario": f"ReExecution - {self.user}"
                    }

                    if prioritario:
                        body["prioridade"] = "true"  # Só fará efeito em caso de DCM | DPGuias

                    body = json.dumps(body)

                    response = requests.post(url, data=body, headers=headers)
                    if not response.ok:
                        raise ConnectionError(f"Erro ao processar a requisição de reprocessamento ({response.status_code}): {response.content}")
                    if printar_ids:
                        typer.echo(f"  id atual: {id_}")
                    c += 1
                    enviados.append(id_)
                    self.countdown(self.sleep_time)
            typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
            typer.echo(f"{c} mensagens enviadas")
            typer.echo(f"ids enviados: {enviados}")
        except KeyboardInterrupt:
            typer.echo(typer.style('Execucao interrompida pelo usuario.                    ', typer.colors.RED))


class ReProcessar(ReExecution):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        super().__init__(id_arquivos, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return "posprocessamento"

    @property
    def get_name_ids(self) -> str:
        return "id_arquivos"


class ReLoad(ReExecution):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        super().__init__(id_arquivos, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return "load"

    @property
    def get_name_ids(self) -> str:
        return "id_arquivo_padronizados"


class RePadronizar(ReExecution):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        super().__init__(id_arquivos, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return "padronizacao"

    @property
    def get_name_ids(self) -> str:
        return "id_arquivo_parseados"


class ReParsear(ReExecution):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        super().__init__(id_arquivos, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return "parser"

    @property
    def get_name_ids(self) -> str:
        return "id_arquivo_originais"
