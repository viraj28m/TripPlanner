
function plotPoints(response) {
    let centerLat = response['midpoint'][0];
    let centerLng = response['midpoint'][1];
    map.setCenter({lat: centerLat, lng: centerLng});
    map.setZoom(10);

    if (midpointMarker != null){
        midpointMarker.setMap(null);
    }
   
    midpointMarker = buildMidpointMarker(centerLat, centerLng);
    midpointMarker.setMap(map);

    console.log("LMAO PLOTPOINTS");
    console.log(response);
    console.log("hello");

    markers.forEach((day) => {
        day.forEach((marker) => {
            marker.setMap(null);
        });
    });
    markers = [];
    let names = [];
    let descs = [];
    for (let day = 0; day < response['locations_info_list'].length; day++){
        let tempMarkers = [];
        let tempNames = [];
        let tempDesc = [];
        response['locations_info_list'][day].forEach((location, index) => {
            tempMarkers.push(buildMarker(location['lat'], location['lng'], day, index + 1));
            tempNames.push(location['name']);
            tempDesc.push(location['editorial_summary']);
        });
        markers.push(tempMarkers);
        names.push(tempNames);
        descs.push(tempDesc);
    }
    for (let day = 0; day < markers.length; day++){
        for (let i = 0; i < markers[day].length; i++){
            markers[day][i].addListener('click', function() {
                infowindow.setContent(buildInfoWindow(names[day][i], descs[day][i], day));
                infowindow.open(map, markers[day][i]);
            });
        }
    }

}

function updateShownMarkers() {
    // Relies on the daysToShow set(), empty set means show everything
    // Otherwise, will show all days included in the set(), 1-indexed
    for(let day = 1; day <= markers.length; day++){
        if (daysToShow.size == 0 || daysToShow.has(day)) {
            markers[day - 1].forEach((marker) => {
                marker.setMap(map);
            });
        }
        else {
            markers[day - 1].forEach((marker) => {
                marker.setMap(null);
            });
        }
    }
}

function buildMidpointMarker(lat, lng){
    let markerSVG = {
        path: "M22,9.81a1,1,0,0,0-.83-.69l-5.7-.78L12.88,3.53a1,1,0,0,0-1.76,0L8.57,8.34l-5.7.78a1,1,0,0,0-.82.69,1,1,0,0,0,.28,1l4.09,3.73-1,5.24A1,1,0,0,0,6.88,20.9L12,18.38l5.12,2.52a1,1,0,0,0,.44.1,1,1,0,0,0,1-1.18l-1-5.24,4.09-3.73A1,1,0,0,0,22,9.81Z",
        fillColor: 'red',
        fillOpacity: 1.0,
        strokeWeight: 0,
        rotation: 0,
        scale: 1,
        anchor: new google.maps.Point(10, 10),
    };
    return new google.maps.Marker({
        position: {lat: lat, lng: lng},
        icon: markerSVG,
        map: map,
    });
}

var dayToColor = ["#E5A49F","#F4BF9F","#FBE685","#C5D3AB","#93BBA7","#CFE6E7","#E2CCDB","#C1AEE5","#A6A8B8","#D0B396"];
function buildMarker(lat, lng, day, index){
    let markerSVG = {
        path: "M128.052,16.75c-37.729,0-69.129,32.667-69.129,68.109c0,15.947,8.973,36.204,15.459,50.204l53.417,102.574 l53.162-102.574c6.484-13.999,15.711-33.242,15.711-50.203C196.671,49.418,165.773,16.75,128.052,16.75z",
        fillColor: dayToColor[day % dayToColor.length],
        fillOpacity: 1.0,
        strokeWeight: 0,
        rotation: 0,
        scale: 0.2,
        labelOrigin: new google.maps.Point(127, 95),
        anchor: new google.maps.Point(127, 231),
    };
    return new google.maps.Marker({
        position: {lat: lat, lng: lng},
        icon: markerSVG,
        map: map,
        label: {
            text: index.toString(),
            color: 'black',
            fontSize: '15px',
            fontWeight: 'bold'
          }
    });
}

function buildInfoWindow(name, desc, day) {
    let url = "https://www.google.com/maps/place/";
    // UNFINISHED: Make link redirect to actual place
    // url += name.split(" ").join("+");
    return '<div style: "display: inline-block" id="content">' + 
        '<style="padding: 5px 5px 5px 5px; border-radius: 10px 10px 0px 0px;-webkit-text-stroke: 1px black;color:'+ dayToColor[day % dayToColor.length] +'"> <h6>'+name+'</h6> <p>' + desc + '</p>' +
        '</div>';
}

let map;
let markers = [];
let infowindow;
let daysToShow = new Set();
let midpointMarker;
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 37.425290, lng: -122.174190 },
        zoom: 15,
        mapId: "c9d2b0ce8b0612fc",
    });

    const taginput = document.getElementById('input-tag'); 
    var autocomplete = new google.maps.places.Autocomplete(taginput);

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            // tag was blank, place not recognized
            console.log("No details available for input: '" + place.name + "'");
            return;
        }

        const placeName = place.name;
        createTag(placeName);
    });

infowindow = new google.maps.InfoWindow();
}