function ShowLoginText(){
    layer.open({
        type:1,
        title:"登录",
        area:["395px","300px"],
        content:$("#loginBox"),
        });
    }
function Login(){
    var username=$.trim($("#InputUsername").val());//获取用户名trim是去掉空格
    var password=$.trim($("#InputUserPwd").val());//获取密码
    if(username==""||password==""){
        layer.alert("用户名或者密码不能为空!",{
        title:"提示",
        icon:5, 
        });
    }
}


function tanchu(){
    document.getElementById('dynamic').style.display='block';
    document.getElementById('fade').style.display='block';
}
function tanchu2(){
    document.getElementById('dynamic').style.display='none';
    document.getElementById('fade').style.display='none';
}

function tanchu3(){
    document.getElementById('idea').style.display='block';
    document.getElementById('fade').style.display='block';
}
function tanchu4(){
    document.getElementById('idea').style.display='none';
    document.getElementById('fade').style.display='none';
}

// -----------------------------------------------------------------
function dynamicComment(dynamicID){
    var ucomment = document.getElementById('ucomment').value;
    $.ajax({
        type: 'POST',
        url: '/indexComment/',
        data: {'dynamicID':dynamicID,'switch':'dynamicComment','ucomment':ucomment},

        success: function(data) {
            data = JSON.parse(data);
            if (data['result'] == 1) {
                alert('评论成功');
                $('#CommentsContainer').html("");
                $('#CommentsContainer').html(data['num']+'条评论');
                $('#commentList').html("");

                for(var i=0;i<data['num'];i++){

                    var str='<div class="commentItem">' +
                    '<div> ' +
                    data['dynamicComment'][i]['commentUser'] +
                    ':'+data['dynamicComment'][i]['commentContent'] +
                    '<div style="float:right;">' +
                    data['dynamicComment'][i]['commentTime'] +
                    '</div>'+
                    '</div>';

                    $('#commentList').append(str);

                }
            }else{
                alert('fuck')
            }
        },
        error: function() {
            alert('fuck，请过会儿再试试');
        }
    });
}
function dynamicCommentTanchu(dynamicID){
    // 动态评论弹出显示
    document.getElementById('light').style.display='block';
    document.getElementById('fade').style.display='block';

    $.ajax({
        type: 'POST',
        url: '/switch/',
        data: {'dynamicID':dynamicID,'switch':'dynamicComment'},

        success: function(data) {
            data = JSON.parse(data);
            if (data['num'] == 0) {
                $('#CommentsContainer').html(data['num']+'条评论');
                $('#commentList').html("");
                alert('快抢沙发');

                $('#commentsFooter').html("");
                var str ='<input type="text" id="ucomment" name="ucomment" class="commentcontent">' + 
                '<input type="submit" name="submit1" class="commentinput" value="评论" onclick="dynamicComment(' + 
                dynamicID +
                ')">' ; 
                $('#commentsFooter').append(str);

            }else{
                $('#CommentsContainer').html(data['num']+'条评论');
                $('#commentList').html("");

                for(var i=0;i<data['num'];i++){

                    var str='<div class="commentItem">' +
                    '<div> ' +
                    data['dynamicComment'][i]['commentUser'] +
                    ':'+data['dynamicComment'][i]['commentContent'] +
                    '<div style="float:right;">' +
                    data['dynamicComment'][i]['commentTime'] +
                    '</div>'+
                    '</div>';

                    $('#commentList').append(str);

                }

                $('#commentsFooter').html("");
                var str ='<input type="text" id="ucomment" name="ucomment" class="commentcontent">' + 
                '<input type="submit" name="submit1" class="commentinput" value="评论" onclick="dynamicComment(' + 
                dynamicID +
                ')">' ; 
                $('#commentsFooter').append(str);


             
                // alert('显示评论成功');
            }
            
        },
        error: function() {
            alert('fuck，请过会儿再试试');
        }
    });

    return false;
}
function commentTanchu2(){
    document.getElementById('light').style.display='none';
    document.getElementById('fade').style.display='none';
}

function dynamicThumup(dynamicID){
    // 动态点赞

    $.ajax({
        type: 'POST',
        url: '/switch/',
        data: {'dynamicID':dynamicID,'switch':'dynamicThumUp'},

        success: function(data) {
            data = JSON.parse(data);
            if (data['result'] == 1) {
                alert('已点赞');
            }else if(data['result'] == 0){
                alert('点赞成功')
            }else{
                alert('fuck')
            }
        },
        error: function() {
            alert('保存失败，请过会儿再试试');
        }
    });

}

function articleThumbUp(articleID){
    // 文章点赞
    
    $.ajax({
        type: 'POST',
        url: '/switch/',
        data: {'articleID':articleID,'switch':'articleThumbUp'},

        success: function(data) {
            data = JSON.parse(data);
            if (data['result'] == 1) {
                alert('已点赞');
            }else if(data['result'] == 0){
                alert('点赞成功')
            }else{
                alert('fuck')
            }
        },
        error: function() {
            alert('保存失败，请过会儿再试试');
        }
    });
}
function ideaThumbUp(ideaID){
    // 想法点赞
    
    $.ajax({
        type: 'POST',
        url: '/switch/',
        data: {'ideaID':ideaID,'switch':'ideaThumbUp'},

        success: function(data) {
            data = JSON.parse(data);
            if (data['result'] == 1) {
                alert('已点赞');
            }else if(data['result'] == 0){
                alert('点赞成功')
            }else{
                alert('fuck')
            }
        },
        error: function() {
            alert('保存失败，请过会儿再试试');
        }
    });

}
function articleCollection(articleID){
    // 文章收藏
    
    $.ajax({
        type: 'POST',
        url: '/switch/',
        data: {'articleID':articleID,'switch':'articleCollection'},

        success: function(data) {
            data = JSON.parse(data);
            if (data['result'] == 1) {
                alert('已收藏');
            }else if(data['result'] == 0){
                alert('收藏成功')
            }else{
                alert('fuck')
            }
        },
        error: function() {
            alert('保存失败，请过会儿再试试');
        }
    });
}
function ideaCollection(ideaID){
    // 想法收藏
    
    $.ajax({
        type: 'POST',
        url: '/switch/',
        data: {'ideaID':ideaID,'switch':'ideaCollection'},

        success: function(data) {
            data = JSON.parse(data);
            if (data['result'] == 1) {
                alert('已收藏');
            }else if(data['result'] == 0){
                alert('收藏成功')
            }else{
                alert('fuck')
            }
        },
        error: function() {
            alert('保存失败，请过会儿再试试');
        }
    });
}
