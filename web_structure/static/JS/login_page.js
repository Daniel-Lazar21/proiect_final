// alert("APASA AICI MA")
let password = document.getElementById("this_password");
let button_pws = document.getElementById("slider");
let ball = document.getElementById("ball")

button_pws.onclick = function(){ 
    if(password.type == "password"){
        password.type = "text"; 
        ball.style = "transform: translateX(38px); \
                      transition:0.5s; \
                      background-color:red;"
                      
        button_pws.style = "border-color:red;\
                            transition:0.5s;"
    }
    else{
        password.type = "password";
        ball.style = "transform: translateX(0); \
                      transition:0.5s;";
        button_pws.style = "border-color:yellowgreen;\
                            transition:0.5s";
    }
}
//termina ce ai de facut la animatie si parola
// in online.py fa sa dai dispay cu html daca nu sunt toate campurile completate
// fa in asa fel incat box urile sa se mareasca la click pt ca altfel vei avea un bug =]]]
function preventBack() { 
    window.history.forward();  
} 
setTimeout("preventBack()", 0);  
window.onunload = function () { null }; 