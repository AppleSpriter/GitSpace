//主要用来进行关注/取消关注　弹窗处理
function Overchange(tar)
{
    if(document.getElementById(tar.id).value=="已关注")
    {   
        // alert(tar.id);

        document.getElementById(tar.id).value="取消关注";
                    var a = document.getElementById(tar.id);
                    a.style.background='rgba(47,166,183,1)';                    
    }
    else
    {
                    document.getElementById(tar.id).value="＋关注";
                    var a = document.getElementById(tar.id);
                    a.style.background='rgba(7,166,83,1)';    
    }
};


function Outchange(tar)
{
    if(document.getElementById(tar.id).value=="取消关注")
    {
        document.getElementById(tar.id).value="已关注";
        var a = document.getElementById(tar.id);
        a.style.background='rgba(7,166,83,1)';
    }else
    {   
        if(document.getElementById(tar.id).value=="已关注")
        {
            document.getElementById(tar.id).value="已关注"
        }else 
            {

                        var a = document.getElementById(tar.id);
                        a.style.background='rgba(47,166,183,1)'; 
            }
    }
};


function Clikchange(tar)
{
    if(document.getElementById(tar.id).value=="＋关注")
    {
        
        document.getElementById(tar.id).value="已关注"
                    var a = document.getElementById(tar.id);
                    a.style.background='rgba(7,166,83,1)';                  
    }
    else
    {
    if(document.getElementById(tar.id).value=="已关注")
    {
        document.getElementById(tar.id).value="已关注"
                    var a = document.getElementById(tar.id);
                    a.style.background='rgba(7,166,83,1)';                  
    } else               
    document.getElementById(tar.id).value="＋关注"
    }
};




// 判断数组中包含element元素
         Array.prototype.contains = function (element) {
         
            for (var i = 0; i < this.length; i++) {
                if (this[i] == element) {
                    return true;
                }
            }
            return false;
        }

//以下是对于弹出小窗口的升级方法
        var split = function(tar){//分割函数
            var s = tar.id.split("");
            var end = s[s.length-1];
            if(end%2==1){
                return true;
            }else{
                return false;
            }
        };

        var shap = function(tar){//变形函数
            var s = tar.id.split("");
            var end = s[s.length-1];
            end++;
            var start = tar.id.substring(0,3);
            var merge = start+end;
            return merge;   
        };

function OverT(tar){
    var outside = document.getElementById(tar.id);
    var judge = split(tar);
    if(judge){
        var insideId = shap(tar);
        var inside = document.getElementById(insideId);
        inside.style.display = "block";
    }
};
function OutT(tar){
    var outside = document.getElementById(tar.id);
    var judge = split(tar);
    if(judge){
        var insideId = shap(tar);
        var inside = document.getElementById(insideId);
        inside.style.display = "none";
    }
};

function ClikT(tar){
    var outside = document.getElementById(tar.id);
    var judge = split(tar);
    if(judge){
        var insideId = shap(tar);
        var inside = document.getElementById(insideId);
        inside.style.display = "none";
    }
};
