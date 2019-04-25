from flask import Flask
from flask import render_template
from flask import jsonify
import yaml
with open("config/config.yml", 'r') as config:
    data = yaml.load(config)


app = Flask("Flask simple HTTP server")

tasks = [
            {
                'app_version': '1.0.0',
                'maintainer': u'Michał Gozdowski'
            }
        ]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/app/api/v1/info', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True, port=data['PORT'], host='0.0.0.0')


