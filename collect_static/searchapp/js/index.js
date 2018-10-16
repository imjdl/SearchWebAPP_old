function submit_data(ths) {
    if(ths.search_msg.value == ""){
        return false;
    }
    if(user_name == "None"){
        alert("请先登录");
        return false;
    }else{
        return true;
    }
    return true;
}