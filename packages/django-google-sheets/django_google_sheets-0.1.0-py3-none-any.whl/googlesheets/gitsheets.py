import gspread
from .simpsheets import google_sheets_simp
from datetime import datetime
from django.conf import settings
import git

class gitsh:

    def __init__(self):
        url = f'{settings.BASE_DIR}/service_account.json'
        gc = gspread.service_account(url)
        self.sh = gc.open_by_key(settings.SHEETS_KEY)

    def enviar(self):
        repo = git.Repo(".")
        master = repo.head.reference
        hcommit = repo.head.commit
        commits_list = list(repo.iter_commits())
        total_de_save_feitos = f'total de git commit: {len(commits_list)}'
        objetos_modificado = f"objetos modificado: {hcommit.diff('HEAD~1')}"
        total_de_arquivos_modificados = f"total de arquivos modificados nessa versão: {len(hcommit.diff('HEAD~1'))}"
        total_de_arquivos_modificados_em_todo_o_periudo = f"total de arquivos modificados: {len(hcommit.diff(f'HEAD~{int(len(commits_list))-1}'))}"
        descrcao = master.commit.message
        data = str(datetime.fromtimestamp(master.commit.committed_date))
        enviar = []
        for diff in hcommit.diff('HEAD~1'):
            tipo_de_modificacao = diff.change_type
            file = f'new file: {diff.new_file}'
            if diff.a_path == diff.b_path:
                arquivo = f'endereço: {diff.a_path}'
            else:
                arquivo = f'endereço antigo: {diff.a_path}, atual: {diff.b_path}'
            enviar.append([tipo_de_modificacao,file,arquivo,total_de_save_feitos,objetos_modificado,total_de_arquivos_modificados,total_de_arquivos_modificados_em_todo_o_periudo,descrcao,data])
        se = 'githistori'
        try:
            worksheet = self.sh.worksheet(se)
            worksheet.col_values(1)
        except:
            self.sh.add_worksheet(title=se, rows=1000, cols=9)
        google_sheets_simp.adicionar(se,enviar)

google_sheets_git = gitsh()