from flask import (Flask, render_template, abort, url_for, jsonify, request, redirect)
from model import db, save_db
app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template(
        "test.html",
        cards = db)

@app.route('/cards/<int:index>')
def cards_view(index):
    try:
        cards = db[index]
        return render_template("cards.html", cards=cards, index=index, max_index=len(db)-1)
    except IndexError:
        abort(500)

@app.route('/api/card/')
def api_card_list():
        return jsonify (db)

@app.route('/api/cards/<int:index>')
def api_cards_view(index):
    try:
       return db[index]
    except IndexError:
        abort(400)

@app.route('/add_cards/', methods= ["GET", "POST"])
def add_cards():
    if request.method == "POST":
        card = {"color": request.form["color"],
                "category": request.form["category"],
                "type": request.form["type"],
                "hex": request.form["hex"]}
        db.append(card)
        save_db()

       # return redirect("https://www.w3schools.com/python/python_json.asp")
        return redirect(url_for('cards_view', index=len(db)-1))
    else:
        return render_template("add_card.html")

@app.route('/remove_cards/<int:index>', methods= ["GET", "POST"])
def remove_cards(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html", cards=db[index])
    except IndexError:
        abort(404)


if __name__ =='__main__':
   app.run(debug=True, port=5000)
