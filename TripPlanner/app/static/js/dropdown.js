function generateList(places, startDate, endDate, overall_location) {
    var outputElement = document.getElementById('accordion');
    outputElement.innerHTML = '';
    let dayCount = 1;
    if (startDate != '' && endDate != ''){
        var start = new Date(startDate);
        var end = new Date(endDate);
        dayCount = Math.round((end - start) / (1000 * 60 * 60 * 24)) + 1;
    }

    route_list = places['route_info'];
    console.log(route_list);

    console.log("Day count:", dayCount)

    for (let day = 0; day < dayCount; day++) {
        let dateString = '';
        if (startDate != '' && endDate != '') {
            var date = new Date(start.getTime() + (day * (1000 * 60 * 60 * 24)));
            const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            var currentDayOfWeek = daysOfWeek[date.getDay()];
            dateString = date.toISOString().split('T')[0];
            date_string_split = dateString.split('-')
            dateString = currentDayOfWeek + ' ' + months[parseInt(date_string_split[1])-1] + ' ' + date_string_split[2] + ', ' + date_string_split[0]
        }
        let gmapsLink = "https://google.com/maps/dir/";

        console.log("GMaps Link:", gmapsLink)
        // Create the header for each day with the date
        var dropdownHtml = '<div class="panel panel-default dropdownPanel">' +
                                '<div class="panel-heading" role="tab" id="heading' + day + '">' +
                                    '<div class="float-left" style="margin-top: 5px;">' +
                                        '<svg height="100%" width="55px" viewBox="0 0 55 55" class="icon"  version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M 25.6 4.2667 c -8.2475 0 -14.9333 6.6869 -14.9333 14.9333 c 0 8.2475 14.9333 27.7333 14.9333 27.7333 s 14.9333 -19.4859 14.9333 -27.7333 c 0 -8.2464 -6.6859 -14.9333 -14.9333 -14.9333 z m 0 22.4 a 7.4667 7.4667 90 1 1 0 -14.9333 a 7.4667 7.4667 90 0 1 0 14.9333 z" fill="' + dayToColor[day % dayToColor.length] + '" /></svg>' +
                                    '</div>' +
                                    '<h4 class="panel-title">' +
                                        '<a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse' + day + '" aria-expanded="false" aria-controls="collapse' + day + '">' +
                                            'Day ' + (day + 1) + ': ' + dateString + 
                                        '</a>' +
                                    '</h4>' +
                                '</div>' +
                                '<div id="collapse' + day + '" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading' + day + '">' +
                                    '<div class="panel-body">';

        // Check if there are locations for this day
        if (day < places['locations_info_list'].length) {
            const locs = places['locations_info_list'][day];
            let counter = 1;
            locs.forEach((location) => {
                console.log(location['name'])
                encoded_name = location['name'].split(' ').map(encodeURIComponent).join('+') + '+'
                gmapsLink += encoded_name + overall_location.split(', ').join('+');
                gmapsLink += '/';
            });
            dropdownHtml += '<a href="' + gmapsLink + '" style="margin-left: 10px;" target="_blank"><i>Day ' + (day+1) + ' Google Maps Route</i></a><br>';
          
            locs.forEach((location) => {             
                // Add route list
                if (counter <= route_list[day].length) {
                    time = route_list[day][counter - 1];
                    width = "225";
                    height = "225";
                    
                    dropdownHtml += '<div class="loc-name">' +
                                        '<div id="locationName">' + '<b>' + counter + '.</b> ' + location['name'] + '</div>' + 
                                        '<div id="locationEditorialSummary"><i>    ' + location['editorial_summary'] + '</i></div>' + '</div>' +
                                        '<div class="route-info">' +
                                            '<div id="dottedLine"></div>' +
                                            '<i class="fa-solid fa-car" style="color: #864a05; font-size: 25px;"></i>' + 
                                            '<div id="time">' + time + ' min</div></div>'
                } else {
                    dropdownHtml += '<div class="loc-name"> <div id="locationName"> <b>' + counter + '.</b> ' + location['name'] + '</div>';
                    dropdownHtml += '<div id="locationEditorialSummary"><i>    ' + location['editorial_summary'] + '</i></div>' + '</div>';
                }

                counter++;
            });
        } else {
            dropdownHtml += '<p>No locations for this day</p>';
        }

        dropdownHtml += '</div></div></div>';
        outputElement.innerHTML += dropdownHtml;
    }

    $('#dropdownContainer').removeClass('d-none'); // make dropdown visible
    $('.panel-collapse').on('show.bs.collapse', function () {
        $(this).siblings('.panel-heading').addClass('active');
        console.log("showing " + ($(this).parent().index() + 1));
        daysToShow.add($(this).parent().index() + 1);
        updateShownMarkers();
    });

    $('.panel-collapse').on('hide.bs.collapse', function () {
        $(this).siblings('.panel-heading').removeClass('active');
        console.log("hiding " + ($(this).parent().index() + 1));
        daysToShow.delete($(this).parent().index() + 1);
        updateShownMarkers();
    });
}