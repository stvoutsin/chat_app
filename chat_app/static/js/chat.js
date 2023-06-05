$(document).ready(function(){
    var current_user;
    $.get("/api/current_user",function(response){
        current_user = response;
    });
    var receiver = "";
    // create websocket
    var socket = new WebSocket("ws://localhost:8000/ws/chat");
    socket.onmessage = function(event) {

        var parent = $("#messages");
        var data = JSON.parse(event.data);
        if ("db_status" in data && "success" in data["db_status"] && data["db_status"]["success"] == false) {
            var content = "<div class='error'><span>There was an error processing this message:</span><br/> <i>" + data["db_status"]["message"]+ "</i></div>";
            parent.append(content);
            document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
            return;
        }
        var sender = data['sender'];
        if (sender == current_user)
            sender = "You";
        var message = data['message']
        var content = "<p><strong>"+sender+" </strong> <span> "+message+"</span> </br> <span class='sentdate'>" + data['created_at'] + "</span></p>";
        parent.append(content);
        document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
    };
    $("#chat-form").on("submit", function(e){
        e.preventDefault();
        var message = $("#message").val();
        var chat_id = $("#chat_id").val();
        var sender_id = $("#user_id").val();
        if (message){
            data = {
                "sender_id": sender_id,
                "chat_id": chat_id,
                "message": message,
            };

            socket.send(JSON.stringify(data));
            $("#message").val("");
            document.cookie = 'X-Authorization=; path=/;';
        }
    });
});
