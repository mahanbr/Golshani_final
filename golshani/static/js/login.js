

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

  let UIpasswordControl = document.querySelector('.password-control')
  UIpasswordControl.addEventListener('click', show_hide_password)

  function show_hide_password(e) {
    let input = document.getElementById("password");
    if (input.getAttribute("type") == "password") {
      input.setAttribute("type", "text");
    } else {
      input.setAttribute("type", "password");
    }
  }


