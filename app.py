from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista simulando um banco de dados em memória
livros = []

# Função para encontrar um livro pelo ID
def encontrar_livro_por_id(id):
    for livro in livros:
        if livro['id'] == id:
            return livro
    return None

@app.route('/', methods=['GET', 'POST'])
def gerenciar_livros():
    global livros
    livro_para_editar = None

    if request.method == 'POST':
        id = request.form.get('id')

        # Se for uma edição de um livro existente
        if id:
            livro_para_editar = encontrar_livro_por_id(int(id))
            if livro_para_editar:
                livro_para_editar['titulo'] = request.form['titulo']
                livro_para_editar['autor'] = request.form['autor']
                livro_para_editar['genero'] = request.form['genero']
                livro_para_editar['data_publicacao'] = request.form['data_publicacao']
        else:
            # Adicionar um novo livro
            novo_livro = {
                'id': len(livros) + 1,
                'titulo': request.form['titulo'],
                'autor': request.form['autor'],
                'genero': request.form['genero'],
                'data_publicacao': request.form['data_publicacao']
            }
            livros.append(novo_livro)

        return redirect(url_for('gerenciar_livros'))

    # Editar um livro existente
    if request.args.get('editar'):
        livro_para_editar = encontrar_livro_por_id(int(request.args.get('editar')))

    # Excluir um livro
    if request.args.get('excluir'):
        livro_para_excluir = encontrar_livro_por_id(int(request.args.get('excluir')))
        if livro_para_excluir:
            livros.remove(livro_para_excluir)
        return redirect(url_for('gerenciar_livros'))

    return render_template('livros.html', livros=livros, livro_para_editar=livro_para_editar)

if __name__ == '__main__':
    app.run(debug=True)
