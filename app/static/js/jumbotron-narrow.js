$(function () {
	jump_tag();
	next_page();
});

function jump_tag() {
	$('.room').on({
		mouseover: function(e) {
			$(this).find('.jump').css('visibility', 'visible');
			$(this).css('border', '2px dashed #C3BDCC');
		},
		mouseout: function(e) {
			$(this).find('.jump').css('visibility', 'hidden');
			$(this).css('border', '0px');
		}
	});
}

function next_page() {
	$(window).on('scroll',function() {
		var last_id = $('#last_id').attr('value');
  		if (scrollTop() + windowHeight() >= documentHeight()) {
	  		$.getJSON("/tv/rooms", {last_id:last_id}, function(json){ 
	            if (json) {
	            	if (json.data) {
		            	fill_page(json);
		            	$('#last_id').attr('value', parseInt(last_id) + 10);
	            	} else {
	            		alert('没有更多的数据了!!!');
	            	}
	            } 
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
  return (document.compatMode == "CSS1Compat")?
  document.documentElement.clientHeight:
  document.body.clientHeight;
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
	jump_tag();
}