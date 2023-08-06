# django-google-sheets

essa biblioteca foi feito para uso proprio mas está sendo disponibilizado em varios projetos
devido a isso não existe uma documentação

Essa biblioteca é utilizada para alimentar benção de dados entre vários programadores entre si sem ter conteúdo repetindo ou faltando

O funcionamento é simples a cada post feito ele é adicionado uma cópia no Google sheets mas antes de adicionar
Os posts são restaurados vendo se não existe repetido e após isso o próprio Django verifica se não é um post repetido de acordo com as suas características únicasa
Após a confirmação o banco de dados no Google sheets é pagado em preenchimento com todos os dados do seu db assim podendo trabalhar em conjunto

Exemplo:

    from googlesheets import google_sheets

    class sb(models.Model):
        sbm = models.CharField(max_length=200)

        def __str__(self):
            return self.sbm
    
        def save(self, *args, **kwargs):
            google_sheets.add(self)
            super().save(*args, **kwargs)
            google_sheets.enviar(self)
            return self
    
        def delete(self, *args, **kwargs):
            google_sheets.delete(self)
            super().delete(*args, **kwargs)
    
        def restaurar():
            return google_sheets.restaurar(__class__.__name__)


Os principais comandos são os de
Adicionar ou atualizar os posts devem ser adicionado dentro do "def save(self, *args, **kwargs):"
O google_sheets.add(self) vai verificar se o posto é novo ou uma alteração
O google_sheets.enviar(self) vai enviar o post

Apagar um post
O google_sheets.delete(self) vai apagar o post

para funcionar deve conter a variavel "SHEETS_KEY" com o ID de sua tabela e um arquivo "service_account.json" na raiz do seu projeto
o service_account.json é uma autorização retirada do site do google para poder alterar a tabela exemplo de como é o service_account.json

    {
      "type": "service_account",
      "project_id": "",
      "private_key_id": "",
      "private_key": "",
      "client_email": "",
      "client_id": "",
      "auth_uri": "",
      "token_uri": "",
      "auth_provider_x509_cert_url": "",
      "client_x509_cert_url": ""
    }