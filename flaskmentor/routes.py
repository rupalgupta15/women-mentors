import os
import json
from flask import jsonify, render_template, send_from_directory, request, url_for, flash, redirect
from flaskmentor.forms import SignUpForm, LoginForm, DetailsForm, SettingsForm
from flaskmentor import app, bcrypt, db
from flaskmentor import match_mentors, clean_user_input
from flaskmentor.models import User6, Test6, OAuth
from flask_paginate import Pagination, get_page_args
from flask_login import login_user, current_user, logout_user, login_required
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
import requests

# In Flask-Dance 1.4.0, "backends" were renamed to "storages"
# from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
# becomes this instead:
# from flask_dance.consumer.storage.sqla import SQLAlchemyStorage

# MOST USEFUL: https://github.com/singingwolfboy/flask-dance-twitter-sqla

app.secret_key = "supersekrit"
blueprint = make_twitter_blueprint(
    api_key="9jurSy2yLbPaGLPr3mBnoq61b",
    api_secret="8Ymv6VJAGvOAXD5F8upt3iLbdsFBkj3rauToRKgFXJrOdx5jpn"
)

app.register_blueprint(blueprint, url_prefix="/login")


# setup SQLAlchemy backend
blueprint.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user, user_required=False)


# https://flask-dance.readthedocs.io/en/v1.0.0/quickstarts/sqla-multiuser.html
# https://flask-dance.readthedocs.io/en/v1.0.0/multi-user.html

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
# once logged in, I will do following things once signal is received - oauth_authorized picks up the signal
def twitter_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Twitter.", category="error")
        return False

    # resp = blueprint.session.get("/user")  # OLD
    resp = blueprint.session.get("account/verify_credentials.json")
    if not resp.ok:
        msg = "Failed to fetch user info from Twitter."
        flash(msg, category="error")
        return False

    twitter_info = resp.json()
    # twitter_user_id = str(twitter_info["id"])
    twitter_user_id = twitter_info["id_str"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=twitter_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=twitter_user_id, token=token,)

    if oauth.user:
        # User already exists in the OAuth table
        login_user(oauth.user)
        flash("Successfully signed in with Twitter.", 'success')
        # Need to check if corresponding entry present in test table - for settings
        user_id = current_user.id
        # print('user_id', user_id)
        details = Test6.query.join(User6).filter(User6.id == user_id).all()
        # print('details', details)
        if len(details) == 0:
            return redirect(url_for('user_details'))
    else:
        # Create a new local user account for this user
        user = User6(
            # Remember that `email` can be None, if the user declines to publish their email address on GitHub!
            username=twitter_info["screen_name"]
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with Twitter.", 'success')
        user_id = current_user.id
        # print('user_id', user_id)
        details = Test6.query.join(User6).filter(User6.id == user_id).all()
        # print('details', details)
        if len(details) == 0:
            return redirect(url_for('user_details'))

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def twitter_error(blueprint, message, response):
    msg = (
        "OAuth error from {name}! "
        "message={message} response={response}"
    ).format(
        name=blueprint.name,
        message=message,
        response=response,
    )
    flash(msg, category="error")


@app.route('/twtsignin/')
# def my_link():
#   print ('I got clicked!')
#   return 'Click.'
def twtsignin():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    print('what is resp', resp.json())
    assert resp.ok
    # return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])
    # print('current_user', current_user.is_authenticated)  # This is false
    return redirect(url_for("user_details"))


@app.route('/')
@app.route('/home', methods = ['GET'])
def home_page():
    #  inspired from: https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    top_mentors = match_mentors.main(None, filename="replies_mentor_data.json")
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
    all_matched_mentors = match_mentors.main(query)
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
    details = Test6.query.join(User6).filter(User6.id == user_id).all()
    # print('details', details)
    if details:
        skills = details[0].mentorskills
    else:
        skills=''
    # TODO: Note that details[0] will only select the first entry from db corresponding to that user
    # print('skills', skills)
    all_matched_mentors = match_mentors.main(skills)
    return render_template("result.html", all_matched_mentors=all_matched_mentors)
    # return render_template('description.html', details=details)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = SignUpForm()
    if form.validate_on_submit():
        # first hash the password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User6(username=form.username.data, email=form.email.data, password=hashed_pw)
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
        details = Test6(mentorskills=form.looking_for.data, location=form.location.data, preference=form.preference.data, owner=current_user)
        #  password should be hashed version of text, not the text itself
        db.session.add(details)
        db.session.commit()
        # flash('Your Recommended Mentors', 'success')
        return redirect(url_for('description'))
    return render_template('details.html', title='User Details', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User6.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # we want to log this user in
            login_user(user, remember=form.remember.data)
            # The next section handles the case, where user tries to access account page without logging in
            # but is not allowed to access the account page. But once the user logs in, they will be redirected
            # to the same page (account page) from which they were requested to log in
            next_page = request.args.get('next')
            # if next_page:
            #     return redirect(next_page)
            # else:
            #     print('going here')
            #     print('URL', url_for('home_page'))
            #     redirect(url_for('home_page'))
            user_id = current_user.id
            details = Test6.query.join(User6).filter(User6.id == user_id).all()
            print('details', details)
            if details:
                skills = details[0].mentorskills
            else:
                skills = ''
                # TODO: Note that details[0] will only select the first entry from db corresponding to that user
            all_matched_mentors = match_mentors.main(skills)
            return redirect(next_page) if next_page else render_template("result.html", all_matched_mentors=all_matched_mentors)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        user_id = current_user.id
        details = Test6.query.join(User6).filter(User6.id == user_id).all()
        details[0].mentorskills = form.mentorskills.data
        details[0].location = form.location.data
        details[0].preference = form.preference.data
        print('details', details)
        db.session.commit()
        flash('Your Settings have been saved', 'success')
        return redirect(url_for('description'))
    # post get redirect pattern : are you sure you want to reload message
    # redirecting causes get request so we wont get that dialog box
    elif request.method == 'GET':
        # Let's us already populate current username data
        form.username.data = current_user.username
        user_id = current_user.id
        details = Test6.query.join(User6).filter(User6.id == user_id).all()
        form.mentorskills.data = details[0].mentorskills
        form.location.data = details[0].location
        form.preference.data = details[0].preference

    return render_template('settings.html', title='Settings', form=form)



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
