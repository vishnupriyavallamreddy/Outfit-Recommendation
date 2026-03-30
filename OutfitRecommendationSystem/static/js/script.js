$(document).ready(function() {
    // Form validation using jQuery before submission
    $('#recommendation-form').on('submit', function(event) {
        let isValid = true;
        let weather = $('#weather').val();
        let occasion = $('#occasion').val();

        // Check weather selection
        if (weather === "") {
            $('#weather').addClass('is-invalid');
            isValid = false;
        } else {
            $('#weather').removeClass('is-invalid').addClass('is-valid');
        }

        // Check occasion selection
        if (occasion === "") {
            $('#occasion').addClass('is-invalid');
            isValid = false;
        } else {
            $('#occasion').removeClass('is-invalid').addClass('is-valid');
        }

        // Prevent submission if invalid
        if (!isValid) {
            event.preventDefault();
        } else {
            // Show loading overlay
            $('#loading-overlay').css('display', 'flex').hide().fadeIn(300);
        }
    });

    // Remove validation styles on change event
    $('#weather, #occasion').on('change', function() {
        $(this).removeClass('is-invalid').addClass('is-valid');
    });

    // Like/Favorite interaction on result page
    $('.btn-like').on('click', function() {
        let btn = $(this);
        let icon = btn.find('i');
        let text = btn.find('.like-text');
        
        if (btn.hasClass('btn-outline-danger')) {
            btn.removeClass('btn-outline-danger').addClass('btn-danger shadow-sm');
            icon.removeClass('bi-heart').addClass('bi-heart-fill');
            text.text('Favorited');
            
            // Add a small pop animation
            btn.css('transform', 'scale(1.08)');
            setTimeout(() => btn.css('transform', ''), 200);
        } else {
            btn.removeClass('btn-danger shadow-sm').addClass('btn-outline-danger');
            icon.removeClass('bi-heart-fill').addClass('bi-heart');
            text.text('Favorite');
        }
    });

    // Hide loading overlay on pageshow (handling back button caching rendering)
    $(window).on('pageshow', function() {
        $('#loading-overlay').fadeOut();
    });
});
