(function($) {
    $.fn.merge = function(data) {
        data = strip(data);
        return doMerge(this, data);
        function strip(data) {
            if (data.length){
                var dataStrip = [];
                for (var i=0; i<data.length; i=i+1) {
                    if(!data[i].data || data[i].data.replace(/\s/g, '')) {
                        dataStrip.push(data[i]);
                    }
                }
                return dataStrip;
            }
            return data;
        }

        function doMerge(one, two) {
            if (two.data) {
                if (two.data!=one.data) {
                    one.data == two.data;
                }
                return one;
            }
            if (two.innerHTML) {
                if (two.innerHTML!=one.innerHTML) {
                    if (one.childNodes.length==two.childNodes.length) {
                        for(var i=0; i<two.childNodes.length; i=i+1) {
                            doMerge(one.childNodes[i], two.childNodes[i]);
                        }
                    } else {
                        return $(one).after($(two).clone()).remove();
                    }
                }
            }
            if (two.length) {
                if (two.length == one.length) {
                    for(var i=0; i<two.length; i=i+1) {
                        doMerge(one[i], two[i]);
                    }
                } else {
                    return $(one).after($(two).clone()).remove();
                }
            }
            return one;
        };
    };
    /*
    $.fn.replace = function(data) {
        return this.merge(data);
    };
    $.fn.replaceContent = function(data) {
        return $(this.html()).merge(data);
    };
    */

})(jQuery);
