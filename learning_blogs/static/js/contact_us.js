$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#contact-us-modal .modal-content").html("");
                $("#contact-us-modal").modal("show");
            },
            success: function (data) {
                $("#contact-us-modal .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    // $("#book-table tbody").html(data.html_book_list);
                    $("#contact-us-modal").modal("hide");
                } else {
                    $("#contact-us-modal .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create modal window
    $(".js-contact-us").click(loadForm);
    $("#contact-us-modal").on("submit", ".js-contact-us-form", saveForm);

    // // Update book
    // $("#book-table").on("click", ".js-update-book", loadForm);
    // $("#modal-book").on("submit", ".js-book-update-form", saveForm);
    //
    // // Delete book
    // $("#book-table").on("click", ".js-delete-book", loadForm);
    // $("#modal-book").on("submit", ".js-book-delete-form", saveForm);

});