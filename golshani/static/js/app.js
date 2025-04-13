// 01.Loader js
// 3.SideBard Show Hide js
// 4.Tap To Top Js 
// 5.Input Number Length Validation Js 
// 6.Owl Carousel js 
// 7. Persian Date js 
// 8. Show Hide Pass
// 9. Add To wishlist
// 10. Format numbers
// 11. Footer Accoridan

"use strict";
// Body Selection //
const body = document.querySelector("body");





/*==================
  01. Loader js
======================*/
const loaderSpan = document.querySelector(".loader").children
const animate = function () {
    document.querySelector(".loader").classList.toggle('animate');
}
const timeOutAnimation = setInterval(animate, 1000);
document.onreadystatechange = function () {
    if (document.readyState !== "complete") {

        timeOutAnimation;
        body.classList.add("loader-overflow")
    } else {
        setTimeout(function () {
            document.querySelector(".loader-wrapper").classList.add("hidden")
            clearInterval(timeOutAnimation)
            body.classList.remove("loader-overflow")
        }, 1000)

    }
};




/*=====================
  3. SideBard Show Hide js
 ==========================*/
const overlay = document.querySelector(".overlay-general");

/// Common Template ///
const sidebarToggle = function (showBtn, sidebar, overlay, backBtn) {
    showBtn?.addEventListener("click", function () {
        sidebar.classList.add("show-menu");
        overlay.classList.add("show");
        const removeFun = function () {
            sidebar.classList.remove("show-menu");
            overlay.classList.remove("show");
        }
        backBtn.addEventListener("click", removeFun)
        overlay.addEventListener("click", removeFun)
    });
}

/// User Dashboard SideBar ///
const settingMenuBtn = document.querySelector(".setting-menu");
const sideBarEl = document.querySelector(".side-bar");
const backBtnEl = document.querySelector(".back-side");
sidebarToggle(settingMenuBtn, sideBarEl, overlay, backBtnEl);
/// Shop Page SideBar ///
const filterOptionBtn = document.querySelector(".filter-btn");
const shopSideBar = document.querySelector(".sidebar-controll");
const backShopBtn = document.querySelector(".back-box");
sidebarToggle(filterOptionBtn, shopSideBar, overlay, backShopBtn);

/*===================== 
4. Tap To Top Js 
==========================*/
const tapTopBtn = document.querySelector(".tap-to-top-button")
const tapTopTopBox = document.querySelector(".tap-to-top-box")
tapTopBtn?.addEventListener("click", function () {
    window.scroll({
        top: 0,
        behavior: 'smooth'
    });
})
if (tapTopTopBox) {
    window.onscroll = function () {
        if (pageYOffset >= 1000) {
            tapTopTopBox.classList.remove("hide")
        } else {
            tapTopTopBox.classList.add("hide")
        }
    }
}


/*===================================
5. Input Number Length Validation Js 
=======================================*/
function constrainUserInput() {
    const inputNumber = document.querySelectorAll("input[type='number']");
    inputNumber?.forEach(function (el) {
        el.addEventListener("keypress", function (e) {
            const maxLength = +el?.getAttribute("maxlength")
            if (maxLength) {
                const value = el.value
                if (value.length >= maxLength) {
                    el.value = value.substring(0, (el.maxLength - 1))
                }
            }
        })
    })
}
constrainUserInput();

/*===================================
6. Owl Carousel js 
=======================================*/

$('.similar-item').owlCarousel({
    rtl: true,
    loop: true,
    nav: false,
    dots: false,
    margin: 30,
    responsive: {
        0: {
            items: 1,
        },
        600: {
            items: 2,

        },
        900: {
            items: 3,

        },
        1200: {
            items: 4
        }
    }
})

 


 
 

    const Toast = swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
      }
    })
    

    $('.product-btn').click(function(){
        const url = $(this).data('url')
        const csrf = $(this).data('csrf')
        var icon = $(this).find('svg');


      $.ajax({
        url: url,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrf
        },
        success: function(data) {
            let status = data['status'] 
            if (status == 200){
                if (icon.hasClass('liked') == false){
                    Toast.fire({
                        icon: 'success',
                        title: 'به علاقه مندی ها افزوده شد.'
                      })
                }
                icon.addClass('liked')
            }
            else if (status == 10){
                if (icon.hasClass('liked') == true){
                    Toast.fire({
                        icon: 'error',
                        title: 'از علاقه مندی ها حذف شد.'
                      })
                }
                icon.removeClass('liked');
            }
            else if(status == 403) {
                Toast.fire({
                    icon: 'error',
                    title: 'برای افزودن به علاقه مندی باید وارد حساب خود شوید.'
                  })
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            console.error('Failed to add product to wishlist.');
        }
      });
    });
 


/*===================================
10. Format numbers 
=======================================*/
const rangeInputs = document.querySelectorAll('.min-max');
rangeInputs.forEach(function(input) {
  input.addEventListener('input', function() {
    const inputValue = Number(this.value.replace(/,/g, ''));
    const formattedValue = new Intl.NumberFormat().format(inputValue);
    this.value = formattedValue;
  });
});


/*===================================
11. Footer Accoridan 
=======================================*/
const footerButton = document.querySelectorAll(".nav-footer h4");
const showNav = document.querySelector(".nav");
for (var i = 0; i < footerButton.length; ++i) {
    footerButton[i].addEventListener('click', function () {
        this.parentNode.classList.toggle('open');
    })
}



// Slider 
$(document).ready(function () {
    feather.replace()



    var owl = $('.owl-carousel.hero');
    $(' .owl-carousel.hero').owlCarousel({
      items: 1,
      loop: true,
      dots: false,
      rtl: true,
      margin: 0,
      autoplay: true,
      smartSpeed: 1000,
      nav: true,
      navText: ["<i class='fa fa-chevron-right'></i>", "<i class='fa fa-chevron-left'></i>"],
  
    });
    $('.owl-carousel.hero .owl-prev').attr('aria-label', 'previous page');
    $('.owl-carousel.hero .owl-next').attr('aria-label', 'next page');
  
    owl.on('changed.owl.carousel', function (event) {
      var item = event.item.index - 2; // Position of the current item
      $('h2').removeClass('animate__animated animate__fadeInUp animate__delay-2s');
      $('a').removeClass('animate__animated animate__fadeInUp animate__delay-2s');
      $('p').removeClass('animate__animated animate__fadeInUp animate__delay-2s');
      $('.owl-item').not('.cloned').eq(item).find('h2').addClass('animate__animated animate__fadeInUp');
      $('.owl-item').not('.cloned').eq(item).find('a').addClass('animate__animated animate__fadeInUp');
      $('.owl-item').not('.cloned').eq(item).find('p').addClass('animate__animated animate__fadeInUp');
    });



    /*===================================
    7. Persian Date js 
    =======================================*/

 
    let UIpdAte = document.querySelectorAll('.pdate')
    UIpdAte = Array.from(UIpdAte)
    UIpdAte.forEach((pdate) => {
        pdate.textContent = new Date(pdate.textContent).toLocaleDateString('fa-IR')
    });
 

    
  });
  
  // Sections background image from data background
  var pageSection = $(".bg-img, section");
  pageSection.each(function (indx) {
    if ($(this).attr("data-background")) {
      $(this).css("background-image", "url(" + $(this).data("background") + ")");
    }
  });
  
  
 
 

 