
//右侧mini排行榜
function getRankList(){
//    var hangye={}
//    var diyu={}
//    var gainian={}
    $.ajax({
        type:'get',
        url:'/stockapi/getRankList',
        success:function (arg) {
             obj = jQuery.parseJSON(arg)
             var hangye = jQuery.parseJSON(obj.hangye)
             var diyu=jQuery.parseJSON(obj.diyu)
             var gainian=jQuery.parseJSON(obj.gainian)
             miniRank(hangye,diyu,gainian)
           },
        error:function(){
            console.log('failed')
        }
    });
};
getRankList()

//左侧自选股列表+ 检查是否已关注该股票
function getFavList(){
    $.ajax({
        type:'get',
        url:'/user/getfav',
        success:function (arg) {
             obj = JSON.parse(arg)
             $('#favlist').text('');
             var favlist=document.getElementById('favlist');
             var stockname = $('#stockname').text();
             var havefollowed = 0
             for(i=0;i<obj.length;i++){
                 if(stockname==obj[i].fields.stockname)
                 {
                    havefollowed=1
                 }
                 var tr=document.createElement("tr");
                 favlist.appendChild(tr);
                 var name=document.createElement("td");
                 tr.appendChild(name);
                 name.innerHTML='<a href="http://127.0.0.1:8000/details/'+obj[i].fields.stockcode+'">'+obj[i].fields.stockname+' '+obj[i].fields.stockcode+'</a>';
             }
             if(havefollowed){
                    $('#followButton').text('-取关');
                    $('#followButton').attr({class:"button is-danger "});
             }else{
                    $('#followButton').text('+关注');
                    $('#followButton').attr({class:"button is-info"});
            }
           },
        error:function(){
            console.log('failed')
        }
    });
};
getFavList()




function miniRank(hangye,diyu,gainian){
//    mini行业排行
   var rankhangye=document.getElementById('hangyeMinRank');
   for (i=0;i<5;i++){
        var tr=document.createElement("tr");
        rankhangye.appendChild(tr);
//        板块
        var name=document.createElement("td");
        tr.appendChild(name);
        name.innerHTML='<a href="#">'+hangye[i].fields.name+'</a>';
//        上涨
        var up=document.createElement("td");
        tr.appendChild(up);
        up.innerHTML=hangye[i].fields.up;
//        下跌
        var down=document.createElement("td");
        tr.appendChild(down);
        down.innerHTML=hangye[i].fields.down;
        down.className='has-text-success'
//        均价
        var avgPrice=document.createElement("td");
        tr.appendChild(avgPrice);
        avgPrice.innerHTML=hangye[i].fields.avgPrice.toFixed(2);
//        涨跌幅
        var avgPchg=document.createElement("td");
        tr.appendChild(avgPchg);
        avgPchg.innerHTML=(hangye[i].fields.avgPchg).toFixed(2)+'%';
//        console.log(100*hangye[i].fields.avgPchg)
        if (hangye[i].fields.avgPchg<0){
            avgPchg.className='has-text-success'
            avgPrice.className='has-text-success'
        }
        }
//        mini地域排行
   var rankdiyu=document.getElementById('diyuMinRank');
   for (i=0;i<5;i++){
        var tr=document.createElement("tr");
        rankdiyu.appendChild(tr);
//        地域名
        var name=document.createElement("td");
        tr.appendChild(name);
        name.innerHTML='<a href="#">'+diyu[i].fields.name+'</a>';
//        上涨
        var up=document.createElement("td");
        tr.appendChild(up);
        up.innerHTML=diyu[i].fields.up;
//        下跌
        var down=document.createElement("td");
        tr.appendChild(down);
        down.innerHTML=diyu[i].fields.down;
        down.className='has-text-success'
//        均价
        var avgPrice=document.createElement("td");
        tr.appendChild(avgPrice);
        avgPrice.innerHTML=diyu[i].fields.avgPrice.toFixed(2);
//        涨跌幅
        var avgPchg=document.createElement("td");
        tr.appendChild(avgPchg);
        avgPchg.innerHTML=(diyu[i].fields.avgPchg).toFixed(2)+'%';
        if (diyu[i].fields.avgPchg<0){
            avgPchg.className='has-text-success'
            avgPrice.className='has-text-success'
        }

   }
//   mini概念排行
   var rankgainian=document.getElementById('gainianMinRank');
   for (i=0;i<5;i++){
        var tr=document.createElement("tr");
        rankgainian.appendChild(tr);
//        板块名
        var name=document.createElement("td");
        tr.appendChild(name);
        name.innerHTML='<a href="#">'+gainian[i].fields.name+'</a>';
//        上涨
        var up=document.createElement("td");
        tr.appendChild(up);
        up.innerHTML=gainian[i].fields.up;
//        下跌
        var down=document.createElement("td");
        tr.appendChild(down);
        down.innerHTML=gainian[i].fields.down;
        down.className='has-text-success'
//        均价
        var avgPrice=document.createElement("td");
        tr.appendChild(avgPrice);
        avgPrice.innerHTML=gainian[i].fields.avgPrice.toFixed(2);
//        涨跌幅
        var avgPchg=document.createElement("td");
        tr.appendChild(avgPchg);
        avgPchg.innerHTML=(gainian[i].fields.avgPchg).toFixed(2)+'%';

        if (gainian[i].fields.avgPchg<0){
            avgPchg.className='has-text-success'
            avgPrice.className='has-text-success'
        }
        }
};


