"use strict";

function getRestRec(results) {
    $("#rest_rec_results").html("<div>" + "Restaurant name: " +
        results["name"] + "<br>" + "Yelp rating: " + results["rating"] +
        "<br>" + "<a href=" + results["yelp"]+ ">Yelp page</a>" + "</div>");
}


function recRestaurant(evt) {
    evt.preventDefault();

    var url = '/get_restaurant_rec';
    var location = $("#trip_location").text();

    $.get(url, {"location": location}, getRestRec);
}

$('button#restaurant_rec_button').on('click', recRestaurant);


function getActRec(results) {
    $("#act_rec_results").html("<div>" + "Activity name: " +
        results["name"] + "<br>" + "Yelp rating: " + results["rating"] +
        "<br>" + "<a href=" + results["yelp"]+ ">Yelp page</a>" + "</div>");
}


function recActivity(evt) {
    evt.preventDefault();

    var url = '/get_activity_rec';
    var location = $("#trip_location").text();

    $.get(url, {"location": location}, getActRec);
}

$('button#activity_rec_button').on('click', recActivity);

