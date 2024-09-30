function generateItinerary() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const location = document.getElementById('city-search-box').value;

    $('#generateButton').prop('disabled', true);
    $('#generateButton').html('Loading...');
    $('.button-28').css("border", "2px solid #FF0000");
    
    locationVals = [];
    $('.location-preference-tag').each(function() {
        var name = $(this).text();
        locationVals.push(name.substring(0, name.length - 1));
    });
    var locationPrefsString = "["+locationVals.join("], [")+"]";
    console.log("Passing the following into request: location="+location+", location-prefs="+locationPrefsString+", startDate="+startDate+", endDate="+endDate+",");

    $.ajax({
        type: "GET",
        url: '/api/get_place_id/',
        data: {'location': location, 'location-prefs': locationPrefsString, 'start-date': startDate, 'end-date': endDate},
        success: function(response) {
            console.log("Data sent successfully!");
            plotPoints(response);
            generateList(response, startDate, endDate, location);
            embedPhotos(response);
            $('#generateButton').prop('disabled', false);
            $('#generateButton').html('Generate Itinerary!');
            $('.button-28').css("border", "2px solid #864a05");
        },
        error: function(error) {
            console.error("Error sending data:", error);
            alert("Something went wrong, please reload the page and try again")
        }
    });
}