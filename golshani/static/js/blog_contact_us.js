function verifySubmit(token) {
    let UIfullName = $('#id_full_name')
    let UIphone_number = $('#id_phone_number')   
    let UIsubject = $('#id_subject')
    let UIuserMessage = $('#id_user_message')
    let inputsVal = [UIfullName,  UIphone_number, UIsubject, UIuserMessage]
    for (let input in inputsVal){
      if (inputsVal[input].val() == ''){
        inputsVal[input].addClass('border-danger')
        return false
      }
    }

    if (UIphone_number.val().substring(0,2) !== '09' || UIphone_number.val().length != 11 ){
      // alert('فرمت شماره تماس صحیح نمی باشد')
      Swal.fire({
        title: "هشدار",
        text: "فرمت شماره تماس صحیح نمی باشد",
        icon: "error",
        showConfirmButton: false,
        timer: 2000,
      });
      return false;
    }
    document.getElementById("contact_us").submit();
  }