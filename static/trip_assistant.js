"use strict";


function getRestRec(results) {
    $("#rest_rec_results").html("<div>" + "Restaurant name: " +
        results["name"] + "<br>" + "Yelp rating: " + results["rating"] +
        "<br>" + "<a href=" + results["yelp"]+ ">Yelp page</a>" + "</div>");
    $("#rest_business_id").html(results["business_id"]);
    $("#rest_rec_saved").hide();
    $("#rest-save").css("display","block");
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
    $("#act_business_id").html(results["business_id"]);
    $("#act_rec_saved").hide();
    $("#act-save").css("display","block");
}


function recActivity(evt) {
    evt.preventDefault();

    var url = '/get_activity_rec';
    var location = $("#trip_location").text();

    $.get(url, {"location": location}, getActRec);
}

$('button#activity_rec_button').on('click', recActivity);


$(document).ajaxStart(function(){
    $("#loadingDiv").css("display","block");
});
    $(document).ajaxComplete(function(){
        $("#loadingDiv").css("display","none");
});


function restaurantRecSaved() {
    $("#rest_rec_saved").show();
    $("#rest-save").css("display","none");
}


function saveRestRec(evt) {
    evt.preventDefault();

    var url = "/save_rest_rec";
    var trip_id = $("#trip_id").text();
    var business_id = $("#rest_business_id").text();

    $.post(url, {"trip_id": trip_id, "business_id": business_id}, restaurantRecSaved);
}

$('button#save_rest_rec').on('click', saveRestRec);


function activityRecSaved() {
    $("#act_rec_saved").show();
    $("#act-save").css("display","none");
}


function saveActRec(evt) {
    evt.preventDefault();

    var url = '/save_act_rec';
    var trip_id = $("#trip_id").text();
    var business_id = $("#act_business_id").text();
    
    $.post(url, {"trip_id": trip_id, "business_id": business_id}, activityRecSaved);
}

$('button#save_act_rec').on('click', saveActRec);

