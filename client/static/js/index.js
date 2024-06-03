$(document).ready(function(){
    
    $("#toggle-sidenav").on("click",function(){
        $(".sidenav").toggleClass("sidenav-collapse")
        $(".main-content").toggleClass("main-content-exp")
        $(".sidenav-header").toggleClass("sidenav-header-resize")
        $(".user-profile-pic").toggleClass("user-profile-pic-resize")
        $(".sidenav-item").toggleClass("sidenav-item-resize")
        $(".sidenav-item-img").toggleClass("sidenav-item-img-expand")
        $(".sidenav-item-span").toggleClass("sidenav-item-span-collapse")
    })
    const clip = document.querySelectorAll(".clip")
  
    for(let i = 0;i < clip.length;i++) {
        clip[i].addEventListener("mouseover", function (e) {
            clip[i].play();
        })
        clip[i].addEventListener("mouseout", function (e) {
            clip[i].pause();
            clip[i].load();
        })
    }
    
})