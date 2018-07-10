$("#radChl").multiselect({
    noneSelectedText : "--请选择--", //当没有内容选中时候显示的文本
    checkAllText : "全选", //全选按钮显示的文本
    uncheckAllText : "全不选", //全不选按钮显示的文本
    minWidth : 200, //select框的宽度，根据option的内容长短设置
    selectedList : 2 //当选中的内容超过2条时，显示“n已选择”
});
