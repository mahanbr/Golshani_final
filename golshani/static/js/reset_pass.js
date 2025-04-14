function validateForm() {
    const phone = document.getElementById('id_phone_number').value
    if (phone == "") {
        Swal.fire({
            title: "هشدار",
            text: "پر کردن تمام فیلدها اجباری است",
            icon: "error",
            showConfirmButton: false,
            timer: 2000,

        });
        phone.style.borderColor = "red";
        return false;
    } else if (phone.length != 11 || phone.substring(0, 2) != 09) {

        Swal.fire({
            title: "هشدار",
            text: "فرمت شماره تماس صحیح نمی باشد",
            icon: "error",
            showConfirmButton: false,
            timer: 2000,

        });
        return false;
    } else {
        return true;
    }
}

function verifySubmit(token) {
    if (validateForm() === true) {
        const pass1 = document.getElementById('id_password1').value
        const pass2 = document.getElementById('id_password2').value
        const user_code = document.getElementById('user_code').value
        if (user_code == '' || pass1 == "" || pass2 == "") {
            Swal.fire({
                title: "هشدار",
                text: "پر کردن تمام فیلدها اجباری است",
                icon: "error",
                showConfirmButton: false,
                timer: 2000,

            });
            return false
        } else if (pass1 != pass2) {
            Swal.fire({
                title: "هشدار",
                text: "رمز و تکرار رمز باید مانند هم باشند",
                icon: "error",
                showConfirmButton: false,
                timer: 2000,

            });
            return false;
        }
        document.getElementById("login-form").submit();
    }
}

const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;


function onSubmit(token) {

    if (Number.isInteger(parseInt(document.getElementById('countdown').value))) {
        return false
    }
    if (validateForm() === true) {
        document.querySelector('#countdown').style.cursor = 'wait'


        $.ajax({
            type: "POST",
            timeout: 5000,
            headers: {
                'X-CSRFToken': csrf
            },
            mode: 'same-origin',
            url: window.location.href,
            data: {
                phone_number: document.getElementById('id_phone_number').value,
                // recaptcha: token
            },
            success: function (data) {
                document.querySelector('#countdown').style.cursor = 'auto'

                if (data['status'] === 200) {
                    Swal.fire({
                        title: "ارسال شد",
                        icon: "success",
                        showConfirmButton: false,
                        timer: 2000,

                    });
                    document.querySelector('#id_phone_number').style.display = 'none'
                    document.querySelector('.otp-confirm').style.display = 'block'
                    reverse_counter('countdown', 200)

                } else if (data['status'] === 500) {
                    Swal.fire({
                        title: "هشدار",
                        text: "خطایی پیش آمده است لطفا مجدد تلاش نمایید.",
                        icon: "question",
                        showConfirmButton: false,
                        timer: 2000,

                    });
                } else if (data['status'] === 409) {
                    Swal.fire({
                        title: "هشدار",
                        text: "این شماره تماس از قبل موجود است",
                        icon: "error",
                        showConfirmButton: false,
                        timer: 2000,

                    });
                }
            },
            error: function (problem) {
                document.querySelector('#countdown').style.cursor = 'auto'
                Swal.fire({
                    title: "هشدار",
                    text: "خطایی پیش آمده است لطفا مجدد تلاش نمایید.",
                    icon: "question",
                    showConfirmButton: false,
                    timer: 2000,

                });
            },
        });

    }
}

document.getElementById('countdown').addEventListener('click', onSubmit);


function reverse_counter(element, time) {
    var timeleft = time;
    const box = document.getElementById(element)
    box.className += ' disabled'

    var downloadTimer = setInterval(function () {
        if (timeleft <= 0) {
            clearInterval(downloadTimer);
            box.value = 'دریافت کد تایید';
            box.classList.remove('disabled')
            document.querySelector('#countdown').style.cursor = 'pointer'

        } else {
            box.value = timeleft;
        }
        timeleft -= 1;
    }, 1000);

}
const UIform = document.querySelector('form')