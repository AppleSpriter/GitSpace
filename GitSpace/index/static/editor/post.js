function publish() {
    save(1);
}

function draft() {
    save(0);
    checkcodeRefesh();
}

function save(isPub) {

    if (!checkForm()) return;

    var data = getPostData();
    data['isPub'] = isPub;
    console.log(data);
    data["csrfmiddlewaretoken"] = $('[name="csrfmiddlewaretoken"]').val();

    var link = '/postnew/save/';

    $.ajax({
        type: 'POST',
        url: link,
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        data: data,
        success: function(ret) {
            var retData = JSON.parse(ret);
            if (retData['result'] == 0) {
                alert("文章发布失败")
            } else {
                if (!isPub) {
                    alert("文章已保存")
                } else {
                    alert('文章发布成功');
                    if (retData['artl-id'] == 0) { /*如果不是编辑*/
                        $("#txtTitle").val('');
                        //编辑区清空
                        $("#editor").val('');
                    }
                }
            }
        },
        error: function() {
            alert('保存失败，请过会儿再试试');
        }
    });

}

function checkTitle(e) {
    var v = $.trim(((typeof e == "string") ? $("#" + e) : e).val());
    return (v != "" && v != "请选择");
}

function getTitle(e) {
    var v = $.trim(((typeof e == "string") ? $("#" + e) : e).val());
    return v;
}

function checkForm() {
    if ($("#selType").val() == '0') {
        alert("请选择文章类型");
        return false;
    }
    if (!checkTitle("txtTitle")) {
        alert("请输入文章标题");
        return false;
    }

    var con = editor1.txt.html();
    if (!$.trim(con)) {
        alert("请输入文章内容");
        return false;
    }
    if ($('#radChl').val() == 0) {
        alert("请选择文章标签");
        return false;
    }
    return true;
}

function getPostData() {
    var type = $("#selType").val();
    var titl = getTitle("txtTitle");
    var cont = "";
    //cont = encodeURIComponent(csdn.val("editor").replace(/<a\s/gi, '<a target=_blank '));
    var chnl = $('#Alabels').val();

    var chnlInt = 0;

    if (chnl == null) {
        chnlInt = 0;
    } else {
        for (i in chnl) {
            chnlInt |= 1 << i;
        }
    }

    var des = $('#article-des').val();

    var data = {
        'titl': titl,
        'cont': editor1.txt.html(),
        'type': type,
        'labl': chnlInt,
        'des': des,
        'privt': $('#chkIsHasNotify').is(':checked')
    }

    return data;
}