
$(document).ready(function() {
    
    //Run all the functions
    registerUser()
    loginUser()
    copyPrivate()
    copyBusiness()
    editPersonalQuestion()
    editBusinessQuestion()

    function registerUser(){
        $('#register').click(function(event) {
            event. preventDefault()
            var registerUrl = $(this).attr("data-url") ;
            var profileUrl = $(this).attr("profile-url") ;
            var username = $("#register_username").val();
            var email = $("#register_email").val();
            var password = $("#register_password").val();
            
            if ((username.length == 0)||(email.length == 0)||(password.length == 0)){
                $('#register_failure').text("** Fill in all the fields");
                return
            }

            $.ajax({
                'method': 'GET',  
                'url': registerUrl,
                'data': {"username": username,
                        "email": email,
                        "password": password,
                        "action": "register",
                        },  
                success: function(dataReturned) {
                    var registered = dataReturned['registered']
                    var username_status = dataReturned['username_status']
                    var email_status = dataReturned['email_status']
                    if (registered == 'True'){
                        $('#register_failure').text("");
                        $('#register_emailHelp').text("");
                        $('#register_usernameHelp').text("");
                        $('#register_success').text("Account Created Succesfully!");
                        setTimeout(function(){
                            window.location.href = profileUrl;

                        }, 1000);
                        
                        }
                    
                    else if (username_status == 'False'){
                        $('#register_usernameHelp').text("username is taken, try another username");
                        $('#register_emailHelp').text("");
                        $('#register_failure').text("");
                        $('#register_success').text("");
                        }
                    
                    else if (email_status == 'False'){
                        $('#register_emailHelp').text("email address already exists!");
                        $('#register_usernameHelp').text("");
                        $('#register_failure').text("");
                        $('#register_success').text("");

                        }

                    else{
                        $('#register_failure').text("Failed! Contact Admin");
                        $('#register_success').text("");
                        $('#register_usernameHelp').text("");
                        $('#register_emailHelp').text("");
                    }
                  
                }
            });
    
            
        });
    }
    


    function loginUser(){
        $('#login').click(function(event) {
            event. preventDefault()
            var loginUrl = $(this).attr("data-url") ;
            var profileUrl = $(this).attr("profile-url") ;
            var username = $("#login_username").val();
            var password = $("#login_password").val();
            
            if ((username.length == 0)||(password.length == 0)){
                $('#login_failure').text("** Fill in all the fields");
                return
            }

            $.ajax({
                'method': 'GET',  
                'url': loginUrl,
                'data': {"username": username,
                        "password": password,
                        "action": "login",
                        },  
                success: function(dataReturned) {
                    var loggedin = dataReturned['loggedin']
                    var username_status = dataReturned['username_status']
                    if (loggedin == 'True'){
                        $('#login_failure').text("");
                        $('#login_usernameHelp').text("");
                        $('#login_success').text("Login Succesfull!");
                        setTimeout(function(){
                            window.location.href = profileUrl;

                        }, 1000);
                        }
                    
                    else if (username_status == 'False'){
                        $('#login_usernameHelp').text("user does not exist, please sign up first");
                        $('#login_failure').text("");
                        $('#login_success').text("");
                        }

                    else{
                        $('#login_failure').text("Incorrect Credentials!");
                        $('#login_success').text("");
                        $('#login_usernameHelp').text("");
                    }
                  
                }
            });
    
            
        });
    }
    
    
    function copyPrivate(){
        $('#linkCopyPrivate').click(function(event) {
            event. preventDefault()
            var link = $("#linkPrivate").val();
            var message = $("#personal-question").text();
            var truncatedMessage = message.split(' ').slice(1).join(' ')
            var finalMessage =truncatedMessage+ "\n" +"Write me an anonymous message"+"\n";
            var finalString = finalMessage.concat(link);

            navigator.permissions.query({ name: "clipboard-write" }).then((result) => {
                if (result.state == "granted" || result.state == "prompt") {

                    navigator.clipboard.writeText(finalString); //copies to the clipboard
                    // alert("copied!! \n\n"+finalString);
                    const tooltip = document.querySelector("#copyPersonal-tooltip");
                    tooltip.style.display = "block";
                    setTimeout(function(){
                        tooltip.style.display = "none";

                    }, 4000);
                  
                }
                else{
                    var range = document.createRange();
                    textNode = document.createElement("p");
                    textNode.appendChild(document.createTextNode(finalString));
                    range.selectNode(document.getElementsByTagName("div").item(0));
                    range.insertNode(textNode);
                    window.getSelection().removeAllRanges(); // clear current selection
                    window.getSelection().addRange(range); // to select text
                    document.execCommand("copy");
                    window.getSelection().removeAllRanges();// to deselect
                    
                    const tooltip = document.querySelector("#copyPersonal-tooltip");
                    tooltip.style.display = "block";
                    setTimeout(function(){
                        tooltip.style.display = "none";

                    }, 4000);
                
                }
              });


            
          
           


            


            
            
        });
    }
    

    function copyBusiness(){
        $('#linkCopyBusiness').click(function(event) {
            event. preventDefault()
            var link = $("#linkBusiness").val();
            var message = $("#business-question").text();
            var truncatedMessage = message.substr(message.indexOf(" ") + 1);
            var finalMessage =truncatedMessage+ "\n"+"Write us anonymous feedback"+"\n";
            var finalString = finalMessage.concat(link);


            navigator.permissions.query({ name: "clipboard-write" }).then((result) => {
                if (result.state == "granted" || result.state == "prompt") {

                    navigator.clipboard.writeText(finalString); //copies to the clipboard
                    // alert("copied!! \n\n"+finalString);
                    const tooltip = document.querySelector("#copyBusiness-tooltip");
                    tooltip.style.display = "block";
                    setTimeout(function(){
                        tooltip.style.display = "none";

                    }, 4000);
                  
                }
                else{
                    var range = document.createRange();
                    textNode = document.createElement("p");
                    textNode.appendChild(document.createTextNode(finalString));
                    range.selectNode(document.getElementsByTagName("div").item(0));
                    range.insertNode(textNode);
                    window.getSelection().removeAllRanges(); // clear current selection
                    window.getSelection().addRange(range); // to select text
                    document.execCommand("copy");
                    window.getSelection().removeAllRanges();// to deselect
                    
                    const tooltip = document.querySelector("#copyBusiness-tooltip");
                    tooltip.style.display = "block";
                    setTimeout(function(){
                        tooltip.style.display = "none";

                    }, 4000);
                
                }
              });


            
          
           


            


            
            
        });
    }
  

    function editPersonalQuestion(){
        $('#savePersQuestion').click(function(event) {
            event. preventDefault()
            var persQuestion = $("#personalQuestionModalText").val();
            var saveUrl = $(this).attr("data-url") ;

            
            if (persQuestion.length == 0){
                alert("question cannot be empty");
                return
            }

            $.ajax({
                'method': 'GET',  
                'url': saveUrl,
                'data': {"persQuestion": persQuestion,
                        "type": "personal",
                        },  
                success: function(dataReturned) {
                    var saved = dataReturned['saved']
                    if (saved == 'True'){
                        $('#PersoanlQUestionModal').modal('toggle');
                        $('#personal-question').text("Question: "+persQuestion+"?");
                        
                        }
                  
                }
            });
    
            
        });
    }

   

    function editBusinessQuestion(){
        $('#saveBusQuestion').click(function(event) {
            event. preventDefault()
            var busQuestion = $("#businessQuestionModalText").val();
            var saveUrl = $(this).attr("data-url") ;

            
            if (busQuestion.length == 0){
                alert("question cannot be empty");
                return
            }

            $.ajax({
                'method': 'GET',  
                'url': saveUrl,
                'data': {"busQuestion": busQuestion,
                        "type": "business",
                        },  
                success: function(dataReturned) {
                    var saved = dataReturned['saved']
                    if (saved == 'True'){
                        $('#BusinessQUestionModal').modal('toggle');
                        $('#business-question').text("Question: "+busQuestion+"?");
                        
                        }
                  
                }
            });
    
            
        });
    }

});
