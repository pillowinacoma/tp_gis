let data;

const map = L.map("map").setView([46.913394453425646, 2.3573931621362108], 7);
const accessToken =
  "pk.eyJ1IjoicGlsbG93aW5hY29tYSIsImEiOiJja3lla3BxY3kwMWlyMndwMHl5aXY2bzA1In0.NaGElR3WWIvsjh0Q4xhtgw";
L.tileLayer(
  `https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${accessToken}`,
  {
    attribution:
      'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    accessToken: "your.mapbox.access.token",
  }
).addTo(map);

// L.marker(
//     [46.913394453425646, 2.3573931621362108],
//     { icon: L.icon({ iconUrl: 'http://franck.favetta.free.fr/cours/lyon1/tiwsig/exercices/meteo/images/icones/neige.png', }) }
// ).addTo(map)

(async () => {
  const meteo = await (await fetch("http://localhost:8010/meteo")).json();
  const aeroports = await (
    await fetch("http://localhost:8010/aeroports")
  ).json();

  data = { meteo, aeroports };
  data.aeroports.features.forEach((it) => {
    const [x, y] = it.geometry.coordinates;
    let { properties } = it;
    const m = data.meteo[properties.icao];
    // console.log("m", m);
    // console.log("properties", properties);
    if (m) {
    }
    let icon_url =
      "http://franck.favetta.free.fr/cours/lyon1/tiwsig/exercices/meteo/images/icones/soleikkkl.png";
    console.log("M", m);
    if (m) {
      switch (m.ciel) {
        case "soleil":
          icon_url =
            "http://franck.favetta.free.fr/cours/lyon1/tiwsig/exercices/meteo/images/icones/soleil.png";
          break;
        case "nuageux":
          icon_url =
            "http://franck.favetta.free.fr/cours/lyon1/tiwsig/exercices/meteo/images/icones/couvert.png";
          break;
        case "neige":
          icon_url =
            "http://franck.favetta.free.fr/cours/lyon1/tiwsig/exercices/meteo/images/icones/neige.png";
          break;
        case "pluit":
          icon_url =
            "http://franck.favetta.free.fr/cours/lyon1/tiwsig/exercices/meteo/images/icones/pluie.png";
          break;
      }
      properties.taf = m.taf;
      properties.ciel = m.ciel;
      console.log("P", properties);
      const icon = L.icon({
        iconUrl: icon_url,
        iconSize: 100,
      });
      L.marker([y, x], { icon })
        .addTo(map)
        .bindPopup(
          `${Object.entries(properties)
            .map(([key, value]) => `<p><strong>${key}</strong> : ${value}</p>`)
            .join(" ")}`
        );
    }
  });
})();
