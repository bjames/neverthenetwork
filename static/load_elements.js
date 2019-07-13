var count = 20
var timer = null
var watch_intervall = null
var curr_active = null

$(document).ready(function() {

    load_anchor();

    // handle watch lready being set on a reload
    watch();

    $('#app').submit(function(event){

        event.preventDefault();

        submit_form();

        return false;
    
    })

    $('#watch').click(function() {

        watch();

    })

    // navbar clicks are handled here
    $('#dns_nav').click(function(){
        active(this)
        load_app('dns');
    })
    $('#subnet_nav').click(function(){
        active(this)
        load_app('subnet');
    })
    $('#curl_nav').click(function(){
        active(this)
        load_app('curl');
    })
    $('#oui_nav').click(function(){
        active(this)
        load_app('oui');
    })
    $('#ping_nav').click(function(){
        active(this)
        load_app('ping');
    })
    $('#traceroute_nav').click(function(){
        active(this)
        load_app('traceroute');
    })    
    $('#clear_scrollback').click(function(){
        $('#term').empty();
    })
});

function active(element) {

    if(curr_active != null){
        $(curr_active).attr('class', '');
    }
    curr_active = element
    $(element).attr('class', 'active')

}


function watch() {

    var checked = $('#watch').is(':checked');

    if(checked) {

        timer = setInterval(function() {
            countdown()
        }, 1000)

        watch_interval = setInterval(function() {
            submit_form();
        }, 30000);

    }else{

        try {
            clearInterval(watch_interval)
            clearInterval(timer)
            document.getElementById('timer').innerHTML='';
        }catch(e){
            // ignore errors due to unset watch_interval here
        }

    }
}


// used to submit the app forms via ajax
function submit_form() {

    var curr_app = document.getElementById("app").firstChild;

    classes = curr_app.classList;

    // disable the submit button to show the user we are working on the request
    $('#submit_app').attr('disabled', true);

    if(classes.contains("curl")){

        $.ajax({
            url: 'curl',
            type: 'post',
            data: $('[name=url]'),
            success: function(data) {

                update_term(data);
                $('#submit_app').attr('disabled', false);
     
            }
        });

    }else if (classes.contains("dns")){

        $.ajax({
            url: 'dns',
            type: 'post',
            data: {dns_lookup: $('[name=dns_lookup]').val(), user_resolver: $('[name=user_resolver]').val(), record_type: $('[name=record_type').val()},
            success: function(data) {

                update_term(data);  
                $('#submit_app').attr('disabled', false);       
      
            }
        });

    }else if (classes.contains("subnet")){

        $.ajax({
            url: 'subnet',
            type: 'post',
            data: {ip_address: $('[name=ip_address]').val(), subnet_mask: $('[name=subnet_mask').val()},
            success: function(data) {

                update_term(data);  
                $('#submit_app').attr('disabled', false);
  
            
            }
        });

    }else if (classes.contains("oui")){

        $.ajax({
            url: 'oui',
            type: 'post',
            data: $('[name=mac_address]'),
            success: function(data) {

                update_term(data);  
                $('#submit_app').attr('disabled', false);
  
            
            }
        });

    }else if (classes.contains("ping")){

        $.ajax({
            url: 'ping',
            type: 'post',
            data: $('[name=hostname]'),
            success: function(data) {

                update_term(data);   
                $('#submit_app').attr('disabled', false);
 
            
            }
        });

    }else if (classes.contains("traceroute")){

        $.ajax({
            url: 'traceroute',
            type: 'post',
            data: $('[name=hostname]'),
            success: function(data) {

                update_term(data);  
                $('#submit_app').attr('disabled', false);
  
            
            }
        });
    }
}

// countdown timer for the watch function
function countdown(timer) {

    count = count - 1;

    if (count <= 0)
    {
        count = 20;
        return;
    }

    document.getElementById('timer').innerHTML=count;
}

// used to append data to the terminal
function update_term(term_data) {

    $("#term").append(term_data);

    var term = document.getElementById("term");
    term.scrollTop = term.scrollHeight;

}

// loads the form above the terminal box
function load_app(app) {
    $('#app').load(app + ' #app');
    active($('#' + app + '_nav'))
    document.title = 'NTN - '+ app;
}

// allows bookmarks to function - if the request URL is #app, the app is loaded
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
            break;
        case '#oui':
            load_app('oui');
            break;
        case '#ping':
            load_app('ping');
            break;
        case '#traceroute':
            load_app('traceroute');
            break;
    }

}