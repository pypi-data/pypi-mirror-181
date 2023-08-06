import gspread
from django.conf import settings
import json
from django.core import serializers


def addicionar(self):
    adr = [self.pk,str(serializers.serialize('json', [self]))]
    ad = str(serializers.serialize('json', [self])).split("[")
    ad = str(ad[1]).split("]")
    ad = json.loads(str(ad[0]))
    ad = str(ad['model']).split('.')
    return adr, str(ad[1])


class Sheets:


    def __init__(self):
        url = f'{settings.BASE_DIR}/service_account.json'
        gc = gspread.service_account(url)
        self.sh = gc.open_by_key(settings.SHEETS_KEY)

    def __ler(self,se):
        add, worksheet = addicionar(se)
        worksheet = self.sh.worksheet(worksheet)
        return worksheet.get_all_values()

    def lertabmod(self,se):
        ws = se.lower()
        worksheet = self.sh.worksheet(ws)
        lis = []
        for li in worksheet.col_values(2):
            s = li.split("[")
            s = s[1].split("]")
            lis.append(s[0])
        lis = str(lis)
        lista = lis.replace("['",'[')
        lista = lista.replace("']",']')
        lista = lista.replace("'",'')
        return lista

    def __verificarigualdade(self,se):
        add, worksheet = addicionar(se)
        wk = worksheet
        y = False
        worksheet = self.sh.worksheet(worksheet)
        itens = worksheet.col_values(2)
        itensfiltrados = []
        for i in itens:
            if not (i in itensfiltrados):
                itensfiltrados.append(i)
        self.sh.del_worksheet(worksheet)
        self.sh.add_worksheet(title=wk.lower(), rows=1000, cols=2)
        for i in itensfiltrados:
            ad = str(i).split("[")
            ad = str(ad[1]).split("]")
            ad = json.loads(str(ad[0]))
            adr = [ad['pk'], i]
            self.sh.values_append(f'{wk}!A1', params={'valueInputOption': 'RAW'}, body={'values': [adr]})
        if not (add in itensfiltrados):
            y = True
        return y

    def __adicionar(self,se):
        if self.__verificarigualdade(se) == True:
            add, worksheet = addicionar(se)
            self.sh.values_append(f'{worksheet}!A1', params={'valueInputOption': 'RAW'}, body={'values': [add]})
            return self.__ler(se)

    def __updata(self,se):
        if self.__verificarigualdade(se) == True:
            antigo = se.pk
            add, worksheet = addicionar(se)
            x = 1
            y = None
            worksheet = self.sh.worksheet(worksheet)
            pks = worksheet.col_values(1)
            for i in pks:
                if int(i) == int(antigo):
                    y = x
                x += 1
            if y == None:
                self.__adicionar(add,worksheet)
                return False
            else:
                self.worksheet.update(f'A{y}', [add])
                return True

    def __existe(self,se):
        try:
            add, worksheet = addicionar(se)
            worksheet = self.sh.worksheet(worksheet)
            pks = worksheet.col_values(1)
            return True
        except:
            try:
                worksheet = self.sh.worksheet(se)
                pks = worksheet.col_values(1)
                return True
            except:
                try:
                    add, worksheet = addicionar(se)
                    self.sh.add_worksheet(title=worksheet.lower(), rows=1000, cols=2)
                except:
                    self.sh.add_worksheet(title=se.lower(), rows=1000, cols=2)
                return False

    def delete(self,se):
        if self.__existe(se) == True:
            self.restaurar(se)
            antigo = se.pk
            add, worksheet = addicionar(se)
            x = 1
            worksheet = self.sh.worksheet(worksheet)
            pks = worksheet.col_values(1)
            for i in pks:
                if int(i) == int(antigo):
                    worksheet.delete_row(x)
                x = x+1
            return True
        else:
            return False

    def add(self, se):
        self.restaurar(se)
        self.__existe(se)
        salvar = None
        if se.pk:
            salvar = 1
        else:
            salvar = 0
        self.salvar = salvar

    def enviar(self, se):
        if self.salvar == 1:
            self.__updata(se)
        elif self.salvar == 0:
            self.__adicionar(se)

    def restaurar(self, se):
        try:
            se = se.lower()
            self.__existe(se)
            obj_generator = serializers.deserialize("json", self.lertabmod(se), ignorenonexistent=True)
            for obj in obj_generator:
                obj.save()
            return self.lertabmod(se)
        except:
            add, worksheet = addicionar(se)
            obj_generator = serializers.deserialize("json", self.lertabmod(worksheet), ignorenonexistent=True)
            for obj in obj_generator:
                obj.save()
            return self.lertabmod(worksheet)

google_sheets = Sheets()