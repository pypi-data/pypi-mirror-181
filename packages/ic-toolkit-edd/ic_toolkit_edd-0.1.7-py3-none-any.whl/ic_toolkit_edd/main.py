import typer
import os
import sys
import hashlib
import re
import json
from pathlib import Path
import pandas as pd
import requests
from ic_toolkit_edd.abstract.utilities import credentials_path, read_credentials, Clipboard, FileExtensions, FileIdTypes, PdfStrippers, PipelineSteps
from ic_toolkit_edd.abstract.file_downloader import download_file
from ic_toolkit_edd.abstract.s3_utils import S3Object
import base64
import webbrowser
from ic_toolkit_edd.abstract.re_execution import *

app = typer.Typer()


@app.command()
def test():
    print(credentials_path())


@app.command()
def config(
        user_db: str = typer.Option(..., prompt=True),
        password_db: str = typer.Option(..., prompt=True),
        host_db: str = typer.Option(..., prompt=True),
        port_db: int = typer.Option(..., prompt=True),
        name_db: str = typer.Option(..., prompt=True),
        user_ic: str = typer.Option(..., prompt=True)):
    if not os.path.exists(credentials_path()):
        os.mkdir(credentials_path())
    with open(f"{credentials_path()}/.credentials", 'w') as credentials:
        credentials.write(
            f"userDB:{user_db}\npasswordDB:{password_db}\nhostDB:{host_db}\nportDB:{port_db}\nnameDB:{name_db}\nuserIC:{user_ic}")

@app.command()
def downpadr(
        id_arq: str,
        tipo_id: FileIdTypes = typer.Option(FileIdTypes.padronizado, "--tipo-id", "-t"),
        output_path: Path = typer.Option("./", "--output-path", "-o", exists=True, file_okay=False)):
    download_file(FileIdTypes.padronizado, tipo_id, id_arq, str(output_path))


@app.command()
def downpars(
        id_arq: str,
        tipo_id: FileIdTypes = typer.Option(FileIdTypes.parseado, "--tipo-id", "-t"),
        output_path: Path = typer.Option("./", "--output-path", "-o", exists=True, file_okay=False)):
    download_file(FileIdTypes.parseado, tipo_id, id_arq, str(output_path))


@app.command()
def downorig(
        id_arq: str,
        tipo_id: FileIdTypes = typer.Option(FileIdTypes.original, "--tipo-id", "-t"),
        output_path: Path = typer.Option("./", "--output-path", "-o", exists=True, file_okay=False)):
    download_file(FileIdTypes.original, tipo_id, id_arq, str(output_path))


@app.command()
def gethash(sha256: bool = False):
    hash_list = []
    filename_list = [f for f in os.listdir('./') if os.path.isfile(f)]
    for file in filename_list:
        with open(file, "rb") as f:
            bytes = f.read()
            if sha256:
                readable_hash = hashlib.sha256(bytes).hexdigest()
            else:
                readable_hash = hashlib.md5(bytes).hexdigest()
            hash_list.append(f'"{readable_hash}"')
    hashses = ', '.join(str(hash) for hash in hash_list)
    typer.echo(
        f"Foram calculados os hashes {('SHA256' if sha256 else 'MD5')} de {len(hash_list)} arquivo(s): {hashses}")
    if not sha256:
        clipboard = Clipboard()
        clipboard.copy(f'select * from upload.pipeline p where orig_ic_hash in ({hashses});')
        typer.echo(
            f"Uma query SQL para acompanhar o(s) arquivo(s) na pipeline foi copiada para a área de transferência")


