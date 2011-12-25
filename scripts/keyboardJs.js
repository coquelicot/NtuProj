var lstNewLine, keyCnt = 0;
function replace(ob, lpos, rpos, str){
    var len = str.length;
    var lpart = ob.value.substring(0, lpos);
    var rpart = ob.value.substring(rpos, ob.value.length);
    ob.value = lpart + str + rpart;
    ob.setSelectionRange(lpos + len, lpos + len);
}
function codeClick(num){
    var i=num;
    clearCode(i);
    copy();
    return false;
}
function keyPress(e){
    keyupCheck(e);
    word_count_fn();
    var ob = document.getElementById('code');
    var pos = ob.selectionStart;
    
    //ob.value=add_color(ob,pos);
}
function keyCheck(e){
    keyCnt++;
    if(e.ctrl || (e.which != 9 && e.which != 13)){
        setCopy();
        return true;
    }
    var ob = document.getElementById('realCode');
    var pos = ob.selectionStart, recScroll = ob.scrollTop;
    if(e.which == 9) replace(ob, pos, pos, "\t");
    else if(e.which == 13){
        lstNewLine = keyCnt;
        var npos, str = "\n", lim = pos;
        if(pos > 0 && ob.value[pos - 1] == '{' && ob.value[pos] != '}') str += "\t";
        for(npos = pos; npos > 0 && ob.value[npos - 1] != '\n'; npos--);
        while(ob.value[npos] == "\t" && lim > npos) npos++, str += "\t";
        replace(ob, pos, pos, str);
        if(ob.selectionStart == ob.value.length){
            var get = ob.scrollHeight - ob.style.height.substring(0, ob.style.height.length - 2);
            if(recScroll < get) recScroll = get;
        }
    }
    ob.scrollTop = recScroll;
    setCopy();
    return false;
}
function keyupCheck(e){
    var ob = document.getElementById('realCode');
    var pos = ob.selectionStart;
    if(!e.ctrl && e.which == 221 && ob.value[pos - 1] == '}' && pos > 1 && ob.value[pos - 2] == "\t" && lstNewLine + 2 >= keyCnt){
        replace(ob, pos - 2, pos, '}');
    }
    setCopy();
}
function copy(){
    var ob = document.getElementById('code');
    var frm = document.getElementById('realCode');
    while(ob.childNodes.length > 0){
        ob.removeChild(ob.firstChild);
    }
    var get = frm.value + '\n';
    get = hljs.fixMarkup(hljs.highlight('cpp', get.replace(/ /g, ' sps;')).value, '\t', true);
    ob.innerHTML = get.replace(/ sps;/g, "<span> </span>").replace(/\t/g, '<span>\t</span>');
    ob.scrollTop = frm.scrollTop;
}
function syncScroll(){
    var ob = document.getElementById('code');
    var frm = document.getElementById('realCode');
    ob.scrollTop = frm.scrollTop;
}
function setCopy(){
    setTimeout('copy()', 100);
}

function word_count_fn(){
    document.getElementById('word_count').innerHTML=document.getElementById("realCode").value.length;
}
