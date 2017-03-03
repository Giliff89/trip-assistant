"use strict";

var new_tab = 'target="_blank"';

function getRestRec(results) {
    $("#rest_rec_results").html("<div>" + "Restaurant name: " +
        results["name"] + "<br>" + "Yelp rating: " + results["rating"] +
        "<br>" + "<a href=" + results["yelp"]+ " " + new_tab + ">Yelp page</a>" +
        "<br>" + results["categories"][0][0] + "<br> <img src=" +
        results["image_url"] + ">" + "</div>");
    $("#rest_business_id").html(results["business_id"]);
    $("#rest_rec_saved").hide();
    $("#rest-buttons").css("display","block");
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
        "<br>" + "<a href=" + results["yelp"]+ " " + new_tab + ">Yelp page</a>" +
        "<br>" + results["categories"][0][0] + "<br> <img src=" +
        results["image_url"] + ">" + "</div>");
    $("#act_business_id").html(results["business_id"]);
    $("#act_rec_saved").hide();
    $("#act-buttons").css("display","block");
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


function restaurantRecSaved(data) {
    $("#rest_rec_saved").show();
    $("#rest-buttons").css("display","none");

    if (data.rec_value == 3) {
        $(".rest_list").append('<li><a href="' + data.yelp +
                                           '">' + data.name + '</a></li>');
    }
}


function saveRestRec(evt) {
    evt.preventDefault();

    var url = "/save_rest_rec";
    var trip_id = $("#trip_id").text();
    var business_id = $("#rest_business_id").text();
    var rec_value = $(this).data("recVal");

    $.post(url, {"trip_id": trip_id, "business_id": business_id,
                 "rec_value": rec_value}).then(restaurantRecSaved);
}

$('button.rest_rec_feedback').on('click', saveRestRec);


function activityRecSaved(data) {
    $("#act_rec_saved").show();
    $("#act-buttons").css("display","none");

    if (data.rec_value == 3) {
        $(".act_list").append('<li><a href="' + data.yelp + '">' +
                                     data.name + '</a></li>');
    }
}


function saveActRec(evt) {
    evt.preventDefault();

    var url = '/save_act_rec';
    var trip_id = $("#trip_id").text();
    var business_id = $("#act_business_id").text();
    var rec_value = $(this).data("recVal");
    
    $.post(url, {"trip_id": trip_id, "business_id": business_id,
                 "rec_value": rec_value}).then(activityRecSaved);
}

$('button.act_rec_feedback').on('click', saveActRec);