@app.command()
def upload(path: Path = typer.Option(".", "--dir", "-d", exists=True, file_okay=False)):
    filename_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    with typer.progressbar(range(len(filename_list)), length=len(filename_list)) as progress:
        for i in progress:
            prefix = "Original/Plataforma/Upload/Old/"
            file_name = filename_list[i]
            file_type = re.search(r'.*\.(.*)$', file_name).group(1)
            file_path = os.path.join(path, file_name)
            try:
                file_type = FileExtensions(file_type)
            except ValueError:
                typer.echo(' ' + typer.style("ERRO", fg=typer.colors.WHITE, bg=typer.colors.RED))
                typer.echo(f'\nTipo de arquivo ".{file_type}" não suportado pela plataforma')
                return
            bucket = 'ic-filerepo-nvus'
            prefix += file_type.value + '/'
            try:
                S3Object.upload_file(file_path, bucket, prefix, file_name)
            except ConnectionError as e:
                typer.echo(' ' + typer.style("ERRO NO UPLOAD DO ARQUIVO", fg=typer.colors.WHITE, bg=typer.colors.RED))
                typer.echo(f'\nO cliente da S3 encontrou o seguinte erro fazer o upload do arquivo: {e}')
            except RuntimeError as e:
                typer.echo(' ' + typer.style("ERRO NO UPLOAD DO ARQUIVO", fg=typer.colors.WHITE, bg=typer.colors.RED))
                typer.echo(f'\nExceção encontrada durante o upload do arquivo: {e}')
        typer.echo(typer.style(" SUCESSO", fg=typer.colors.GREEN, bold=True))


@app.command()
def cvtpdf(input_path: Path = typer.Option(".", "--input-dir", "-i", exists=True),
           stripper: PdfStrippers = typer.Option("raw", "--stripper", "-s", prompt="Escolha o stripper:"),
           output_path: Path = typer.Option(".", "--output-dir", "-o", exists=True, file_okay=False, writable=True)):
    if not os.path.isfile(input_path):
        pdf_names = [os.path.basename(f) for f in os.listdir(input_path) if
                     os.path.isfile(os.path.join(input_path, f)) and f.endswith('.pdf')]
    elif input_path.name.endswith('.pdf'):
        pdf_names = [os.path.basename(input_path)]
        input_path = os.path.dirname(input_path)
    else:
        pdf_names = []
    if len(pdf_names) == 0:
        typer.echo(" " + typer.style("ERRO: NENHUM PDF ENCONTRADO", typer.colors.WHITE, typer.colors.RED))
        typer.echo(f'\nCaminho de entrada: "{input_path}"')
        return
    s3_bucket = 'ic-teste'
    s3_prefix = 'temp/'
    request_url = "https://api-transform.intuitivecare.com/prod/transform/pdf2txt/v2"
    request_payload = {
        "input": [
            {
                "filename": '',
                "prefix": s3_prefix,
                "bucket": s3_bucket,
                "options": {
                    "stripper": stripper.value
                }
            }
        ],
        "output": {
            "bucket": "ic-transient",
            "prefix": "txt2csv/"
        }
    }
    with typer.progressbar(range(len(pdf_names)), length=len(pdf_names)) as progress:
        for i in progress:
            pdf_path = os.path.join(input_path, pdf_names[i])
            try:
                pdf_object = S3Object.upload_file(pdf_path, s3_bucket, s3_prefix, pdf_names[i], override_object=False)
            except FileExistsError:
                pdf_object = S3Object(s3_bucket, s3_prefix, pdf_names[i])
            request_payload['input'][0]['filename'] = pdf_object.filename
            request_body = json.dumps(request_payload, indent=2).encode('utf-8')
            try:
                response = requests.post(request_url, data=request_body)
                if not response.ok:
                    typer.echo(" " + typer.style("ERRO AO ENVIAR REQUISIÇÃO PARA O CONVERSOR",
                                                 typer.colors.WHITE, typer.colors.RED))
                    typer.echo(f"\n{response.status_code} - {response.json()['message']}")
                    return
                response_data = response.json()
                txt_object = S3Object(response_data['response'][0]["Bucket"], response_data['response'][0]["Prefix"],
                                      response_data['response'][0]["Filename"])
                txt_object.download(str(output_path))
                # Escrevendo informações do objeto dos TXT em um arquivo temporário
                txt_info = str(txt_object)
                with open(os.path.join(output_path, f"{os.path.splitext(txt_object.filename)[0]}_caminho.txt"),
                          'w') as info_file:
                    info_file.write(txt_info)
            except Exception as e:
                typer.echo("\n\n" + typer.style('ERRO', typer.colors.WHITE, typer.colors.RED))
                typer.echo(f'Exceção encontrada durante a conversão do PDF "{pdf_names[i]}": {e}')
    typer.echo(typer.style(" SUCESSO", fg=typer.colors.GREEN, bold=True))
    typer.echo(
        f'\nForam convertidos {len(pdf_names)} arquivos! Os TXTs e caminhos para os objetos na S3 foram salvos no diretório "{output_path}"')


