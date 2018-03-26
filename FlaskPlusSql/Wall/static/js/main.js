$(document).ready(function () {

    $(document).on('click', 'a.comment', function (e) {
        e.preventDefault();
        //$(this).parents('div.post-message').find('div.comment-form').css('display', 'block');
        var commentForm = $(this).parents('div.post-message').find('div.comment-form');
        commentForm.slideToggle();
    });


});