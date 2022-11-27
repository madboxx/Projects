import sqlite3
import random
from flask import Flask, session, render_template, request, g
#Alle imports

app = Flask(__name__) #Initialisere en klasse, kalder den app. 
app.secret_key = "Wolololo"

@app.route("/", methods=["POST", "GET"])
def index(): #Bemærk, alt er pakker ind i sessions - dette for at gøre lokale scopes globale! 
    session["all_items"], session["shopping_items"] = get_db() #Kalder get_db funktionen på linje 18
    return render_template("index.html", all_items=session["all_items"], shopping_items=session["shopping_items"]) #all_items, shopping_items matcher navne der findes i index.html filen

@app.route("/add_items", methods=["post"])
def add_items(): #Funktion oprettet der returnere valgte emner
    session["shopping_items"].append(request.form["select_items"])
    session.modified = True
    return render_template("index.html", all_items=session["all_items"], shopping_items=session["shopping_items"])

@app.route("/remove_items", methods=["post"]) #Sletning af emner på indkøbsliste
def remove_items():
    checked_boxes = request.form.getlist("check")

    for item in checked_boxes: 
        if item in session["shopping_items"]:
            idx = session["shopping_items"].index(item)
            session["shopping_items"].pop(idx)
            session.modified = True
    
    return render_template("index.html", all_items=session["all_items"], shopping_items=session["shopping_items"])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('grocery_list.db')
        cursor = db.cursor() #Opretter cursor object. 
        cursor.execute("select name from groceries") #Dette object bruges til at eksekvere sql-kommandoer.
        all_data = cursor.fetchall() #Returnerer resultatet for ovenstående sql-kommando, i en variable. 
        all_data = [str(val[0]) for val in all_data]

        shopping_list = all_data.copy() #Stykke der udvælger 5 stk fra shoppinglisten. 
        random.shuffle(shopping_list)
        shopping_list = shopping_list[:5]
    return all_data, shopping_list #Returnerer nu en tuple, og ikke en liste. 

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__': #Såfremt vores app hedder main = kør! 
    app.run()