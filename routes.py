from flask import Flask, render_template
import sqlite3

# create the Flask app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', title='HOME')


@app.route('/me')
def me():
    title = 'ME'  # an alternative way to send a variable to the template
    return render_template('me.html', title=title)


@app.route('/pet_rocks/<int:id>')  # only accept an INT in this position
def pet_rocks(id):  # must have the variable (id) in the function signature too
    id = id * 2  # just to show you can process the variable if you need to
    return render_template('pet_rocks.html', title='PET ROCKS', id=id)


@app.route('/adder/<int:one>/<int:two>')
def adder(one, two):
    total = one + two
    # what follows is an alternative way to structure the render_template
    # to ensure you don't breach the 79 character limit with lots of
    # parameters in the 'render_template' function call
    return render_template('adder.html', one=one, two=two, total=total, title=total)


@app.route('/all_pizzas')
def all_pizzas():
    conn = sqlite3.connect('pizza.db') # connect to the database
    cur = conn.cursor() # create a cursor to read lines from the database
    cur.execute('SELECT * FROM pizza') # give cursor a job to do
    pizzas = cur.fetchall()   # fetch all the results
    conn.close() # close the connection (you opened it so close it)
    return render_template('all_pizzas.html', pizzas=pizzas)


@app.route('/pizza/<int:id>')
def pizza(id):
    conn = sqlite3.connect('pizza.db')
    cur = conn.cursor()
    cur.execute('SELECT name, description, rank, base, photo FROM pizza WHERE id = ?', (id,))
    pizza = cur.fetchone()
    #using a join to get the toppings for the pizza
    cur.execute('''
    SELECT Topping.name, 
           Topping.description, 
           Topping.gf, 
           Topping.vegan 
    FROM PizzaTopping 
    JOIN Topping 
    ON PizzaTopping.tid = Topping.id 
    WHERE PizzaTopping.pid = ?
    ''', (id,)) # the comma is needed to make it a tuple 
    pizza_toppings = cur.fetchall()
    cur.execute('SELECT base.name FROM base JOIN Pizza ON Pizza.base = Base.id WHERE Pizza.id = ?', (id,))
    base = cur.fetchone()
    conn.close()

    return render_template('pizza.html', pizza=pizza, pizza_toppings=pizza_toppings, base=base)

if __name__ == '__main__':
    app.run(debug=True)
