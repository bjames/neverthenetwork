$(document).ready(function() {
    load_anchor();
    $('#app').submit(function(event){

        event.preventDefault();

        var curr_app = document.getElementById("app").firstChild;

        classes = curr_app.classList;

        if(classes.contains("curl")){

            $.ajax({
                url: 'curl',
                type: 'post',
                data: $('[name=url]'),
                success: function(data) {

                    update_term(data);
         
                }
            });

        }else if (classes.contains("dns")){

            $.ajax({
                url: 'dns',
                type: 'post',
                data: {dns_lookup: $('[name=dns_lookup]').val(), user_resolver: $('[name=user_resolver]').val(), record_type: $('[name=record_type').val()},
                success: function(data) {

                    update_term(data);         
          
                }
            });

        }else if (classes.contains("subnet")){

            $.ajax({
                url: 'subnet',
                type: 'post',
                data: {ip_address: $('[name=ip_address]').val(), subnet_mask: $('[name=subnet_mask').val()},
                success: function(data) {

                    update_term(data);    
                
                }
            });

        }else if (classes.contains("oui")){

            $.ajax({
                url: 'oui',
                type: 'post',
                data: $('[name=mac_address]'),
                success: function(data) {

                    update_term(data);    
                
                }
            });
        }

       return false;
    
    })

    $('#dns_nav').click(function(){
        load_app('dns');
    })
    $('#subnet_nav').click(function(){
        load_app('subnet');
    })
    $('#curl_nav').click(function(){
        load_app('curl');
    })
    $('#oui_nav').click(function(){
        load_app('oui');
    })

});

function update_term(term_data) {

    $("#term").append(term_data);

    var term = document.getElementById("term");
    term.scrollTop = term.scrollHeight;

}

function load_app(app) {
    $('#app').load(app + ' #app');
    document.title = 'NTN - '+ app;
}

function load_anchor() {
    console.log(window.location.pathname)
    switch ($(location).attr('hash')) {
        case '#curl':
            load_app('curl');
            break;
        case '#dns':
            load_app('dns');
            break;
        case '#subnet':
            load_app('subnet');
        case '#oui':
            load_app('oui');
            break;
    }
}
