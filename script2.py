import requests
import pg8000

r = requests.get('http://api.geonames.org/search?featureClass=P&country=FR&maxRows=10&orderby=population&type=json&username=yoannbouge'); 

result = r.json()['geonames']

resu = list(map(lambda x: {'geonameId': x['geonameId'], 'name': x[
            'name'], 'geometry': (x['lat']) + ' ' + x['lng']}, result))

conn = pg8000.connect(user = "postgres", host = "localhost", port = 5432,
                              database = "postgres", password = "password")

for city in resu:
    conn.run("INSERT INTO public.villes(geonameid, geom, name) Values({}, {}, '{}');".format(
        city['geonameId'], "ST_GeomFromText('POINT({})')".format(city['geometry']), city['name']))

print(conn.run("SELECT * from public.villes"))

