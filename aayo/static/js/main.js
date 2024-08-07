document.addEventListener('DOMContentLoaded', function() {
     // 중복 설정 방지 코드
     if (!window.menuInteractionsSetup) {
        const guestNameForm = document.getElementById('guestNameForm');
        if (guestNameForm) {
            guestNameForm.addEventListener('submit', handleGuestNameSubmit);
        }
        setupMenuInteractions(); // 메뉴 선택 상호작용 관련 함수 불러오기
        window.menuInteractionsSetup = true;
    }

    // room.html 에서 카페 리스트 선택 시 AJAX
    const cafeLogos = document.querySelectorAll('.cafe-logo');
    const cafeInput = document.getElementById('cafe');
    cafeLogos.forEach(logo => {
        logo.addEventListener('click', function() {
            // 모든 로고에서 'selected' 클래스를 제거하여 선택되지 않은 상태로 만들기
            cafeLogos.forEach(logo => logo.classList.remove('selected'));
            // 클릭한 로고에 'selected' 클래스를f 추가하여 선택된 상태로 만들기
            this.classList.add('selected');
            // 클릭한 로고의 'data-cafe' 속성 값을 가져와 'cafeInput' 요소의 값으로 설정
            cafeInput.value = this.getAttribute('data-cafe');
        });
    });
    
    // 링크 공유하기 버튼 눌렀을 때 클립보드에 링크 복사 AJAX
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    const roomLink = document.getElementById('roomLink');
    if (copyLinkBtn && roomLink) {
        copyLinkBtn.addEventListener('click', function() {
            const linkToCopy = roomLink.href;
            navigator.clipboard.writeText(linkToCopy).then(() => {
                alert("방 링크가 클립보드에 복사되었습니다!");
            }).catch(err => {
                console.error('클립보드 복사 실패:', err);
                // API 호출 오류날 때 대체기능 함수
                fallbackCopyTextToClipboard(linkToCopy);
            });
        });
    }

});

// 디바운스 함수로 호출 지연(timeout) -> post 요청이 두 번 가는 것 방지
function debounce(func, wait) { 
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
    .then(async response => {
        if (!response.ok) {
            const text = await response.text();
            throw new Error('Server error: ' + text);
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

// 메뉴 선택 상호작용 - 모달 창(주문 상세 페이지) 상세 정보를 클릭하고 그걸 db로 보내는 ajax
function setupMenuInteractions() {
    const menuItems = document.querySelectorAll('.menu-item');
    const modal = document.getElementById('menuDetailModal');
    const modalTitle = document.getElementById('menuDetailModalLabel');
    const modalImage = document.getElementById('modalMenuImage');
    const saveMenuItem = document.getElementById('saveMenuItem');
    const closeBtn = modal.querySelector('.close');
    const confirmButton = document.getElementById('confirmButton');
    const selectedOptions = new Set();

    // 모달 초기화 함수
    function resetModal() {
        // 각 버튼의 'active' 클래스를 제거하여 초기 상태로 만듦
        ['hotButton', 'iceButton', 'regularButton', 'extraButton', 'bigIceButton', 'regularIceButton', 'lessIceButton'].
        forEach(id => {
            document.getElementById(id).classList.remove('active');
        });
        // 추가 지시사항 입력 필드를 비움
        document.getElementById('additionalInstructions').value = '';
    }

    // 확인 버튼 상태 업데이트 함수
    function updateButtonState() {
        confirmButton.disabled = selectedOptions.size === 0;
    }

    function toggleButtonActive(button) {
        button.classList.toggle('active');
    }

    // 메뉴 상세 선택 - 버튼 활성화 토글 설정 함수
    function setupToggleButtons(buttonIds) {
        buttonIds.forEach(id => {
            document.getElementById(id).addEventListener('click', function() {
                buttonIds.forEach(btnId => {
                    document.getElementById(btnId).classList.remove('active');
                });
                this.classList.add('active');
            });
        });
    }

    // 각 메뉴 항목에 클릭 이벤트 리스너 추가
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // 메뉴 항목의 데이터 속성 값을 가져와 모달 창에 표시
            const menuId = this.getAttribute('data-menu-id');
            const menuName = this.querySelector('.menu-name').textContent;
            const menuImageSrc = this.querySelector('.menu-image')?.src;

            // 모달 창의 제목과 이미지 설정
            modalTitle.textContent = menuName;
            if (menuImageSrc) {
                modalImage.src = menuImageSrc;
                modalImage.style.display = 'block';
            } else {
                modalImage.style.display = 'none';
            }

            // 모달 창 초기화 및 열기
            resetModal();
            modal.style.display = 'block';
            saveMenuItem.setAttribute('data-menu-id', menuId);
        });
    });

    // 모달 창 닫기 버튼 클릭 시 모달 창 닫기
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    // 모달 창 외부 클릭 시 모달 창 닫기
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // "저장" 버튼 클릭 시 선택된 메뉴 옵션 저장
    saveMenuItem.addEventListener('click', function() {
        const menuId = this.getAttribute('data-menu-id');
        const temperature = document.querySelector('#hotButton.active, #iceButton.active') ? document.querySelector('#hotButton.active, #iceButton.active').textContent.trim() : '';
        const size = document.querySelector('#regularButton.active, #extraButton.active') ? document.querySelector('#regularButton.active, #extraButton.active').textContent.trim() : '';
        const ice = document.querySelector('#bigIceButton.active, #regularIceButton.active, #lessIceButton.active') ? document.querySelector('#bigIceButton.active, #regularIceButton.active, #lessIceButton.active').textContent.trim() : '';
        const instructions = document.getElementById('additionalInstructions').value;

        // 선택된 옵션들을 Set에 추가
        selectedOptions.add({
            id: menuId,
            options: { temperature, size, ice, instructions }
        });

        // 버튼 상태 업데이트 및 모달 창 닫기
        updateButtonState();
        modal.style.display = 'none';
    });

    // [POST] 메뉴 폼 제출 시 선택된 옵션들을 서버로 전송
    const menuForm = document.getElementById('menuForm');
    menuForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (selectedOptions.size === 0) {
            alert('최소 하나의 메뉴를 선택해주세요.');
            return;
        }

        const submitButton = this.querySelector('button[type="submit"]');
        if (submitButton.disabled) {return;} // 버튼이 이미 비활성화된 경우, 더블 클릭 방지
        submitButton.disabled = true;

        const formData = new FormData(menuForm);
        formData.append('menus', JSON.stringify(Array.from(selectedOptions)));

        // AJAX 요청으로 폼 데이터 전송
        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
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
    }, 300);

    // 버튼 활성화 토글 설정
    setupToggleButtons(['hotButton', 'iceButton']);
    setupToggleButtons(['regularButton', 'extraButton']);
    setupToggleButtons(['bigIceButton', 'regularIceButton', 'lessIceButton']);
}

// 링크 복사 API 안될 때 복사하기 함수(대체기능))
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