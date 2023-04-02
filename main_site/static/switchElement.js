function switchElement(e, suff){
    let details = document.getElementById(e.id + suff);
    
    if (details.classList.contains("hide")) {
        details.classList.remove('hide');
    
    } else {
        details.classList.add('hide');
    }
};