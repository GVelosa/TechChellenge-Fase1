import os
from api import create_app
from scripts.database_setup import populate_database

app = create_app()

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        while True:
            choice = input("Deseja executar o web scraping para atualizar a base de dados? (s/n): ").lower().strip()

            if choice in ['s', 'sim', 'y', 'yes']:
                print("\nIniciando o processo de web scraping e atualização do banco de dados...")
                try:
                    populate_database()
                    print("Processo de scraping finalizado com sucesso.\n")
                except Exception as e:
                    print(f"Erro durante o scraping: {e}")
                    print("Servidor será iniciado com os dados existentes (se houver).")
                break
            elif choice in ['n', 'nao', 'não', 'no']:
                print("\nPulando a etapa de scraping.\n")
                break 
            else:
                print("Opção inválida. Por favor, digite 's' para sim ou 'n' para não.")

    print("Iniciando o servidor da API Flask...")
    app.run(debug=True)