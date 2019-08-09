var static_count = 10
var variable_count = static_count
var timer = null
var curr_active = null
var paused = false

$(document).ready(function() {

    $('#bottom_buttons').css('display', 'inherit');
    $('#nojs_text').css('display', 'none');


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
        event.preventDefault();
        active(this);
        load_app('dns', 'DNS');
        enable_watch();
        response_navbar();
    })
    $('#subnet_nav').click(function(){
        event.preventDefault();
        active(this);
        load_app('subnet', 'Subnet');
        disable_watch();
        response_navbar();
    })
    $('#curl_nav').click(function(){
        event.preventDefault();
        active(this);
        load_app('curl', 'cURL');
        enable_watch();
        response_navbar();
    })
    $('#oui_nav').click(function(){
        event.preventDefault();
        active(this)
        load_app('oui', 'OUI');
        disable_watch();
        response_navbar();
    })
    $('#ping_nav').click(function(){
        event.preventDefault();
        active(this);
        load_app('ping', 'Ping');
        enable_watch();
        response_navbar();
    })
    $('#traceroute_nav').click(function(){
        event.preventDefault();
        active(this);
        load_app('traceroute', 'Traceroute');
        enable_watch();
        response_navbar();
    })
    $('#whois_nav').click(function(){
        event.preventDefault();
        active(this);
        load_app('whois', 'Whois');
        enable_watch();
        response_navbar();
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
    $('#timer').css('visibility', 'hidden');
    clearInterval(timer);
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
        $('#timer').css('visibility', 'visible');
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
            $('#timer').css('visibility', 'hidden');
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

        var url = $('[name=url]').val();
        var follow_redirects = $('[name=follow_redirects]').is(':checked');

        $.ajax({
            url: 'curl',
            type: 'post',
            cache: false,
            data: {url: url, follow_redirects: follow_redirects},
            success: function(data) {
                set_query_string('curl?url=' + url + '&follow_redirects=' + follow_redirects);
                post_success(data);
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("dns")){

        var url = $('[name=url]').val();
        var record_type = $('[name=record_type]').val();
        var user_resolver = $('[name=user_resolver]').val();

        $.ajax({
            url: 'dns',
            type: 'post',
            cache: false,
            data: {url: url, record_type: record_type, user_resolver: user_resolver},
            success: function(data) {

                set_query_string('dns?url=' + url + '&record_type=' + record_type + '&user_resolver=' + user_resolver);
                post_success(data);

            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("subnet")){

        var ip_address = $('[name=ip_address]').val();
        var subnet_mask = $('[name=subnet_mask]').val();

        $.ajax({
            url: 'subnet',
            type: 'post',
            cache: false,
            data: {ip_address: ip_address, subnet_mask: subnet_mask},
            success: function(data) {

                set_query_string('subnet?ip_address=' + ip_address + '&subnet_mask=' + subnet_mask);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("oui")){

        var mac_address = $('[name=mac_address]').val();

        $.ajax({
            url: 'oui',
            type: 'post',
            cache: false,
            data: {mac_address: mac_address},
            success: function(data) {

                set_query_string('oui?mac_address=' + mac_address);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("ping")){

        var hostname = $('[name=hostname]').val();

        $.ajax({
            url: 'ping',
            type: 'post',
            cache: false,
            data: {hostname: hostname},
            success: function(data) {

                set_query_string('ping?hostname=' + hostname);
                post_success(data);
            
            },
            error: function() {
                post_failed()
            }
        });

    }else if (classes.contains("traceroute")){

        var hostname = $('[name=hostname]').val();

        $.ajax({
            url: 'traceroute',
            type: 'post',
            cache: false,
            data: {hostname: hostname},
            success: function(data) {

                set_query_string('traceroute?hostname=' + hostname);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });
    }else if (classes.contains("whois")){

        var hostname = $('[name=hostname]').val();

        $.ajax({
            url: 'whois',
            type: 'post',
            cache: false,
            data: {hostname: hostname},
            success: function(data) {

                set_query_string('whois?hostname=' + hostname);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });
    }

}

function post_success(data) {
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
function load_app(app, title) {
    $('#app').load(app + ' #app');
    active($('#' + app + '_nav'));
    document.title = 'NTN - '+ title;
}

// allows bookmarks to function - if the request URL is #app, the app is loaded
function load_anchor() {

    switch ($(location).attr('hash')) {
        case '#curl':
            load_app('curl', 'cURL');
            enable_watch();
            return;
        case '#dns':
            load_app('dns', 'DNS');
            enable_watch();
            return;
        case '#subnet':
            load_app('subnet', 'Subnet');
            return;
        case '#oui':
            load_app('oui', 'OUI');
            return;
        case '#ping':
            load_app('ping', 'Ping');
            enable_watch();
            return;
        case '#traceroute':
            load_app('traceroute', 'Traceroute');
            enable_watch();
            return;
        case '#whois':
            load_app('whois', 'Whois');
            enable_watch();
            return;
    }

    switch ($(location).attr('pathname')) {
        case '/tools/curl':
            enable_watch();
            active($('#curl_nav'));
            return;
        case '/tools/dns':
            enable_watch();
            active($('#dns_nav'));
            return;
        case '/tools/ping':
            enable_watch();
            active($('#ping_nav'));
            return;
        case '/tools/oui':
            active($('#oui_nav'));
            return;
        case '/tools/subnet':
            active($('#subnet_nav'));
            return;
        case '/tools/traceroute':
            enable_watch();
            active($('#traceroute_nav'));
            return;
        case '/tools/whois':
            active($('#whois_nav'));
            return;
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

function set_query_string(url_location) {
    window.history.pushState(null, null, url_location)
}