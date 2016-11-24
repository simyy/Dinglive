$(function () {
    jump_tag();
    next_page();
    $('#searchBtn').click(function() {
        var str = $('#searchStr').val();
        if (str.length == 0) {
            return;
        }
        window.location.href = '/search/' + str;
    });
    $('.carousel').carousel({
        interval: 2000
    })
});

var stop = false;

function jump_tag() {
    $('.room').on({
        mouseover: function(e) {
            $(this).find('.jump').css('visibility', 'visible');
            $(this).css('border', '2px dashed #C3BDCC');
            $(this).css('transition', 'ease-out 0.1s');
            $(this).css('transform', 'scale(1.02)');
            $(this).css('-ms-transform', 'scale(1.02)');
            $(this).css('-moz-transform', 'scale(1.02)');
            $(this).css('-webkit-transform', 'scale(1.02)');
        },
        mouseout: function(e) {
            $(this).find('.jump').css('visibility', 'hidden');
            $(this).css('border', '0px');
            $(this).css('transition', 'ease-out 0.1s');
            $(this).css('transform', 'scale(1)');
            $(this).css('-ms-transform', 'scale(1)');
            $(this).css('-moz-transform', 'scale(1)');
            $(this).css('-webkit-transform', 'scale(1)');
        }
    });
}

function next_page() {
    $(window).on('scroll',function() {
        var page = $('#page').attr('value');
        if (scrollTop() + windowHeight() == documentHeight() && stop == false) {
            stop = true;
            load_start();
            var pattern = new RegExp(".*\/cate\/(.+)?");
            if (window.location.href.match(pattern) == null)
                url = "/tv/cate/all/list"
            else
                url = "/tv/cate/" + window.location.href.match(pattern)[1] + "/list";

            var params = {page: page};

            pattern = new RegExp(".*\/search\/(.+)?");
            if (window.location.href.match(pattern) != null) {
                var searchStr = window.location.href.match(pattern)[1];
                console.log(decodeURI(searchStr))
                params = {page: page, searchStr: decodeURI(searchStr)}
            }

            $.getJSON(url, params, function(json) {
                if (json) {
                    if (json.data.length > 0) {
                        console.log(123)
                        fill_page(json);
                        $('#page').attr('value', parseInt(page) + 1);
                        stop = false;
                    } else {
                        alert('没有更多的数据了!!!');
                    }
                }
                load_end();
            });
        }
    });
}

//获取页面顶部被卷起来的高度
function scrollTop(){
    return Math.max(
        //chrome
        document.body.scrollTop,
        //firefox/IE
        document.documentElement.scrollTop);
}

 //获取页面文档的总高度
function documentHeight(){
    //现代浏览器（IE9+和其他浏览器）和IE8的document.body.scrollHeight和document.documentElement.scrollHeight都可以
    return Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);
}

//获取页面浏览器视口的高度
function windowHeight(){
    return (document.compatMode == "CSS1Compat") ? document.documentElement.clientHeight : document.body.clientHeight;
}

function fill_page(json) {
    for (var i = 0; i < json.data.length; i++) {
        if (i % 4 == 0)
            json.data[i].bg_color = 'bg-success';
        else if (i % 4 == 1)
            json.data[i].bg_color = 'bg-info';
        else if (i % 4 == 2)
            json.data[i].bg_color = 'bg-warning';
        else
            json.data[i].bg_color = 'bg-danger';
    }
    var x = tmpl("tmpl-page", json);
    $('.marketing').append(x);
    $('#div_' + json.data[0].id).fadeIn();
    jump_tag();
}

function load_start() {
    $('.loader').css('display', 'block');
}

function load_end() {
    $('.loader').css('display', 'none');
}

