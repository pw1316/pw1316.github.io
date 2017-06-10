//jquery
$(document).ready(function(){

	$(".dropdown").hover(
	function(){
		$(this).addClass("hover");
	},
	function(){
		$(this).removeClass("hover");
	});

	//当滚动条的位置处于距顶部100像素以下时，跳转链接出现，否则消失
	$(function() {
		$(window).scroll(function() {
			if ($(window).scrollTop() > 100) {
				$(".scrollbar").fadeIn();
			} else {
				$(".scrollbar").fadeOut();
			}
		});
		//当点击跳转链接后，回到页面顶部位置
		$(".scrolltop").click(function() {
			$('body,html').animate({
				scrollTop: 0
			},
			500);
			return false;
		});
	});
	$("[tips]").mouseover(function(){
		layer.tips($(this).attr("tips"), this, {
			tips: [1, '#000']
		});
	}).mouseout(function(){
		layer.closeAll('tips');
	})
});
//editor
function editor(o){
	var start=0, end=0, len=0;
	obj = document.getElementById('comment');
	obj.focus();
	var e = o.replace(/\[/ig,'[/');
	if (e.indexOf('-')>-1){
		e = '';
	}else if (e.indexOf('=')>-1){
		e = e.replace(/(.*?)\=.*?(\])/,'$1$2');
	}
	//focus start
	start = obj.selectionStart;
	//focus end
	end = obj.selectionEnd;
	//selected
	//sel = window.getSelection();
	sel = obj.value.substring(start,end);
	//front str
	front = obj.value.substr(0,start);
	//back str
	back = obj.value.substring(end);
	//rewrite str
	obj.value = front + o + sel + e + back;
	//focus
	document.getElementById('comment').setSelectionRange(start+o.length,end+o.length);
}
//emot
function emot(o){
	var start=0, end=0, len=0;
	obj = document.getElementById('comment');
	obj.focus();
	//for other
	start = obj.selectionStart;
	end = obj.selectionEnd;
	sel = obj.value.substring(start,end);
	front = obj.value.substr(0,start);
	back = obj.value.substring(end);
	obj.value = front + sel + o + back;
	obj.setSelectionRange(start+o.length,end+o.length);
}

//reply
function reply(e){
	box = document.getElementById('comment');
	oc = box.value;
	prefix = '@' + e + ' ';
	nc = oc + prefix;
	box.focus();
	box.value = nc;
}
//open & closed
function change(e){
	$("#"+e).toggle();
}
function updown(obj,type,param,updown){
	if(updown=='up'){
		var txt = '顶';
		var conf = '要付出4铜币来顶一下吗？';
	}else if(updown == 'down'){
		var txt = '踩';
		var conf = '确定要踩吗？';
	}else{
		layer.msg('参数有雾');
	}
	layer.confirm(conf,{},function(index){
		$.ajax({
			type:'POST',
			url:u+'/set/updown/post',
			data:{"type":type,"param":param,"updown":updown},
			success:function(data){
				obj.innerHTML = '已'+txt;
			},
			error:function(a){
				layer.msg(a.responseText);
			}
		});
		layer.close(index);
	});
}
function fav(obj,type,param){
	layer.confirm('确定要收藏吗？',{},function(index){
		$.ajax({
			type:'POST',
			url:u+'/set/fav/post',
			data:{"type":type,"param":param},
			success:function(data){
				obj.innerHTML = '已收藏';
			},
			error:function(a){
				layer.msg(a.responseText);
			}
		});
		layer.close(index);
	});
}

//close gene
function closegene(geneid){
	layer.confirm('真要删除这个机因吗？此操作不可逆',{},function(index){
		$.ajax({
			type:'POST',
			url:u+'/set/closegene/post',
			data:{"geneid":geneid},
			success:function(data){
				if(data=='1'){
					window.location.replace(u+'/gene/'+geneid);
				}else{
					layer.msg(data);
				}
			},
		});
	});
}

//close trade
function closetrade(tradeid){
	layer.confirm('关闭后这个交易信息将无法再打开，确定要关闭吗？',{},function(index){
		$.ajax({
			type:'POST',
			url:u+'/set/closetrade/post',
			data:{"tradeid":tradeid},
			success:function(data){
				if(data=='1'){
					window.location.replace(u+'/trade/'+tradeid);
				}else{
					layer.msg(data);
				}
			},
		});
	});
}

//up trade
function uptrade(tradeid){
	layer.confirm('每隔12小时只能打捞一次，确定要打捞么？',{},function(index){
		$.ajax({
			type:'POST',
			url:u+'/set/uptrade/post',
			data:{"tradeid":tradeid},
			success:function(data){
				if(data=='1'){
					layer.msg('打捞成功，2秒后跳转',{time:2000}, function(){
						window.location.replace(u+'/trade');
					});
				}else{
					layer.msg(data);
				}
			},
		});
	});
}

//qidao
function qidao(obj){
	$(obj).hide();
	layer.open({
		type: 2,
		title: '祈祷',
		shadeClose: true,
		area: ['280px', '250px'],
		content: u+'/set/qidao/post'
	});
}

