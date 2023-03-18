from flask import Flask, render_template, request, after_this_request
# import json
# from werkzeug.middleware.profiler import ProfilerMiddleware
app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.disabled = True
# file = open('stats.txt', 'a')
# app.wsgi_app  = ProfilerMiddleware(app.wsgi_app, profile_dir='.')
import testing
import time
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
planet_pass = pd.read_json('planets.json')
star_pass = pd.read_json('stars.json')
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='./profile')

@app.route('/')
def startup():
    return 'Welcome'

@app.route('/stars')
def norm_stars():
    # before = time.time()
    normal = request.args.get('normal')
    if normal == '0.0:0.0:0.0':
        normal = '0.01:0.01:0.01'
    normal = list(map(float, normal.split(':')))
    k = testing.normalise_stars(normal, star_pass)
    # @after_this_request
    # def cal_time(response):
    #     print(time.time() - before)
        # return response
    return k

@app.route('/planets')
def norm_planets():
    normal = request.args.get('normal')
    if normal == '0.0:0.0:0.0':
        normal = '0.01:0.01:0.01'
    normal = list(map(float, normal.split(':')))
    return testing.normalise_planets(normal, planet_pass)

scheduler = BackgroundScheduler()
scheduler.add_job(func=testing.update_data, trigger="interval", seconds=60)
scheduler.start()   

# @app.route('/planets')
# def load_planets():
#     testing.update_data()
#     planet_json = json.load(open(r'C:\Users\vikra\starview_api\planets.json'))
#     return planet_json

if __name__ == '__main__':
    # ip = "192.168.0.33"
    # ip = "172.28.8.38"
    app.run(debug=True, threaded=True, host = "0.0.0.0")