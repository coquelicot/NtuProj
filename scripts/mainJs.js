var currentRoomName=null;
var roomNo=0;
var room_times=0;

function getRequestObject(){    //OK!
    var request = false;
    if(window.XMLHttpRequest){
        request = new XMLHttpRequest();
    }
    else{
        request = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return request;
}
function send(request, method, url, flg, msg){  //OK!
    var time = new Date();
    request.open(method, url + '?time=' + time.getTime(), flg);
    if(method == 'POST'){
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    }
    request.send(msg);
}            

/*  coder   */
function sendCode(){    //OK!
    var req = getRequestObject();
    if(!req) {}
    else{
        req.onreadystatechange = function(){
            if(req.readyState == 4){
                if(req.status == 200){
                    var text = transfer(req.responseText);    //成功編譯或超時或編譯錯誤或或runtime error;若成功回傳結果
                    var flag= text.indexOf("<br/>");
                    document.getElementById('output').style.borderWidth='10px';
                    document.getElementById('output').style.borderColor='#213216';
                    document.getElementById('output').style.borderStyle='outset';
                    document.getElementById('Output_title').style.fontSize='12px';
                    document.getElementById('Output_title').style.marginTop='25px';
                    document.getElementById('Output_title').style.padding='1px';
                    document.getElementById('Output_title').style.borderWidth='2px';
                    document.getElementById('Output_title').style.borderStyle='solid';
                    document.getElementById('errorSyntax').innerHTML=text.slice(0,flag);
                    document.getElementById('errorContent').innerHTML = text.slice(flag+5);
                }
            }
        }
        var code=document.getElementById('realCode');
        var input=document.getElementById('input');
        send(req, 'POST', '/coder/sendCode', true, 'code=' + encodeURIComponent(code.value) +'&input=' + encodeURIComponent(input.value));
    }
    return false;
}

/*  other   */
function getVisit(){
    var req = getRequestObject();
    if(!req) {}
    else{
        req.onreadystatechange = function(){
            if(req.readyState == 4){
                if(req.status == 200){
                    var text = transfer(req.responseText);    //當天累計人數 總人數
                    var flag = text.indexOf(" ");
                    document.getElementById("today_num").innerHTML=text.slice(0,flag);
                    document.getElementById("accumulate_num").innerHTML=text.slice(flag+1);
                }
            }
        }
        send(req, 'POST', '/other/getVisit', true, null);
    }
}

/*  chat    */  
function sendMessage(room_name){
    var req = getRequestObject();
    if(!req) {}
    else{
        req.onreadystatechange = function(){
            if(req.readyState == 4){
                if(req.status == 200){
                    var text = req.responseText;    //唯一不必回傳消息 sendMessage後接續執行getmessage
                    document.getElementById('message_send_text').value="";
                }
            }
        }
        var text=document.getElementById('message_send_text').value;
        send(req, 'POST', '/chat/sendMessage', true, 'text=' + encodeURIComponent(text)+ '&room=' + encodeURIComponent(room_name));

    }
}

function getMessage(room_name){
    var req = getRequestObject();
    if(!req) {}
    else{
        req.onreadystatechange = function(){
            if(req.readyState == 4){
                if(req.status == 200){
                    var text = req.responseText;    //上限50筆資料 顯示在顯示在chatroom
                    //transfer(text);
                    document.getElementById('chatroom').innerHTML=text;
                }
            }
        }
        send(req, 'POST', '/chat/getMessage', true, 'room=' + encodeURIComponent(room_name));
    }
}

function getUserList(room_name,e){ //先暫時停擺
    var req = getRequestObject();
    if(!req) {}
    else{
        req.onreadystatechange = function(){
            if(req.readyState == 4){
                if(req.status == 200){
                    var text = transfer(req.responseText);    //顯示在show上 半透明置中
                    var ob = document.getElementById('show_userName');
                    if (text=='Room not exist.')    text='';
                    if (text==''){
                        ob.style.borderWidth='0px';
                        ob.style.borderStyle='none';
                    }
                    else{
                        ob.style.borderWidth='2px';
                        ob.style.borderStyle='solid';
                    }
                    var x=e.clientX;
                    var y=e.clientY;
                    ob.innerHTML=text;
                    ob.style.position='fixed';
                    ob.style.top=y+'px';
                    ob.style.left=x+'px';
                }
            }
        }
        send(req, 'POST', '/chat/getUserList', true, 'room=' + encodeURIComponent(room_name));
    }

}

function createFunc(num){
    return function(){
        var id = 'room_name' + num;
        joinRoom(document.getElementById(id).innerHTML);
    };
}

function display(num){
    return function(){
        var id='room_name'+num;
        getUserList(document.getElementById(id).innerHTML,event);
    }
}

function notdisplay(){
    document.getElementById('show_userName').style.borderStyle='none';
    document.getElementById('show_userName').innerHTML="";
}

function getNumberOfUser(){
    var req = getRequestObject();
    if(!req) {}
    else{
        req.onreadystatechange = function(){
            if(req.readyState == 4){
                if(req.status == 200){
                    var text = transfer(req.responseText);    /*顯示在room的table後面*/
                    var temp_split = text.split("<br/>");
                    var roomList = document.getElementById('room_list');
                    var i;
                    var j=0;
                    while(roomList.childNodes.length > 0){
                        roomList.removeChild(roomList.firstChild);
                    }
                    for (i=0;i<temp_split.length;i=i+1){
                        var pos = temp_split[i].indexOf(" ");
                        var tempfile = new Array(temp_split[i].slice(0, pos), temp_split[i].slice(pos + 1));
                        var newdivRoom = document.createElement('div');
                        var newdivName = document.createElement('div');
                        var newspanState = document.createElement('span');
                        var newspanNum = document.createElement('span');
                        newdivRoom.id = 'room' + i;
                        newdivRoom.className='room';
                        newdivRoom.onclick = createFunc(i);
                        newdivRoom.onmouseover = display(i);
                        newdivRoom.onmouseout = notdisplay;
                        newdivName.id = 'room_name' + i;
                        newdivName.className='room_name';
                        newdivName.appendChild(document.createTextNode(tempfile[1]));
                        //document.getElementById('room_name' + i).innerHTML = tempfile[1];
                        newspanState.className = 'person';
                        newspanState.appendChild(document.createTextNode('在線人數: '));
                        newspanNum.id = 'room_num' + i;
                        newspanNum.appendChild(document.createTextNode(tempfile[0]));
                        //document.getElementById('room_num' + i).innerHTML = tempfile[0];
                        newspanState.appendChild(newspanNum);
                        newdivRoom.appendChild(newdivName);
                        newdivRoom.appendChild(newspanState);
                        roomList.appendChild(newdivRoom);
                    }

                }
            }
        }
        send(req, 'POST', '/chat/getNumberOfUser', true, null);
    }
}

function createRoom(){
    var req = getRequestObject();
    if(!req) {}
    else{
        req.onreadystatechange = function(){
            if(req.readyState == 4){
                if(req.status == 200){
                    var text = req.responseText;    //回傳成功或是失敗
                    transfer(text);
                    if (text == "AC"){ 
                        alert("Accepted!");
                        joinRoom(room.value);
                    }
                    // else alert(text);
                }
            }
        }
        var room=document.getElementById('create_room_text');
        send(req, 'POST', '/chat/createRoom', true, 'room=' + encodeURIComponent(room.value));
    }
}

function joinRoom(room_name){
    /*if(currentRoomName){
      alert("You are leaving from: " + currentRoomName);
      }*/
    var req = getRequestObject();
    if(!req){}
    else{
        req.onreadystatechange = function(){
            if(req.readyState == 4){
                if(req.status == 200){
                    var text = req.responseText;    //得到前50筆訊息
                    if (text == 'AC'){
                        currentRoomName=room_name;
                        document.getElementById('currentRoomName').innerHTML=currentRoomName;
                        getMessage(currentRoomName);
                        getNumberOfUser();
                    }
                    else alert(text);
                }
            }
        }
        send(req, 'POST', '/chat/joinRoom', true, 'room=' + encodeURIComponent(room_name));
    }
}

function logout(){
    location.href="/other/logout";
}

/*
   function getRoomList(){
   var req = getRequestObject();
   if(!req) {}
   else{
   req.onreadystatechange = function(){
   if(req.readyState == 4){
   if(req.status == 200){
   var text = transfer(req.responseText);    //回傳仍存在房間名稱
   alert(text);
   var eachroom = text.split("<br/>");
   var i,j=0;
   var room_check=0;
   var array = new Array();
   var roomList = document.getElementById('room_list');
   for (i=0;i<room_times;i=i+1){
   room_check=0;
   for (j=0;j<eachroom.length;j++){
   if (roomList.childNodes[i].firstchild.innerHTML == eachroom[j]){
   room_check=1;
   }
   }
   if (room_check==0){
   array.push(roomList.childNodes[i]);
   }
   }
   for(i = 0; i < array.length; i++){
   roomList.removeChild(array[i]);
   }
   }
   }
   }
   send(req, 'POST', '/chat/getNumberOfUser', true, null);
   }
   }
   */

function send_and_read(){
    sendMessage(currentRoomName);
    getMessage(currentRoomName);
}

function transfer(text){
    return text.replace(/\n/g,"<br/>");
}

function clearCode(num){
    if (num==0){
        if (document.getElementById('realCode').value!='<Please write your code here!>'){}
        else document.getElementById('realCode').value='';
    }
    else if (num==1)    document.getElementById('realCode').value='<Please write your code here!>';
}

function clearInput(num){
    if (num==0){
        if (document.getElementById('input').value!='<Please write your input here!>'){}
        else document.getElementById('input').value='';
    }
    else if (num==1)    document.getElementById('input').value='<Please write your input here!>';
    return false;
}
function recover(){
    if (document.getElementById('realCode').value==''){
        document.getElementById('realCode').value='<Please write your code here!>';
        copy();
    }
    if (document.getElementById('input').value==''){
        document.getElementById('input').value='<Please write your input here!>';
    }
}
