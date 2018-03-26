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

    $('span.stars').each(function () {
        var num_stars = parseInt($(this).text());
        var text_stars = "";

        console.log(num_stars);
        for (var i = 0; i < num_stars; i++) {
            text_stars += '<i class="fa fa-star" aria-hidden="true"></i>';
        }
        console.log(text_stars);
        $(this).html(text_stars);
    });

});