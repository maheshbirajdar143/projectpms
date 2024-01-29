function openPopupz(url) {
    var popupContainer = document.getElementById('popup-container1');
    var popupIframe = document.getElementById('popup-iframe');

    popupIframe.src = url;
    popupContainer.style.display = 'block';

    document.body.addEventListener('click', closePopupzOutside);
    }

    function closePopupz() {
        var popupContainer = document.getElementById('popup-container1');
        popupContainer.style.display = 'none';
    }