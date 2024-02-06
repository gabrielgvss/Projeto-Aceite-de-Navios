from app import create_app

# Cria a aplicação Flask
app = create_app()

# Verifica se este arquivo está sendo executado diretamente
if __name__ == "__main__":
    # Executa o servidor Flask
    app.run(debug=True)