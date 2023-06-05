$(document).ready(function(){
    $("#login-form").on("submit", function(e){
        e.preventDefault();
        var username = $("#user_input").val();
        var password = $("#pass_input").val();
        if (username){
            data = {"username": username, "password": password};
               $.ajax({
                  type: "POST",
                  contentType: "application/json",
                  url: '/api/login',
                  data: JSON.stringify(data),
                  dataType: "json",
                  success: function (data) {
                       if ("status" in data){
                           if (!data["status"]){
                               $("#error").html(data["message"]).show();
                           } else {
                               $(".chat-body").removeClass("hide");
                               $(".chat-register").addClass("hide");
                               window.location.href = "/";
                           }
                       }
                  }
               });

        }
    });
});
