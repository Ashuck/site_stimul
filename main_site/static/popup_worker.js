function showFeedback(){
    let popupLaer = document.getElementById("popup");
    popupLaer.classList.remove("hide");
};
function hideFeedback(){
    let popupLaer = document.getElementById("popup");
    popupLaer.classList.add("hide");
};
async function sendFeedback(){
    const url = "/feedback"
    let formElement = document.getElementById("feedbackData");
    let statusbar = document.getElementById("status");
    let popupLaer = document.getElementById("popup");
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
        statusbar.innerText = "Заявка принята";
        statusbar.classList.remove("hide");
        await new Promise(r => setTimeout(r, 2000));
        popupLaer.classList.add("hide");
        statusbar.classList.add("hide");
        formElement.classList.remove("hide");
    } else {
        statusbar.innerText = result.msg;
        statusbar.classList.remove("hide");
    }

}