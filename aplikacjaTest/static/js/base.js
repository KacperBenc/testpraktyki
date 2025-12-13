document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".alert-dismissible");
    const timeout = 4000; // czas w ms, np. 4000 = 4 sekundy

    alerts.forEach(function (alert) {
      setTimeout(function () {
        alert.classList.add("fade-out");
        // po animacji usuń element z DOM (dopasuj do czasu w CSS)
        setTimeout(function () {
          alert.remove();
        }, 500);
      }, timeout);
    });
});

const scrollTop = document.getElementById("goto-top-link");

window.onscroll = function(){
    scrollFunction();
};
function scrollFunction(){

    if( document.body.scrollTop > 20 || document.documentElement.scrollTop > 20){
        scrollTop.style.display = "block";
    } else {
        scrollTop.style.display = "none";
    }
}

scrollTop.addEventListener("click", function(){
    window.scrollTo({
        left: 0,
        top: 0,
        behavior: "smooth"
    })
})