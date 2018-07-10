$('navi a').on('click', function(e) {                 
 2   e.preventDefault();  // 阻止链接跳转
 3   var url = this.href;  // 保存点击的地址
 4 
 5   $('nav a.hot').removeClass('hot');    
 6   $(this).addClass('hot');                       
 7 
 // 8   $('.recommends').remove();                          
 9   $('.recommends').load(url + ' #recommends').fadeIn('slow'); 
10 });


function makeComments(){
 if (document.getElementById('test').style.display=='block'){
        document.getElementById('test').style.display='none';
    }
else{
    document.getElementById('test').style.display='block';
    }   
};