//板块排行榜nav点击事件
function hangyeRank(){
    $('#hangyetab').attr({class:"navbar-item is-tab is-active"});
    $('#diyutab').attr({class:"navbar-item is-tab "});
    $('#gainiantab').attr({class:"navbar-item is-tab "});
}
function gainianRank(){

    $('#hangyetab').attr({class:"navbar-item is-tab "});
    $('#diyutab').attr({class:"navbar-item is-tab "});
    $('#gainiantab').attr({class:"navbar-item is-tab is-active"});
}
function diyuRank(){

    $('#hangyetab').attr({class:"navbar-item is-tab "});
    $('#diyutab').attr({class:"navbar-item is-tab is-active"});
    $('#gainiantab').attr({class:"navbar-item is-tab "});
}


$('#searchfields').mouseover(function(){
    var temp = $('#searchfields').val();
    if (temp==''){
     $('#searchDropdown').attr({class:"dropdown"});
    }else{
    $('#searchDropdown').attr({class:"dropdown is-active"});
    }
})

$(document).click(function(){
    $('#searchDropdown').attr({class:"dropdown"});
});

//搜索框
 $('#searchfields').on('input',function(){

        var temp = $('#searchfields').val();
        if (temp==''){
         $('#searchDropdown').attr({class:"dropdown"});
        }
        else{
            $('#searchDropdown').attr({class:"dropdown is-active"});
            $.ajax({
                url:'/stockapi/search',
                type:'POST',
                data:{stock:temp},
                success:function(arg){
                    obj = jQuery.parseJSON(arg)
                    var dropdown=document.getElementById('dropdown-menu');
                    if(obj.statuscode == 0){
                        dropdown.innerHTML='<p class="dropdown-item">暂时没有找到符合条件的结果</p>';
                    }
                    if(obj.statuscode == 1){
                        dropdown.innerHTML='';
                        var searchlist = JSON.parse(arg)
                        var list=JSON.parse(searchlist.list)
                        for(i=0;i<list.length;i++){
                            var stockname=document.createElement("p");
                            dropdown.appendChild(stockname);
                            stockname.innerHTML='<a href="/details/'+list[i].fields.stockcode+'" class="dropdown-item">'+list[i].fields.stockname+'</a>';
                        }
                    }
                },
                error:function(){
                    console.log('search failed')
                }
            });
        }
 });


