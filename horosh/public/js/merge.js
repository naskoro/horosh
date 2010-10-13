(function($) {
    $.fn.merge = function(data) {
        $data = $(data);
        if ($data.find('form').length) {
            if(!$data.find('.error-message').length) {
                return;
            }
        }
        $(this).html(data);
    };
})(jQuery);
