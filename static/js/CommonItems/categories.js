
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

var categoriesTD = $('.category');
var subcategoriesTD = $('.subcategory');
$('#categorySearch').on('keyup', function(){
    categoriesTD.parent().hide();
    $(".category:contains("+$(this).val().toUpperCase()+")").parent().show()
});

$('#subCategorySearch').on('keyup', function(){
    categoriesTD.parent().hide();
    $(".subcategory:contains("+$(this).val().toUpperCase()+")").parent().show()
});
$('table').on('click', '.delete', function(){
    var row = $(this).parents('tr')
    if (confirm("This is will remove the element from the database, are you sure?")) {
        deleteSubCat(row.children('.subcategory'));
    }
});

$('table').on('submit', 'form', function(e){
    e.preventDefault();
    postChanges($(this).parent(), $(this).find('input[name="subCatID"]'), $(this).find('input[name="subCatDesc"]'));
    $(this).parents('tr').children('.change').show();
});

$('#newCategoryForm').on('submit', 'form', function(e) {
    e.preventDefault();
    clearErrors($(this));
    createSubCategory();
});

$('#newCategory').on('click', function(){
    $('#newCategoryForm').toggle(500);
    $(this).find('i').toggleClass('fa-plus fa-minus');
});

$('table').on('click', '.change', function(){
    var tr = $(this).parent();
    generateForm(1,tr)
});
function generateForm(id, tr) {
    var previousValue = tr.find('.subcategory').text()
    console.log(previousValue);
    var $form = $('<form />', {action:"", method:"POST", class:"form-inline editSubCategory"}),
    frmID = $('<input />', {id:"Id", type:"number", name:"subCatID", class:"form-control", value:previousValue.split('-')[0].trim()}),
    frmDesc = $('<input />', {type:"text", name:"subCatDesc", class:"form-control", value:previousValue.split('-')[1].trim()}),
    frmSubmitButton = $('<input />', { type: 'submit', value: 'Save',  class:"btn btn-primary" });
    frmCancelButton = $('<button />', { type:"button",  text:'Cancel', value: 'cancel', click: function() {cancelButton(previousValue, tr)} , class:"btn btn-danger" });
    $form.append(frmID, frmDesc, frmSubmitButton,frmCancelButton);
    tr.find('.subcategory').html("");
    tr.find('.change').hide()
    $form.appendTo(tr.find('.subcategory'));
    window.onbeforeunload = function() {
    return true;
    };

}
function cancelButton(previous, tr) {
    tr.find('.subcategory').text(previous);
    tr.find('.change').show();
    window.onbeforeunload = null;
}


function postChanges(td, categoryID, categoryDescription) {
    $.ajax({
        url: "ajax/EditCategory/",
        type: "POST",
        data: {changePK : td.attr('id'), newCatId: categoryID.val(), newCatDesc: categoryDescription.val()},

        success: function(json){
            td.text(json['catID']+' - '+json['catDesc']);
            window.onbeforeunload = null;
        },
        error: function(json) {
            var p = $('<p />', {class: "bg-danger"}).text("Ups, the query failed please try again later");
            td.prepend(p);
        }
    });
}
function deleteSubCat(td) {
    $.ajax({
        url: "ajax/DeleteCategory/",
        type: "POST",
        data: {deletePK: td.attr('id')},

        success: function(json){
            td.parents("tr").fadeOut(1000, function() {
            $(this).remove();
            })
        },
        error: function(json) {
            var p = $('<p />', {class: "bg-danger"}).text("Ups, the query failed please try again later");
            td.prepend(p);
        }
    });
}

function createSubCategory() {
    $.ajax({
        url: 'ajax/CreateCategory',
        type: 'POST',
        data: $('#newCategoryForm').find('form').serialize(),
        success: function(json){
            if (json.result) {
                $(':input','#newCategoryForm')
                .not(':button, :submit, :reset, :hidden')
                .val('');
                $(".CategoryParent").select2('val', 'All');
                console.log(json);
                var row = $('tr:nth-of-type(2)').clone();
                row.attr('id', json.pk);
                row.find('.category').text(json.Category);
                row.find('.subcategory').text(json.SubCategory);
                $('table').prepend(row).fadeIn("slow");         
            }  else {
                var p = $('<p />', {class: "bg-danger"}).text(json.msg)
                $('#FormBody').prepend(p);
            }

        },
        error: function(json) {
            var p = $('<p />', {class: "bg-danger"}).text(json.msg)
            $('#newCategoryForm').prepend(p);
        }

    })
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function clearErrors(element) {
    element.find('.bg-danger').remove();
}