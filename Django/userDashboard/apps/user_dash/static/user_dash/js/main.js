$(document).ready(function () {
    $('td.user-level').each(function () {
        if ($(this).text() === '1') {
            $(this).text('User')
        }
        if ($(this).text() === '9') {
            $(this).text('Admin')
        }
    });

    $(document).on('click', 'a.comment-link', function (e) {
        e.preventDefault();
        //$(this).parents('div.post-message').find('div.comment-form').css('display', 'block');
        var commentForm = $(this).parents('.post').find('div.comment-form-row');
        commentForm.slideToggle();
        console.log('click!')
    });

});