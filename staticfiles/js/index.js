var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});

jQuery('.slider-item').owlCarousel({
    loop:true,
    margin:10,
    rtl: true,
    nav: false,
    dots: true,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
        },
        600:{
            items:2,
        },
        1000:{
            items:2,
        }
    }
});

// jQuery('footer span.scrooltop').click(function (){
//     jQuery('body,html').animate((screenTop 0),2000)
// });

// let mybutton = document.getElementsByClassName(scrooltop);
// window.onscroll=function (){scrollFunction()};
// function scrollFunction(){
//     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20){
//         mybutton.style.display="block";
//     }
//     else {
//         mybutton.style.display="none";
//     }
// }
// function topFunction(){
//     document.body.scrollTop=0;
//     document.documentElement.scrollTop=0;
// }

jQuery('.cat-slider-item').owlCarousel({
    loop:true,
    margin:10,
    rtl: true,
    nav: false,
    dots: true,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
        },
        600:{
            items:3,
        },
        1000:{
            items:4,
        }
    }
});

jQuery('.product-gallery').owlCarousel({
    loop:true,
    margin:10,
    rtl: true,
    nav: false,
    dots: true,
    responsiveClass:true,
    responsive:{
        0:{
            items:2,
        },
        600:{
            items:3,
        },
        1000:{
            items:4,
        }
    }
});

jQuery('.timer').startTimer();
