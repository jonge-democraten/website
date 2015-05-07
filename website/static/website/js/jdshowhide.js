function showHide(id) {
    var elm = document.getElementById(id);
    elm.style.display = (elm.style.display=='none'?'block':'none');
}

$(document).ready(function(){
    $("a[id|='jdtoggle']").attr("onclick", function(i) {
        return "showHide('A"+this.id.substring(9)+"'); return false;";
    });
});
