var multivalue_widget = {
    init: function() {
        // open close
        $('#multiselectWidgetLeft a.open').click(function() {
            var a = $(this);
            var div = $(this).parents()[1];
            var ul = $(div).next('ul');
            
            if ($(ul).is(":visible")) {
                $(ul).fadeOut();
                $(a).css('background', 'url(/static/images/open.png) no-repeat');
            } else {
                $(ul).fadeIn();
                $(a).css('background', 'url(/static/images/close.png) no-repeat');
            }
            
            return false;
        });
        
        // add
        $('#multiselectWidgetLeft a.add').click(function() {
            if ($('#multiselectWidgetRight li:first').text() == 'No Skills Selected') {
                $('#multiselectWidgetRight li:first').remove();
            }
    
            var span = $(this).parent();
            var prevSpanText = $(span).prev().text();
            var prevSpanId = $(span).prev().attr('rel');
            
            var li = $('<li><div><span>'+prevSpanText+'</span><span><a href="#" class="remove">remove</a><input type="hidden" name="skill" value="'+prevSpanId+'"/></span></div></li>');
            
            if ($('#multiselectWidgetRight input[value="'+prevSpanId+'"]').length < 1) {
                $('#multiselectWidgetRight ul').append(li);
                $('#multiselectWidgetRight ul li:last').hide().fadeIn();
            }
            
            return false;
        });
        
        // remove
        $('#multiselectWidgetRight a.remove').live('click', function() {
            var li = $(this).parents()[2];
            
            $(li).fadeOut(function() {
                $(this).remove();
                
                if ($('#multiselectWidgetRight li').length < 1) {
                    $('#multiselectWidgetRight ul').append('<li style="margin: 0 0 10px">No Skills Selected</li>');
                }
            });
            
            return false;
        });
    }
}

$(function() {
    multivalue_widget.init();
});