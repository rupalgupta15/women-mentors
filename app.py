import os
import json
from flask import Flask, jsonify, render_template, send_from_directory, request
import prepare_data
import requests
app = Flask(__name__)


# @app.route('/')
# def hello():
#     return "<h1> Hello World! </h1>"


@app.route('/')
def show_json():

    filename = os.path.join('data', 'final_mentors.json')
    # final_mentors
    # return send_from_directory('js', )

    with open(filename) as data_file:
        data = json.load(data_file)
        # data = data["mentors"][0]["description"]

    return render_template('index.html', data=data)
    # return jsonify(data)


@app.route('/result',methods = ['GET'])
def result():
    query = request.args.get('query')  # this url thing comes from the text entered by user on index.html
    all_matched_mentors = prepare_data.main(query)
    print(all_matched_mentors, len(all_matched_mentors))
    return render_template("result.html", all_matched_mentors=all_matched_mentors)

    # if request.method == 'POST':
    #     result = request.form
    #     return render_template("result.html",result = result)

if __name__ == '__main__':
    app.run(debug=True)
