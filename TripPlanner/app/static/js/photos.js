function embedPhotos(response) {
    var photoDiv = document.getElementById("photos");
    photoDiv.replaceChildren();
    photoDiv.classList.remove("photosEnabled");
    photoDiv.classList.add("photosDisabled");

    var oneImageExists = false;

    var countryFlag = response['photos']['countryFlag'];
    if (countryFlag != ""){
        var countryFlagImg = document.createElement("img");
        countryFlagImg.src = countryFlag;
        photoDiv.appendChild(countryFlagImg);
        oneImageExists = true;
    }

    var cityPhoto = response['photos']['cityPhoto'];
    if (cityPhoto != ""){
        var cityPhotoImg = document.createElement("img");
        cityPhotoImg.src = cityPhoto;
        photoDiv.appendChild(cityPhotoImg);
        oneImageExists = true;
    }
    if (oneImageExists) {
        photoDiv.classList.remove("photosDisabled");
        photoDiv.classList.add("photosEnabled");
        var city = document.getElementById("city-search-box").value;
        photoDiv.innerHTML += '<div id="break"> <div id="city-name"> <b>' + city + '</b> </div> </div>'; 
    }
}