import os
import json
from flask import jsonify, render_template, send_from_directory, request, url_for, flash, redirect
from flaskmentor.forms import SignUpForm, LoginForm, DetailsForm
from flaskmentor import app, bcrypt, db
from flaskmentor import prepare_data, clean_user_input
from flaskmentor.models import User5, Test5
from flask_paginate import Pagination, get_page_args
from flask_login import login_user, current_user, logout_user, login_required
import requests


@app.route('/')
@app.route('/home', methods = ['GET'])
def home_page():
    #  inspired from: https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    top_mentors = prepare_data.main(None, filename="replies_mentor_data.json")
    top_mentors = top_mentors[:50]
    pagination_users = top_mentors[offset: offset + per_page]
    # print('len(top_mentors)', len(top_mentors))
    pagination = Pagination(page=page, per_page=per_page, total=len(top_mentors), record_name='top_mentors', css_framework='bootstrap4')
    return render_template('home.html', pagination_users=pagination_users, pag=page, per_page=per_page, pagination=pagination)


@app.route('/show')
def show_json():
    filename = os.path.join('data', 'final_mentors.json')

    with open(filename) as data_file:
        data = json.load(data_file)

    return render_template('index.html', data=data)


#  we might not even need this page
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


@app.route("/description")
def description():
    user_id = current_user.id
    details = Test5.query.join(User5).filter(User5.id == user_id).all()
    # print('details', details)
    skills = details[0].mentorskills
    # Note that details[0] will only select the first entry from db corresponding to that user
    print('skills', skills)
    all_matched_mentors = prepare_data.main(skills)
    return render_template("result.html", all_matched_mentors=all_matched_mentors)
    # return render_template('description.html', details=details)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        # first hash the password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User5(username=form.username.data, email=form.email.data, password=hashed_pw)
        #  password should be hashed version of text, not the text itself
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        # 2nd argument is category = "success" if for bootstrap class
        return redirect(url_for('user_details'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route("/user_details", methods=['GET', 'POST'])
@login_required
def user_details():
    form = DetailsForm()
    if form.validate_on_submit():
        # print('current_user', current_user)
        details = Test5(mentorskills=form.looking_for.data, location=form.location.data, preference=form.preference.data, owner=current_user)
        #  password should be hashed version of text, not the text itself
        db.session.add(details)
        db.session.commit()
        # flash('We found the following mentors for you', 'success')
        return redirect(url_for('description'))
    return render_template('details.html', title='User Details', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User5.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # we want to log this user in
            login_user(user, remember=form.remember.data)
            # The next section handles the case, where user tries to access account page without logging in
            # but is not allowed to access the account page. But once the user logs in, they will be redirected
            # to the same page (account page) from which they were requested to log in
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                redirect(url_for('home_page'))

        # return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/search", methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    # query = clean_user_input.main(query)
    return render_template('search_mentors.html', title='Search Mentors', query=query)


@app.route("/logout")
def logout():
    #  it doesnt need any parameters, because it knows which user is logged in
    logout_user()
    return redirect(url_for('home_page'))

# if __name__ == '__main__':
#     app.run(debug=True)
