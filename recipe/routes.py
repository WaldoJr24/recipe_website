from recipe import app, db
from flask import render_template, request, url_for, redirect, flash, session
from flask_session import Session
from sqlalchemy import text

@app.route('/')
def home_page():
    cookie = session.get('username')
    #cookie = request.cookies.get('name')
    print("<>home_page()")
    return render_template('home.html', cookie=cookie)

@app.route('/login', methods=['GET', 'POST'])
def login_pages():
    print("login was called")

    if request.method == 'POST':
        print("->login_pages()")
        username = request.form.get('Username')
        password = request.form.get('Password')
        print("Here the Data!!!")
        print(username)
        print(password)

        if (username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            print("not valid")
            return render_template('login.html', cookie=None)

        if (password is None or
                isinstance(password, str) is False or
                len(password) < 3):
            print("something with password")
            return render_template('login.html', cookie=None)

        query_stmt = f"select username from recipeusers where username = '{username}' and password = '{password}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))

        user = result.fetchall()
        flash(f"User: '{user}', you are logged in!", category='success')

        if not user:
            return render_template('login.html', cookie=None)

        resp = redirect('/')
        session['username'] = username
        #resp.set_cookie('name', username)
        print("<-login(), go to home_page")
        return resp

    return render_template('login.html', cookie=None)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        print("->register_page()")

        username = request.form.get('Username')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        print(username)
        print(email)
        print(password1)
        print(password2)

        if(username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            print("<-register_page(), username invalid")
            return render_template('register.html', cookie=None)

        if(email is None or
                isinstance(email, str) is False or
                len(email) < 3):
            print("<-register_page(), email not valid")
            return render_template('register.html', cookie=None)

        if(password1 is None or
                isinstance(password1, str) is False or
                len(password1) < 3 or
                password1 != password2):
            print("<-register_page(), password1 not valid")
            return render_template('register.html', cookie=None)

        query_stmt = f"select * from recipeusers where username = '{username}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))
        item = result.fetchone()
        print(item)

        if item is not None:
            print("Username exists")
            return render_template('register.html', cookie=None)

        query_insert = f"insert into recipeusers (username, email_address, password) values ('{username}', '{email}', '{password1}')"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        resp = redirect('/recipes')
        session['username'] = username
        #resp.set_cookie('name', username)
        print("<-register_page(), go to recipes_pages")
        return resp

    return render_template('register.html')

@app.route('/recipes')
def recipes_pages():

    cookie = session.get('username')
    #cookie = request.cookies.get('name')
    print("->recipes_pages()", cookie)
    if not cookie:
        print("<-recipes_pages(), no cookie")
        return redirect(url_for('login_pages'))

    query_stmt = f"select * from recipeitems"
    result = db.session.execute(text(query_stmt))
    itemsquery = result.fetchall()

    print(itemsquery)
    print("<-recipes_pages()=", cookie)
    return render_template('recipes.html', items=itemsquery, cookie=cookie)

@app.route('/logout')
def logout():
    session.pop('username', None)
    resp = redirect('/')
    resp.set_cookie('name', '', expires=0)
    return resp

@app.route('/recipe_entry', methods=['GET', 'POST'])
def recipe_entry():
    cookie = session.get('username')
    #cookie = request.cookies.get('name')
    print("->recipe_entry()", cookie)
    if not cookie:
        print("no cookie")
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.cookies.get('name')
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        description = request.form.get('description')
        difficulty = request.form.get('difficulty')

        print("INSERT RECIPE DEBUG username:", username)
        query_insert = f"INSERT INTO recipeitems (username, title, description,ingredients, difficulty) VALUES ('{username}', '{title}', '{description}', '{ingredients}', '{difficulty}')"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        print("successfully added")
        return redirect('/recipes')

    return render_template('recipe_entry.html', cookie=cookie)

@app.route('/recipe_item/<int:item_id>', methods=['GET'])
def recipe_item(item_id):
    print("->recipe_item()")
    query_stmt = f"select * from recipeitems where id={item_id}"

    result = db.session.execute(text(query_stmt))
    item = result.fetchone()
    print(query_stmt)
    if not item:
        print("item not existing")

    cookie = session.get('username')
    #cookie = request.cookies.get('name')

    return render_template('recipe_item.html', items=item, cookie=cookie)