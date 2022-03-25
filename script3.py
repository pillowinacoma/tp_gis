

from flask_cors import CORS
from flask import Flask
from functools import reduce
import requests
import pg8000
from shapely import wkb
import requests
import ssl


ssl_context = ssl.SSLContext()
ssl_context.verify_mode = ssl.CERT_NONE
conn = pg8000.connect(user = "p1711842", host = "bd-pedago.univ-lyon1.fr", port = 5432,
                              database = "p1711842", password = "Pu1WtY83xbUx", ssl_context=ssl_context)
localConnection = pg8000.connect(user = "postgres", host = "localhost", port = 5432,
                              database = "postgres", password = "password")


meteo_aeroports = conn.run("SELECT * from public.aeroport_proche_ville")


aeroports = list(map(lambda x: [*x[1:], wkb.loads(x[0], hex=True)],
                     meteo_aeroports))




icao = list(set(map(lambda x: x[3], aeroports)))


url = 'https://api.met.no/weatherapi/tafmetar/1.0/taf.txt?icao={}'.format(
    ",".join(icao))

headers = {
    'User-Agent': 'python',
    'Accept': 'text/plain'
}

response = requests.get(url, headers=headers)


tafs = response.text.split('\n')




def reduceTafs(acc, curr):
    splitted = curr.split(' ')
    if splitted[0] != '':
        acc[splitted[0]] = {'ciel': None, 'taf': curr}
        if curr.find('SN') != -1:
            acc[splitted[0]]['ciel'] = 'neige'
        elif curr.find('RA') != -1:
            acc[splitted[0]]['ciel'] = 'pluit'
        elif curr.find('OVC') != -1:
            acc[splitted[0]]['ciel'] = 'nuageux'
        else:
            acc[splitted[0]]['ciel'] = 'soleil'
    return acc


tafReduced = reduce(reduceTafs, tafs, {})
tafReduced


# save this as app.py


app = Flask(__name__)
CORS(app)


@app.route("/meteo")
def meteo():
    return tafReduced

@app.route("/aeroports")
def eo():
    from geojson import Point, FeatureCollection, Feature
    return FeatureCollection([
        Feature(
            geometry=Point((aero[5].xy[0][0], aero[5].xy[1][0])),
            properties={
                'aeroport': aero[2],
                'distance': aero[4],
                'icao': aero[3],
                'id_va': aero[0],
                'ville': aero[1]
            }
        ) for aero in aeroports
    ])


@app.route("/")
def hello():
    return "Hello"


if __name__ == '__main__':
    app.run(host='localhost', port=8010, debug=True)
