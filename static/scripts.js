$(document).ready(function() {
    $('.help-link').click(function(e) {
        e.preventDefault();
        
        var target = $(this).attr('href');
        
        $('.help-section').removeClass('active');
        $(target).addClass('active');
        
        // // Smooth scroll to the target section
        // $('html, body').animate({
        //     scrollTop: $(target).offset().top
        // }, 500);
    });
});

$(document).ready(function() {
    $('#help-toggle-btn').click(function() {
        $('.help').toggle(); // Toggle visibility of help section
        
    });
});
