let user_icon = document.getElementById("user_icon");
let log_out_button = document.getElementById("log_out_button");
let info_box = document.getElementById("info_box")
let user_icon_active = false

user_icon.onclick = function(){
    if (user_icon_active)
    {
        log_out_button.style = "opacity:0;\
                                transform:translateX(70px);\
                                transition: 0.5s;"
        user_icon_active = false
    }
    else
    {
        log_out_button.style = "opacity:1;\
                                transform:translateX(0);\
                                transition: 0.5s;"
        user_icon_active = true
    }
    
}

log_out_button.onclick = function(){
    log_out_button.style = "transform:scale(0.9)"
}

function check_info_box_text(){
    if(info_box.innerHTML.trim() === "<h4>Datele au fost introduse cu succes!</h4>")
    {
        info_box.style = "color:#00ff00"
    }
    else
    {
        info_box.style = "color:#ff0000"  
    }

}

check_info_box_text()