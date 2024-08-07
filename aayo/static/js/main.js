document.addEventListener('DOMContentLoaded', function() {
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    const roomLink = document.getElementById('roomLink');
    const cafeLogos = document.querySelectorAll('.cafe-logo');
    const cafeInput = document.getElementById('cafe');

    // room.html 에서 카페 리스트 선택 시 AJAX
    cafeLogos.forEach(logo => {
        logo.addEventListener('click', function() {
            // 모든 로고에서 'selected' 클래스를 제거하여 선택되지 않은 상태로 만들기
            cafeLogos.forEach(logo => logo.classList.remove('selected'));
            // 클릭한 로고에 'selected' 클래스를 추가하여 선택된 상태로 만들기
            this.classList.add('selected');
            // 클릭한 로고의 'data-cafe' 속성 값을 가져와 'cafeInput' 요소의 값으로 설정
            cafeInput.value = this.getAttribute('data-cafe');
        });
    });

    // 링크 공유하기 버튼 눌렀을 때 클립보드에 링크 복사 AJAX
    if (copyLinkBtn && roomLink) {
        copyLinkBtn.addEventListener('click', function() {
            const linkToCopy = roomLink.href;
            navigator.clipboard.writeText(linkToCopy).then(() => {
                alert("방 링크가 클립보드에 복사되었습니다!");
            }).catch(err => {
                console.error('클립보드 복사 실패:', err);
                fallbackCopyTextToClipboard(linkToCopy);
            });
        });
    }

    const modal = document.getElementById('menuDetailModal');
    if (modal) {
        const menuItems = document.querySelectorAll('.menu-item');
        const modalTitle = document.getElementById('menuDetailModalLabel');
        const modalImage = document.getElementById('modalMenuImage');
        const saveMenuItem = document.getElementById('saveMenuItem');
        const closeBtn = modal.querySelector('.close');
        const confirmButton = document.getElementById('confirmButton');
        const selectedOptions = new Set();

        menuItems.forEach(item => {
            item.addEventListener('click', function() {
                const menuId = this.getAttribute('data-menu-id');
                const menuName = this.querySelector('.menu-name').textContent;
                const menuImageSrc = this.querySelector('.menu-image')?.src;

                modalTitle.textContent = menuName;
                if (menuImageSrc) {
                    modalImage.src = menuImageSrc;
                    modalImage.style.display = 'block';
                } else {
                    modalImage.style.display = 'none';
                }
                modal.style.display = 'block';
                saveMenuItem.setAttribute('data-menu-id', menuId);
            });
        });

        closeBtn.onclick = function() {
            modal.style.display = 'none';
        }

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }

        saveMenuItem.addEventListener('click', function() {
            const menuId = this.getAttribute('data-menu-id');
            const temperature = document.querySelector('#hotButton.active, #iceButton.active') ? document.querySelector('#hotButton.active, #iceButton.active').textContent.trim() : '';
            const size = document.querySelector('#regularButton.active, #extraButton.active') ? document.querySelector('#regularButton.active, #extraButton.active').textContent.trim() : '';
            const ice = document.querySelector('#bigIceButton.active, #regularIceButton.active, #lessIceButton.active') ? document.querySelector('#bigIceButton.active, #regularIceButton.active, #lessIceButton.active').textContent.trim() : '';
            const instructions = document.getElementById('additionalInstructions').value;


            selectedOptions.add({
                id: menuId,
                options: { temperature, size, ice, instructions }
            });

            updateButtonState();
            modal.style.display = 'none';
        });

        // 메뉴 선택하기 버튼 눌렀을 때 작동되는 ajax
        const menuForm = document.getElementById('menuForm');
        menuForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (selectedOptions.size === 0) {
                alert('최소 하나의 메뉴를 선택해주세요.');
                return;
            }

            const formData = new FormData(menuForm);
            formData.append('menus', JSON.stringify(Array.from(selectedOptions)));

            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken') 
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success && data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
            });
        });

        function updateButtonState() {
            confirmButton.disabled = selectedOptions.size === 0;
        }

        function toggleButtonActive(button) {
            button.classList.toggle('active');
        }

        ['hotButton', 'iceButton'].forEach(id => {
            document.getElementById(id).addEventListener('click', function() {
                ['hotButton', 'iceButton'].forEach(btnId => {
                    document.getElementById(btnId).classList.remove('active');
                });
                toggleButtonActive(this);
            });
        });

        ['regularButton', 'extraButton'].forEach(id => {
            document.getElementById(id).addEventListener('click', function() {
                ['regularButton', 'extraButton'].forEach(btnId => {
                    document.getElementById(btnId).classList.remove('active');
                });
                toggleButtonActive(this);
            });
        });

        ['noSyrupButton', 'lessSyrupButton', 'regularSyrupButton'].forEach(id => {
            document.getElementById(id).addEventListener('click', function() {
                ['noSyrupButton', 'lessSyrupButton', 'regularSyrupButton'].forEach(btnId => {
                    document.getElementById(btnId).classList.remove('active');
                });
                toggleButtonActive(this);
            });
        });
    }

    function fallbackCopyTextToClipboard(text) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            const successful = document.execCommand('copy');
            const msg = successful ? '성공적으로 복사되었습니다.' : '복사에 실패했습니다.';
            alert(msg);
        } catch (err) {
            console.error('Fallback: 복사 실패', err);
            alert("링크 복사에 실패했습니다. 수동으로 복사해주세요.");
        }

        document.body.removeChild(textArea);
    }
});
// modal창 동적 생성하는 ajax


