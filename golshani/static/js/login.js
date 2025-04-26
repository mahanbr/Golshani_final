

  function validateForm() {
    const phone = document.getElementById('username').value
    const pass = document.getElementById('password').value
    if (phone == "" || pass == "") {
      alert("پر کردن تمام فیلدها اجباری است");
      user.style.borderColor = "red";
      pass.style.borderColor = "red";
      return false;
    }else if(phone.length != 11 || phone.substring(0, 2) != 09 ){
        alert("فرمت شماره تماس غلط می باشد!");
        return false;
    }
     else {
      return true;
    }
  }

  function verifySubmit(token) {
    if (validateForm() === true) {
        document.getElementById("login-form").submit();
    }
  }

  // let UIpasswordControl = document.querySelector('.password-control')
  // UIpasswordControl.addEventListener('click', show_hide_password)

  // function show_hide_password(e) {
  //   let input = document.getElementById("password");
  //   if (input.getAttribute("type") == "password") {
  //     input.setAttribute("type", "text");
  //   } else {
  //     input.setAttribute("type", "password");
  //   }
  // }



/*===================================
8. Show Hide Pass
=======================================*/
// ! need Work
const showHideBtn = document.querySelectorAll(".showHidePassword");

for (let i = 0; i < showHideBtn.length; ++i) {
    showHideBtn[i].addEventListener("click", function () {
        let inputEl = showHideBtn[i].closest(".input-wrapper").querySelector("input");

        if (inputEl) {
            if (inputEl.type === "password") {
                inputEl.type = "text";
                showHideBtn[i].classList.remove("bi-eye-fill");
                showHideBtn[i].classList.add("bi-eye-slash-fill");
            } else {
                inputEl.type = "password";
                showHideBtn[i].classList.remove("bi-eye-slash-fill");
                showHideBtn[i].classList.add("bi-eye-fill");
            }
        } else {
            console.error("Input element not found for the clicked button!");
        }
    });
}
