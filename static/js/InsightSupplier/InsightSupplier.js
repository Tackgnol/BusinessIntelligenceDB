;(function($){
    $.fn.extend({
        donetyping: function(callback,timeout){
            timeout = timeout || 1e3; // 1 second default timeout
            var timeoutReference,
                doneTyping = function(el){
                    if (!timeoutReference) return;
                    timeoutReference = null;
                    callback.call(el);
                };
            return this.each(function(i,el){
                var $el = $(el);
                // Chrome Fix (Use keyup over keypress to detect backspace)
                // thank you @palerdot
                $el.is(':input') && $el.on('keyup keypress',function(e){
                    // This catches the backspace button in chrome, but also prevents
                    // the event from triggering too premptively. Without this line,
                    // using tab/shift+tab will make the focused element fire the callback.
                    if (e.type=='keyup' && e.keyCode!=8) return;
                    
                    // Check if timeout has been set. If it has, "reset" the clock and
                    // start over again.
                    if (timeoutReference) clearTimeout(timeoutReference);
                    timeoutReference = setTimeout(function(){
                        // if we made it here, our timeout has elapsed. Fire the
                        // callback
                        doneTyping(el);
                    }, timeout);
                    e.stopImmediatePropagation();
                }).on('blur',function(){
                    // If we can, fire the event since we're leaving the field
                    doneTyping(el);
                });
            });
        }
    });
})(jQuery);

function GetURLParameter(param)
{
    var pageURL = window.location.search.substring(1);
    var URLValues = pageURL.split('&');
    for (var i = 0; i < URLValues.length; i++)
    {
        var parameterName = URLValues[i].split('=');
        if (parameterName[0] == param)
        {
            return parameterName[1];
        }
    }
};


$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
var selectedSort;
$(document).ready(function(){
    selectedSort = $('#subMenu').children('.Active');
    getInsights();
});


$('.SubMenuItem').on('click', function(e){
    $(this).siblings().removeClass('Active');
    $(this).addClass('Active');
    selectedSort = $(this);
    getInsights();
});

$('#searchField').donetyping(function() {
    getInsights();
}, 500);

$('#costInvolved').on('click', function(e){
    getInsights();
});


function getInsights() {
    $.ajax({
        url: 'Subcategory/ajax/getInsights/',
        type: 'GET', 
        data: {searchField: $('#searchField').val(), 
               costInvolved: $('#costInvolved').is(':checked'), 
               sortBy: selectedSort.text(),
               subCat: GetURLParameter('')},
        success: function(json) {
            var sites = $.parseJSON(json);
            $('#items').children().remove();
            $.each(sites, function(index, value){
                newInsight(value['Name'], value['Details'], value['Supplier'], value['Price'], value['Views']);
            });
            console.log(GetURLParameter('pk_url_kwarg'));
        },
        error: function (json) {
            console.log(json);
        }
    });

}

function newInsight(title, description, URL, price, views) {
    var div = $('<div />', {class: 'col-xs-11 col-sm-5 col-md-3 insight'}),
    pTitle = $('<p />', {class: 'header'}).text(title),
    img = $('<img />', {src: 'https://logo.clearbit.com/'+URL + '?size=100'}),
    stars = $('<span />', {class: 'header'});
    for(i=0; i<=4; i++) {
        stars.append($('<span />', {class:'fa fa-star checked'}))
    }
    pPrice = $('<p />', {class: 'regular'})
    if (price !== 0.0) {
        pPrice.text('Cost: ' + price + ' USD');
    } else {
        pPrice.text('This resource is free')
    }
    pViews = $('<p />', {class: 'regular'})
    pViews.text('Views: ' + views);
    div.fadeIn();
    div.append(pTitle,img,$('<br />'),pPrice, stars, pViews);
    div.appendTo($('#items'));

}