// 중복 설정 방지
if (!window.menuInteractionsSetup) {
    document.addEventListener('DOMContentLoaded', function() {
        const guestNameForm = document.getElementById('guestNameForm');
        if (guestNameForm) {
            guestNameForm.addEventListener('submit', handleGuestNameSubmit);
        } else {
            setupMenuInteractions();
        }
    });
    window.menuInteractionsSetup = true;
}

function debounce(func, wait) { // 디바운스 함수로 호출 지연(timeout) -> post 요청이 두 번 가는 것 방지
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function handleGuestNameSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const submitButton = e.target.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error('Server error: ' + text);
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred: ' + error.message);
    })
    .finally(() => {
        submitButton.disabled = false;
    });
}

// 메뉴 선택 상호작용
function setupMenuInteractions() {
    const menuItems = document.querySelectorAll('.menu-item');
    const modal = document.getElementById('menuDetailModal');
    const modalTitle = document.getElementById('menuDetailModalLabel');
    const modalImage = document.getElementById('modalMenuImage');
    const saveMenuItem = document.getElementById('saveMenuItem');
    const closeBtn = modal.querySelector('.close');
    const confirmButton = document.getElementById('confirmButton');
    const selectedOptions = new Set();

    function resetModal() {
        ['hotButton', 'iceButton', 'regularButton', 'extraButton', 'bigIceButton', 'regularIceButton', 'lessIceButton'].forEach(id => {
            document.getElementById(id).classList.remove('active');
        });
        document.getElementById('additionalInstructions').value = '';
    }

    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const menuId = this.getAttribute('data-menu-id');
            const menuName = this.querySelector('.menu-name').textContent;
            const menuImageSrc = this.querySelector('.menu-image')?.src;

            modalTitle.textContent = menuName;
            if (menuImageSrc) {
                modalImage.src = menuImageSrc;
                modalImage.style.display = 'block';
            } else {
                modalImage.style.display = 'none';
            }

            resetModal();
            modal.style.display = 'block';
            saveMenuItem.setAttribute('data-menu-id', menuId);
        });
    });

    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    saveMenuItem.addEventListener('click', function() {
        const menuId = this.getAttribute('data-menu-id');
        const temperature = document.querySelector('#hotButton.active, #iceButton.active') ? document.querySelector('#hotButton.active, #iceButton.active').textContent.trim() : '';
        const size = document.querySelector('#regularButton.active, #extraButton.active') ? document.querySelector('#regularButton.active, #extraButton.active').textContent.trim() : '';
        const ice = document.querySelector('#bigIceButton.active, #regularIceButton.active, #lessIceButton.active') ? document.querySelector('#bigIceButton.active, #regularIceButton.active, #lessIceButton.active').textContent.trim() : '';
        const instructions = document.getElementById('additionalInstructions').value;

        selectedOptions.add({
            id: menuId,
            options: { temperature, size, ice, instructions }
        });

        updateButtonState();
        modal.style.display = 'none';
    });

    const menuForm = document.getElementById('menuForm');
    menuForm.addEventListener('submit', debounce(function(e) {
        e.preventDefault();
        if (selectedOptions.size === 0) {
            alert('최소 하나의 메뉴를 선택해주세요.');
            return;
        }

        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        const formData = new FormData(menuForm);
        formData.append('menus', JSON.stringify(Array.from(selectedOptions)));

        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server responded with an error');
            }
            return response.json();
        })
        .then(data => {
            if (data.success && data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                throw new Error('Invalid server response');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('주문 처리 중 오류가 발생했습니다: ' + error.message);
        })
        .finally(() => {
            submitButton.disabled = false;
        });
    }, 300));

    function updateButtonState() {
        confirmButton.disabled = selectedOptions.size === 0;
    }

    function toggleButtonActive(button) {
        button.classList.toggle('active');
    }

    ['hotButton', 'iceButton'].forEach(id => {
        document.getElementById(id).addEventListener('click', function() {
            ['hotButton', 'iceButton'].forEach(btnId => {
                document.getElementById(btnId).classList.remove('active');
            });
            toggleButtonActive(this);
        });
    });

    ['regularButton', 'extraButton'].forEach(id => {
        document.getElementById(id).addEventListener('click', function() {
            ['regularButton', 'extraButton'].forEach(btnId => {
                document.getElementById(btnId).classList.remove('active');
            });
            toggleButtonActive(this);
        });
    });

    ['bigIceButton', 'regularIceButton', 'lessIceButton'].forEach(id => {
        document.getElementById(id).addEventListener('click', function() {
            ['bigIceButton', 'regularIceButton', 'lessIceButton'].forEach(btnId => {
                document.getElementById(btnId).classList.remove('active');
            });
            toggleButtonActive(this);
        });
    });
}
// 모달 창(주문 상세 페이지) 상세 정보를 클릭하고 그걸 db로 보내는 ajax