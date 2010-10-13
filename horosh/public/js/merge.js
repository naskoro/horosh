(function($) {
    $.fn.merge = function(data) {
        $data = $(data);
        $this = $(this);
        if ($data.find('form').length) {
            if(!$data.find('.error-message').length && !$this.find('.error-message').length) {
                return;
            }
        }
        $this.html(data);
    };
})(jQuery);
