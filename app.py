from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get("DB_URL")
client = MongoClient(host=host)

db = client.autocentral

#RESOURCES
users = db.users
comments = db.comments

app = Flask(__name__)

app.secret_key = '9a5c0aaf287745d3b21bb5a22e6dahewfef0e9c8fbr3bc39e34474f2f400f57'

@app.route('/')
def login():
    return render_template('login.html')



@app.route('/', methods=['GET', 'POST'])
def userlogin():
    if request.method=='GET':
        session['username']=request.form['username']
        flash('You are logged in', 'error')
        return redirect(url_for('login'))
    elif request.method=='POST':
        user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
        }
        user = users.insert_one(user)
        session['username']=request.form['username']
        print(user)
        user_obj = users.find_one({'username': session['username']})
        flash(f'You Have Successfully Registered', 'error')
        return redirect(url_for('login'))



@app.route('/index')
def index():
    user_obj = users.find_one({'username': session['username']})
    return render_template('index.html', user_obj=user_obj, user=user_obj)



@app.route('/findr')
def findr():
    user_obj = users.find_one({'username': session['username']})
    return render_template('findr.html', user_obj=user_obj, user=user_obj)


#Car Pages

@app.route('/camry')
def camry():
    return render_template('camry.html')

@app.route('/ford')
def ford():
    return render_template('ford.html')

@app.route('/civic')
def civc():
    return render_template('civic.html')

@app.route('/rogue')
def rogue():
    return render_template('rogue.html')

@app.route('/highlander')
def highlander():
    return render_template('highlander.html')

@app.route('/tesla')
def tesla():
    return render_template('tesla.html')

@app.route('/jeep')
def jeep():
    return render_template('jeep.html')

@app.route('/ram')
def ram():
    return render_template('ram.html')

@app.route('/sub')
def sub():
    return render_template('sub.html')

#------------------------------------------------

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    flash('You are logged out', 'error')
    session.pop("username", None)
    return render_template('logout.html')



@app.route('/insights')
def insight_index(): 
    insight=list(comments.find())
    for i in range(len(insight)):
      insight[i]['amount'] = str(insight[i]['amount'])
    
    user_obj = users.find_one({'username': session['username']})
    return render_template("insights.html", comments=insight, user_obj=user_obj, user=user_obj)



@app.route('/insights/new')
def insights_new():
    return render_template('insights_new.html')



@app.route('/comments', methods=['POST'])
def comment_submit():
    comment = {
        'name': request.form.get('destination-name'),
        'amount': request.form.get('amount'),
        'date': request.form.get('date')
      }
    comments.insert_one(comment)
    return redirect(url_for('insight_index'))



@app.route("/comments/<comment_id>/edit")
def comment_edit(comment_id):
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    return render_template('comment_edit.html', comment=comment)



@app.route("/comments/<comment_id>", methods=['POST'])
def comment_update(comment_id):
    updated_comment = {
        'name': request.form.get('destination-name'),
        'amount': request.form.get('amount'),
        'date': request.form.get('date')
    }

    comments.update_one(
        {'_id': ObjectId(comment_id)},
        {'$set': updated_comment})
    return redirect(url_for('isight_index', comment_id=comment_id))



@app.route('/comments/<comment_id>/delete', methods=['POST'])
def comment_del(comment_id):
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('insight_index'))



if __name__ == '__main__':
    app.run(debug=True, port=5000)