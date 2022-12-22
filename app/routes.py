from app import app
from flask import render_template, jsonify
from functions import env_data, news

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/env_data', methods=['POST'])
def ENV():
    temp = env_data()
    return jsonify({'data': render_template('env_data.html', plot=temp)})

@app.route('/news', methods=['POST'])
def News():
    data = news()
    return jsonify({'data': render_template('news.html', news = data[:3])})