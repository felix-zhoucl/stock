function refresh(){
    $.ajax({
        type:'get',
        url:'http://api.money.126.net/data/feed/0000001,UD_SHAZ,UD_SHAP,UD_SHAD,1399001,UD_SZAZ,UD_SZAP,UD_SZAD,1399300,UD_HS3Z,UD_HS3P,UD_HS3D',
        dataType : "jsonp",
        jsonp: "jsonpCallback",
        jsonpCallback:"_ntes_quote_callback",
        success:function (arg) {
//            console.log(arg);
            //上证指数
            $('#shzs').text(arg['0000001'].price+' (' +arg['0000001'].updown+ ') '+Math.round(arg['0000001'].turnover/100000000)+'亿');
            if (arg['0000001'.updwon]>0){
                $('#shzs').attr({class:" tile is-size-7 has-text-danger"});
                }
                else{
                $('#shzs').attr({class:"tile is-size-7  has-text-success"});
                }
            $('#shzhang').text(arg.UD_SHAZ.count);
            $('#shping').text(arg.UD_SHAP.count);
            $('#shdie').text(arg.UD_SHAD.count);
            //深证指数
            $('#szzs').text(arg['1399001'].price+' (' +arg['1399001'].updown+ ') '+Math.round(arg['1399001'].turnover/100000000)+'亿');
            if (arg['1399001'.updwon]>0){
                $('#szzs').attr({class:" tile is-size-7 has-text-danger"});
                }
                else{
                $('#szzs').attr({class:"tile is-size-7  has-text-success"});
                }
            $('#szzhang').text(arg.UD_SZAZ.count);
            $('#szping').text(arg.UD_SZAP.count);
            $('#szdie').text(arg.UD_SZAD.count);
            //沪深300
             $('#hszs').text(arg['1399300'].price+' (' +arg['1399300'].updown+ ') '+Math.round(arg['1399300'].turnover/100000000)+'亿');
            if (arg['1399300'.updwon]>0){
                $('#hszs').attr({class:" tile is-size-7 has-text-danger"});
                }
                else{
                $('#hszs').attr({class:"tile is-size-7  has-text-success"});
                }
            $('#hszhang').text(arg.UD_HS3Z.count);
            $('#hsping').text(arg.UD_HS3P.count);
            $('#hsdie').text(arg.UD_HS3D.count);
            },
        error:function(){
            console.log('failed')
        }
    });
};
refresh()
//定时
setInterval('refresh()',5000)


function sha(){
    $('#hsa').attr({class:"navbar-item is-tab"});
    $('#sha').attr({class:"navbar-item is-tab is-active"});
    $('#sza').attr({class:"navbar-item is-tab"});
    $('#zxb').attr({class:"navbar-item is-tab"});
    $('#kcb').attr({class:"navbar-item is-tab"});
    $('#hsb').attr({class:"navbar-item is-tab"});
}

function sza(){
    $('#hsa').attr({class:"navbar-item is-tab"});
    $('#sha').attr({class:"navbar-item is-tab"});
    $('#sza').attr({class:"navbar-item is-tab is-active"});
    $('#zxb').attr({class:"navbar-item is-tab"});
    $('#kcb').attr({class:"navbar-item is-tab"});
    $('#hsb').attr({class:"navbar-item is-tab"});
}

function zxb(){
    $('#hsa').attr({class:"navbar-item is-tab"});
    $('#sha').attr({class:"navbar-item is-tab"});
    $('#sza').attr({class:"navbar-item is-tab"});
    $('#zxb').attr({class:"navbar-item is-tab is-active"});
    $('#kcb').attr({class:"navbar-item is-tab"});
    $('#hsb').attr({class:"navbar-item is-tab"});
}
function kcb(){
    $('#hsa').attr({class:"navbar-item is-tab"});
    $('#sha').attr({class:"navbar-item is-tab"});
    $('#sza').attr({class:"navbar-item is-tab"});
    $('#zxb').attr({class:"navbar-item is-tab"});
    $('#kcb').attr({class:"navbar-item is-tab is-active"});
    $('#hsb').attr({class:"navbar-item is-tab"});
}
function hsb(){
    $('#hsa').attr({class:"navbar-item is-tab"});
    $('#sha').attr({class:"navbar-item is-tab"});
    $('#sza').attr({class:"navbar-item is-tab"});
    $('#zxb').attr({class:"navbar-item is-tab"});
    $('#kcb').attr({class:"navbar-item is-tab"});
    $('#hsb').attr({class:"navbar-item is-tab is-active"});
}