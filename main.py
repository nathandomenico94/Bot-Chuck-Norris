import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

def executar_automacao():
    try:
        # --- 1. BUSCA A PIADA ---
        response = requests.get("https://api.chucknorris.io/jokes/random", timeout=10)
        
        if response.status_code == 200:
            mensagem = response.json().get('value')
            print(f"Sucesso API! Mensagem: {mensagem}")
        else:
            print(f"Erro na API! Status Code: {response.status_code}")
            return

        # --- 2. AUTENTICAÇÃO (O SEGREDO ESTÁ AQUI) ---
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Pega a string do .env ou do GitHub Secrets
        creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        
        if not creds_json:
            print("Erro: A variável GOOGLE_SHEETS_CREDENTIALS não foi encontrada!")
            return

        # Converte a string JSON em dicionário e autentica
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # --- 3. GOOGLE SHEETS ---
        try:
            # Abre a planilha pelo nome exato
            sheet = client.open("Retorno API Chuck Norris").sheet1
            sheet.append_row([mensagem])
            print("Dados inseridos na planilha com sucesso!")
            
        except gspread.exceptions.SpreadsheetNotFound:
            print("Erro: Planilha não encontrada. Verifique o nome ou se compartilhou com o e-mail do JSON.")
        except Exception as e:
            print(f"Erro ao acessar a planilha: {e}")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    executar_automacao()