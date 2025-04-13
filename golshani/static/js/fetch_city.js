const UIprovince = document.getElementById('id_province')
const UIcity = document.getElementById('id_city')
const UIcityData = document.getElementById('cityData')
UIprovince.addEventListener('click', receiveCities)

function receiveCities(e) {
    if (e.target.value == '') {
        return false
    }
    let proNum = e.target.value
    $.ajax({
        type: "GET",
        timeout: 5000,
        mode: 'same-origin',
        url: UIcityData.getAttribute('data-url'),
        data: {
            province_num: proNum,
        },
        success: function (data) {
            if (data['status'] === 200) {
                UIcity.innerHTML = ''
                data['city'].forEach(city => {
                    let option = document.createElement('option')
                    option.value = city['id']
                    option.textContent = city['name']
                    UIcity.appendChild(option)
                });
            }
        },
        error: function (problem) {
            // alert('خطایی پیش آمده است لطفا مجدد تلاش نمایید.', )
            Swal.fire({
                title: "هشدار",
                text: "خطایی پیش آمده است لطفا مجدد تلاش نمایید.",
                icon: "error",
                showConfirmButton: false,
                timer: 2000,

            });
        },
    });
}