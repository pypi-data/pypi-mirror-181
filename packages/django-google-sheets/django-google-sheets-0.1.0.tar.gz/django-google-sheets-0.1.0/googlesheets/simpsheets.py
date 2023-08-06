import gspread
from django.conf import settings

class Sheets:


    def __init__(self):
        url = f'{settings.BASE_DIR}/service_account.json'
        gc = gspread.service_account(url)
        self.sh = gc.open_by_key(settings.SHEETS_KEY)

    def lertabmod(self,se):
        worksheet = self.sh.worksheet(se)
        return worksheet.get_all_values()

    def adicionar(self,se, add):
        self.sh.values_append(f'{se}!A1', params={'valueInputOption': 'RAW'}, body={'values': [add]})
        return self.__ler(se)

    def updata(self,se, add, celula):
        worksheet = self.sh.worksheet(se)
        self.worksheet.update(f'{celula}', [add])

    def delete(self,se, linha):
            worksheet = self.sh.worksheet(se)
            worksheet.delete_row(linha)

google_sheets_simp = Sheets()