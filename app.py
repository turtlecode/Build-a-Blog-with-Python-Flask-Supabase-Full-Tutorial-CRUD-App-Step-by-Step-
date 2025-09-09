from flask import Flask, render_template, request, redirect
from supabase import create_client, Client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

app = Flask(__name__)

# Home page: list all blog posts
@app.route('/')
def index():
    posts = supabase.table('posts').select('*').order('created_at', desc=True)\
        .execute()
    return render_template('index.html', posts=posts.data)

# Add a new post
@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        supabase.table('posts').insert({'title': title, 'content': content})\
            .execute()
        return redirect('/')
    return render_template('add.html')

# Delete a post
@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    supabase.table('posts').delete().eq('id', post_id).execute()
    return redirect('/')

# Edit a post
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = supabase.table('posts').select('*').eq('id', post_id).single().\
        execute().data
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        supabase.table('posts').update({'title': title, 'content': content}).\
            eq('id', post_id).execute()
        return redirect('/')
    return render_template('edit.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