@app.command()
def equiv(destination_df: str = typer.Option(..., "--destino", "-d", prompt="Entre o nome do dataframe de destino"),
          origin_df: str = typer.Option("df", "--origem", "-o")):
    typer.prompt("Copie as três primeiras colunas da planilha de equivalência e pressione enter...", default="",
                 show_default=False, prompt_suffix="")
    equivalence_template = f"self.{destination_df}['{{0}}'] = self.{origin_df}['{{1}}']\n"
    equivalence_hardcoded_template = f"self.{destination_df}['{{0}}'] = {{1}}\n"
    equivalences = pd.read_clipboard()
    if len(equivalences.columns) != 3 or len(equivalences) == 0:
        typer.echo(" " + typer.style("\nERRO: EQUIVALÊNCIAS NÃO ENCONTRADAS", typer.colors.WHITE, typer.colors.RED))
        typer.echo("\nAs células copiadas estão vazias ou não estão no formato correto")
        typer.echo(
            'Certifique-se de copiar as três primeiras colunas da planilha ("Coluna (DOCUMENTO)", "OBS" e "Equivalencia")')
        return
    equivalences.drop(equivalences.columns[1], axis=1, inplace=True)
    equivalences.dropna(inplace=True)
    n_columns = equivalences.shape[0]
    equivalence_code = ''
    for i in range(n_columns):
        if "'" in equivalences.iloc[i, 1]:
            equivalence_code += equivalence_hardcoded_template.format(equivalences.iloc[i, 0].strip(),
                                                                      equivalences.iloc[i, 1].strip())
        else:
            equivalence_code += equivalence_template.format(equivalences.iloc[i, 0].strip(),
                                                            equivalences.iloc[i, 1].strip())
    clipboard = Clipboard()
    clipboard.copy(equivalence_code)
    typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
    typer.echo("O código de equivalência foi copiado para sua área de transferência")


@app.command()
def verids3(bucket: str = typer.Option(..., prompt=True), prefix: str = typer.Option(..., prompt=True),
            filename: str = typer.Option(..., prompt=True)):
    clipboard = Clipboard()
    object = S3Object(bucket, prefix, filename)
    try:
        version_id = object.version_id()
        clipboard.copy(version_id)
        typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
        typer.echo(f"ID da versão na AWS: {version_id}")
        typer.echo("O ID da versão também foi copiado para sua área de transferência")
    except Exception as e:
        typer.echo(typer.style("ERRO AO OBTER O VERSION_ID!", typer.colors.WHITE, typer.colors.RED))
        typer.echo(f"\nExceção encontrada: {e}")


@app.command()
def downs3(bucket: str = typer.Option(..., prompt=True), prefix: str = typer.Option(..., prompt=True),
           filename: str = typer.Option(..., prompt=True),
           output_path: Path = typer.Option(
                    ".", "--output-dir", "-o", prompt=True, exists=True, file_okay=False, writable=True)):
    object = S3Object(bucket, prefix, filename)
    try:
        object.download(str(output_path))
    except FileExistsError:
        choice = typer.confirm("O arquivo a ser baixado já existe no diretório de destino. Substituir?")
        if choice:
            object.download(output_path, True)
        else:
            typer.echo(typer.style("ERRO AO BAIXAR O OBJETO!", typer.colors.WHITE, typer.colors.RED))
            typer.echo(f"\nO objeto {object} já existe no diretório \"{output_path}\"")
            return
    except Exception as e:
        typer.echo(typer.style(f"ERRO AO BAIXAR O OBJETO!", typer.colors.WHITE, typer.colors.RED))
        typer.echo(f"\nExceção encontrada: {e}")
    typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
    typer.echo(f"O arquivo foi baixado com sucesso para o diretório {output_path}")


