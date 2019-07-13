import os
import json
from flask import jsonify, render_template, send_from_directory, request, url_for, flash, redirect
from flaskmentor.forms import SignUpForm, LoginForm
from flaskmentor import app, bcrypt, db
from flaskmentor import prepare_data
from flaskmentor.models import User
from flask_login import login_user, current_user, logout_user, login_required
import requests


@app.route('/')  # was /home earlier
def home_page():
    return render_template('new_home_page.html')



@app.route('/show')
def show_json():
    filename = os.path.join('data', 'final_mentors.json')

    with open(filename) as data_file:
        data = json.load(data_file)

    return render_template('index.html', data=data)


@app.route('/result', methods = ['GET'])
def result():
    query = request.args.get('query')  # this url thing comes from the text entered by user on index.html
    all_matched_mentors = prepare_data.main(query)
    # print(all_matched_mentors, len(all_matched_mentors))
    return render_template("result.html", all_matched_mentors=all_matched_mentors)

    # if request.method == 'POST':
    #     result = request.form
    #     return render_template("result.html",result = result)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        # first hash the password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        #  password should be hashed version of text, not the text itself
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        # 2nd argument is category = "success" if for bootstrap class
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search_mentors.html', title='Search Mentors')


if __name__ == '__main__':
    app.run(debug=True)