//store
function store(id, server){
	if(server=='cn'){
		param = 'CN/zh';
		uparam = 'zh-hans-cn';
	}else if(server=='hk'){
		param = 'HK/zh';
		uparam = 'zh-hans-hk';
	}else if(server=='jp'){
		param = 'JP/ja';
		uparam = 'ja-jp';
	}else if(server=='us'){
		param = 'US/en';
		uparam = 'en-us';
	}
	url = 'https://store.playstation.com/store/api/chihiro/00_09_000/container/'+ param +'/999/' + id;
	$.ajax({
		url: url,
		dataType: 'json',
		beforeSend: function(){
			var load = layer.load();
		},
		success: function(data){
			var img = '';
			var plus = '';
			var skuname = '';
			var reledate = '';
			var price = '';
			var cover = '';
			var links = '';
			var genre = '';
			if(!jQuery.isEmptyObject(data.promomedia[1])){
				if(!jQuery.isEmptyObject(data.promomedia[1].materials)){
					if(!jQuery.isEmptyObject(data.promomedia[1].materials[0].urls)){
						$.each(data.promomedia[1].materials, function(i, item) {
							img += '<br /><img src="'+item.urls[0].url+'" />';
						});
					}
				}
			}else if(!jQuery.isEmptyObject(data.promomedia[0])){
				if(!jQuery.isEmptyObject(data.promomedia[0].materials[0].urls)){
					$.each(data.promomedia[0].materials, function(i, item) {
						img += '<br /><img src="'+item.urls[0].url+'" />';
					});
				}
			}
			if(!jQuery.isEmptyObject(data.default_sku)){
				if(!jQuery.isEmptyObject(data.default_sku.rewards)){
					plus = '<em>　-　折扣价：</em><span class="text-warning">'+data.default_sku.rewards[0].display_price+'</span>（'+data.default_sku.rewards[0].discount+'% Off）';
				}

				if(!jQuery.isEmptyObject(data.default_sku.name)){
					skuname = data.default_sku.name;
					price = data.default_sku.display_price;
				}
			}
			if(!jQuery.isEmptyObject(data.images)){
				cover = data.images[0].url;
			}
			if(!jQuery.isEmptyObject(data.links)){
				links = '<div class="hd3">关联内容</div><ul class="storebg storelist">';
				$.each(data.links, function(i, item) {
					links += '<li><div class="pd10"><p align="center"><a href="javascript:void(0)" onclick="store(\''+item.id+'\',\''+server+'\')"><img src="'+item.images[2].url+'" width="160" height="160" /></a></p>';
					links += '<div class="lh180">';
					links += item.name;
					if(!jQuery.isEmptyObject(item.game_contentType)){
					links += '<br /><em>类别：</em>'+item.game_contentType;
					}
					if(!jQuery.isEmptyObject(item.release_date)){
					links += '<br /><em>发行：</em>'+item.release_date;
					}
					if(!jQuery.isEmptyObject(item.default_sku)){
					links += '<br /><em>售价：</em>'+item.default_sku.display_price;
					links += '<br /><em>备注：</em>'+item.default_sku.name;
					}
					links += '</div></div></li>';
				});
				links += '<div class="clear"></div></ul>';
			}
			if(!jQuery.isEmptyObject(data.metadata.genre)){
				genre = '<em>　-　类型：</em>'+data.metadata.genre.values
			}
			if(!jQuery.isEmptyObject(data.release_date)){
				reledate = '<em>发行日期</em>：'+data.release_date
			}
			layer.closeAll('loading');
			layer.open({
				title: false,
				type: 1,
				scrollbar: false,
				//shadeClose: true,
				area: ['90%', '80%'],
				content:'<div class="storebg content pd20"><img src="'+cover+'" class="pd10 r h-p" /><h1 class="pb10">'+data.name+'&nbsp;<em>'+skuname+'</em></h1><p><a href="https://store.playstation.com/#!/cid='+data.id+'" target="_blank">去官方商城（PlayStation Store）购买</a></p><p><em>分类：</em>'+data.game_contentType+'</p><p>'+reledate+'<em>　-　发行商：</em>'+data.provider_name+'</p><p><em>平台</em>：'+data.playable_platform+genre+'</p><p><em>零售价</em>：'+price+plus+'</p><div class="pd10">'+data.long_desc+'</div>'+img+'</div>'+links 
			});
		},
		error: function(){
			//关掉所有loading层
			layer.closeAll('loading');
			layer.msg('商品已下架');
		}
	});
}

//修复按钮提交的BUG
if(!+"\v1"){
	window.attachEvent("onload", function(){
	var buttons = document.getElementsByTagName('button');
	for (var i=0; i<buttons.length; i++) {
		if(buttons[i].onclick) continue;
		buttons[i].onclick = function () {
			for(var j=0,n=this.form.elements.length; j<n; j++)
			if( this.form.elements[j].tagName == 'BUTTON' )
				this.form.elements[j].disabled = true;
				this.disabled=false;
				this.value = this.attributes["value"].nodeValue ;
			}
		}
	});
}
//阻止冒泡的方法
function stopPP(e){
	var evt = e || window.event;
	//IE用cancelBubble=true来阻止而FF下需要用stopPropagation方法
	evt.stopPropagation ? evt.stopPropagation() : (evt.cancelBubble=true);
}