@app.command()
def uploads3(bucket: str = typer.Option(..., prompt=True), prefix: str = typer.Option(..., prompt=True),
             filename: str = typer.Option(""),
             input_path: Path = typer.Option(..., "--input-file", "-i", prompt=True, exists=True, dir_okay=False)):
    if filename == "":
        filename = typer.prompt("filename", default=input_path.name)
    obj = S3Object('', '', '')
    try:
        obj = S3Object.upload_file(str(input_path), bucket, prefix, filename)
    except FileExistsError:
        choice = typer.confirm(
            "O arquivo a ser enviado para a s3 já existe no bucket/prefixo informado. Deseja substituir o objeto?")
        if choice:
            obj = S3Object.upload_file(str(input_path), bucket, prefix, filename, override_object=True)
        else:
            typer.echo(typer.style("ERRO AO ENVIAR O ARQUIVO PARA A S3!", typer.colors.WHITE, typer.colors.RED))
            typer.echo(f"\nO arquivo \"{input_path}\" já existe no bucket/prefixo informado")
            return
    except Exception as e:
        typer.echo(typer.style(f"ERRO AO CARREGAR O ARQUIVO PARA A S3", typer.colors.WHITE, typer.colors.RED))
        typer.echo(f"\nExceção encontrada ao fazer o upload do arquivo \"{input_path}\": {e}")
    typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
    typer.echo(f"O arquivo foi salvo com sucesso na S3 como o objeto:")
    typer.echo(str(obj))

@app.command()
def reexec(step: PipelineSteps = typer.Option(..., "--passo-pipeline", "-p", prompt="Escolha o passo do pipeline para reprocessar"),
           interval: int = typer.Option(30, "--tempo-intervalo", "-t", prompt="Entre o intervalo entre cada requisição de reprocessamento (em segundos)", min=0),
           print_ids: bool = typer.Option(False, "--mostrar-ids", "-i", prompt="Deseja printar os IDs?")):
    id_type = PipelineSteps.required_id(step)
    id_type_name = "id_arquivo" + (f"_{id_type.value}" if id_type != FileIdTypes.arquivo else "")
    typer.echo(f"Entre os {id_type_name}'s separados por espaços, enter ou vírgulas. Ao final, deixe uma linha vazia e pressione enter...")
    ids_input = ''
    for line in sys.stdin:
        if line == "\n" or line == "":
            break
        ids_input += line
    ids_input = ids_input.strip()
    ids = [id_ for id_ in re.split(r",?\s+", ids_input) if id_ != '']
    ic_user = read_credentials()['userIC']
    if step == PipelineSteps.parsing:
        re_exec = ReParsear(ids, interval, ic_user)
    elif step == PipelineSteps.padronizacao:
        re_exec = RePadronizar(ids, interval, ic_user)
    elif step == PipelineSteps.load:
        re_exec = ReLoad(ids, interval, ic_user)
    elif step == PipelineSteps.pos_proc:
        re_exec = ReProcessar(ids, interval, ic_user)
    try:
        re_exec.run(prioritario=False, printar_ids=print_ids)
    except Exception as e:
        typer.echo(typer.style("ERRO AO REPROCESSAR ARQUIVOS!", typer.colors.WHITE, typer.colors.RED))
        typer.echo("fA seguinte exceção foi encontrada: {e}")

@app.command()
def filtro(id_arq: str, creditos: bool = typer.Option(False, "--creditos")):
    if creditos:
        rota = "conciliacao/creditos"
    else:
        rota = "glosas/auditar-glosas"
    if "," in id_arq:
        filtro = '{"id_arquivo":{"$in":[filter]}}'.replace("filter", id_arq)
    else:
        filtro = '{"id_arquivo":{"$eq":filter}}'.replace("filter", id_arq)
    base64_filtro = str(base64.b64encode(filtro.encode('utf-8'))).replace("b'", "").replace("'","")
    clipboard = Clipboard()
    clipboard.copy(f"https://app.intuitivecare.com/{rota}/protocolo/?filters={base64_filtro}")
    typer.echo(f"O filtro foi copiado para a área de transferência")