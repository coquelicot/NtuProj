function getRequestObject(){
    var request = false;
    if(window.XMLHttpRequest){
        request = new XMLHttpRequest();
    }
    else{
        request = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return request;
}
function send(request, method, url, flg, msg){
    var time = new Date();
    request.open(method, url + '?time=' + time.getTime(), flg);
    if(method == 'POST'){
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    }
    request.send(msg);
}            
