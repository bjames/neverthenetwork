$(document).ready(function() {
    $('#curl_nav').click(function(){
        $('#app').load('curl #app', function() {
        });
    })
    $('#app').submit(function(event){

        event.preventDefault()

        var curr_app = document.getElementById("app").firstChild

        classes = curr_app.classList

        if(classes.contains("curl")){

            $.ajax({
                url: 'curl',
                type: 'post',
                data: $('[name=url]'),
                success: function(data) {

                    $("#term").append(data);

                    var term = document.getElementById("term");
                    term.scrollTop = term.scrollHeight;            
                }
            });

        }else if (classes.contains("dns")){

            $.ajax({
                url: 'dns',
                type: 'post',
                data: {dns_lookup: $('[name=dns_lookup]').val(), user_resolver: $('[name=user_resolver]').val(), record_type: $('[name=record_type').val()},
                success: function(data) {

                    $("#term").append(data);

                    var term = document.getElementById("term");
                    term.scrollTop = term.scrollHeight;            
                }
            });

        }else if (classes.contains("subnet")){

            $.ajax({
                url: 'subnet',
                type: 'post',
                data: {ip_address: $('[name=ip_address]').val(), subnet_mask: $('[name=subnet_mask').val()},
                success: function(data) {

                    $("#term").append(data);

                    var term = document.getElementById("term");
                    term.scrollTop = term.scrollHeight;            
                }
            });

        }

       return false;
    
    })

    $('#dns_nav').click(function(){
        $('#app').load('dns #app', function() {
        });
    })
    $('#subnet_nav').click(function(){
        $('#app').load('subnet #app', function() {
        });
    })
});