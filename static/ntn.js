var static_count = 10
var variable_count = static_count
var timer = null
var curr_active = null
var paused = false

$(document).ready(function() {

    load_anchor();

    // handle watch already being set on a reload
    watch();

    $('#app').submit(function(event){

        event.preventDefault();
        submit_form();
    
    })

    $('#watch').click(function() {

        watch();

    })

    // navbar clicks are handled here
    $('#dns_nav').click(function(){
        active(this);
        load_app('dns');
        enable_watch();
    })
    $('#subnet_nav').click(function(){
        active(this);
        load_app('subnet');
        disable_watch();
    })
    $('#curl_nav').click(function(){
        active(this);
        load_app('curl');
        enable_watch();
    })
    $('#oui_nav').click(function(){
        active(this)
        load_app('oui');
        disable_watch();
    })
    $('#ping_nav').click(function(){
        active(this);
        load_app('ping');
        enable_watch();
    })
    $('#traceroute_nav').click(function(){
        active(this);
        load_app('traceroute');
        enable_watch();
    })    
    $('#clear_scrollback').click(function(){
        $('#term').empty();
    })
    $('#nav_icon').click(function(){
        response_navbar();
    })
});

function disable_watch() {
    $('#watch').attr('disabled', true);
    $('#watch').attr('checked', false);
    clearInterval(timer);
    document.getElementById('timer').innerHTML='';
}

function enable_watch() {
    $('#watch').attr('disabled', false)
}

function active(element) {

    if(curr_active != null){
        $(curr_active).attr('class', '');
    }
    curr_active = element
    $(element).attr('class', 'active');

}

function start_timer() {

    timer = setInterval(function() {
        countdown();
    }, 1000)

}

// countdown timer for the watch function
function countdown(timer) {

    if (!paused) {

        variable_count = variable_count - 1;

        document.getElementById('timer').innerHTML=variable_count;

        if (variable_count == 0)
        {
            paused = true;
            submit_form();
            variable_count = static_count;
        }
    
    }

}

function watch() {

    var checked = $('#watch').is(':checked');

    if(checked) {
        variable_count = static_count;
        start_timer();
    }else{

        try {
            clearInterval(timer);
            document.getElementById('timer').innerHTML='';
        }catch(e){
            // ignore errors due to unset timer here
        }

    }
}

// used to submit the app forms via ajax
function submit_form() {

    var curr_app = document.getElementById("app").firstChild;

    classes = curr_app.classList;

    // disable the submit button to show the user we are working on the request
    $('#submit_app').attr('disabled', true);
    $('#term').addClass('spinner');

    if(classes.contains("curl")){

        $.ajax({
            url: 'curl',
            type: 'post',
            cache: false,
            data: $('[name=url]'),
            success: function(data) {
                post_success(data);
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("dns")){

        $.ajax({
            url: 'dns',
            type: 'post',
            cache: false,
            data: {dns_lookup: $('[name=dns_lookup]').val(), record_type: $('[name=record_type]').val(), user_resolver: $('[name=user_resolver]').val()},
            success: function(data) {

                post_success(data);

            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("subnet")){

        $.ajax({
            url: 'subnet',
            type: 'post',
            cache: false,
            data: {ip_address: $('[name=ip_address]').val(), subnet_mask: $('[name=subnet_mask]').val()},
            success: function(data) {

                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("oui")){

        $.ajax({
            url: 'oui',
            type: 'post',
            cache: false,
            data: $('[name=mac_address]'),
            success: function(data) {

                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("ping")){

        $.ajax({
            url: 'ping',
            type: 'post',
            cache: false,
            data: $('[name=hostname]'),
            success: function(data) {

                post_success(data);
            
            },
            error: function() {
                post_failed()
            }
        });

    }else if (classes.contains("traceroute")){

        $.ajax({
            url: 'traceroute',
            type: 'post',
            cache: false,
            data: $('[name=hostname]'),
            success: function(data) {

                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });
    }

}

function post_success(data) {
    console.log('post success');
    update_term(data);  
    paused = false;
    $('#submit_app').attr('disabled', false);
    $('#term').removeClass('spinner');
}

function post_failed() {
    paused = false;
    $('#submit_app').attr('disabled', false);
    $('#term').removeClass('spinner');
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

function response_navbar() {
    var element = document.getElementById("navbar");
    if (element.className === "navbar") {
      element.className += " responsive";
    } else {
      element.className = "navbar";
    }
} 