function switchElement(e, suff){
    console.log(e);
    let details = document.getElementById(e.id + suff);
    
    if (details.classList.contains("hide")) {
        details.classList.remove('hide');
    
    } else {
        details.classList.add('hide');
    }
};

function switchPdnBtn(e) {
    let pdnCheBox = document.getElementById("pdn");
    let submitBtn = document.getElementsByClassName("feedbacksub")[0];
    if (pdnCheBox.checked) {
        submitBtn.classList.add('active');
    } else {
        submitBtn.classList.remove('active');
    }
}


async function sendFeedback(e, suff){
    let pdnCheBox = document.getElementById("pdn");
    if (!pdnCheBox.checked) {
        alert("Сначала необходимо дать согласие на обработку ПД")
        return 0
    }
    const url = "/feedback"
    let formElement = document.getElementById("feedbackData");
    let statusbar = document.getElementById("status");
    // let popupLaer = document.getElementById("popup");
    const data = new URLSearchParams();
    for (const pair of new FormData(formElement)) {
        
        data.append(pair[0], pair[1]);
    }

    let result = await fetch(url, {
        method: 'post',
        body: data,
    })
    .then((response) => {
        if (response.ok) {
            return response.json()
        }
        throw new Error('Something went wrong');
    })
    .catch((error) => {
        console.log("error")
    })
    if (result.status == "ok") {
        formElement.classList.add("hide");
        statusbar.innerText = result.msg;
        statusbar.classList.remove("hide");
        await new Promise(r => setTimeout(r, 2000));
        switchElement(e, suff);
        statusbar.classList.add("hide");
        formElement.classList.remove("hide");
    } else {
        statusbar.innerText = result.msg;
        statusbar.classList.remove("hide");
    }

}