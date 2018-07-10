function tanchu(){
    document.getElementById('deleteIdeaMember').style.display='block';
    document.getElementById('fade').style.display='block';
}

function tanchu2(){
    document.getElementById('deleteIdeaMember').style.display='none';
    document.getElementById('fade').style.display='none';
}

function antianalyse(){
    var dic = {
                    1:'java',
                    2:'c',
                    4:'c++',
                    8:'python',
                    16:'大数据',
                    32:'人工智能',
                    64:'游戏开发',
                    128:'编程学习'
    };
                var str = "想法";
                    for(var i = 1;i<=128;i=i*2)
                    {
                     if(({{s.label}}&i) == i)
                     str+=","+dic[i]
                    }
                document.getElementById("idea{{s.ideaID}}").innerHTML = str;
}

