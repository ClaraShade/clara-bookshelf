from books_web import create_app

app, api = create_app()

if __name__ == "__main__":
    app.run(debug=True)
