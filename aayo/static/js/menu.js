document.addEventListener('DOMContentLoaded', function() {
    const guestNameForm = document.getElementById('guestNameForm');
        if (guestNameForm) {
            console.log('guestName 입력 필요');
            guestNameForm.addEventListener('submit', handleGuestNameSubmit);
        } else {
            setupMenuInteractions();
        }
});

// 메뉴 선택 상호작용 - 모달 창(주문 상세 페이지) 상세 정보를 클릭하고 그걸 db로 보내는 ajax
function setupMenuInteractions() {
    console.log('# 함수 실행');
    const menuItems = document.querySelectorAll('.menu-item');
    console.log('menuItems:', menuItems);
    const modal = document.getElementById('menuDetailModal');
    console.log('modal:', modal);
    const modalTitle = document.getElementById('menuDetailModalLabel');
    console.log('modalTitle:', modalTitle);
    const modalImage = document.getElementById('modalMenuImage');
    console.log('modalImage:', modalImage);
    
    const confirmButton = document.getElementById('confirmButton');
    console.log('confirmButton:', confirmButton);
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

    console.log(1);

    // 확인 버튼 상태 업데이트 함수
    function updateButtonState() {
        confirmButton.disabled = selectedOptions.size === 0;
    }

    console.log(2);

    function toggleButtonActive(button) {
        button.classList.toggle('active');
    }

    console.log(3);

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

    console.log(4);

    // 각 메뉴 항목에 클릭 이벤트 리스너 추가
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // 메뉴 항목의 데이터 속성 값을 가져와 모달 창에 표시
            const menuId = this.getAttribute('data-menu-id');
            const menuName = this.querySelector('.menu-name').textContent;
            const menuImageSrc = this.querySelector('.menu-image')?.src;

            // [BORDER] 이미 선택된 메뉴인 경우, 선택 취소하는 로직 추가
            // border로 선택된 메뉴 강조하는 부분과 연계
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
                // selected 상태 삭제
                selectedOptions.delete(Array.from(selectedOptions).find(option => option.id === menuId));
                // 선택한 옵션도 삭제
                updateButtonState();
                // 주문 확정 버튼 비활성화 (시각적으로 확인할 수 있게 하면 좋을 듯)
                alert('커스텀을 변경하시겠습니까?')
                return;
            }

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

            // 모달이 열릴 때마다 닫기 버튼에 이벤트 리스너를 추가
            const closeBtn = modal.querySelector('.close');
            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    modal.style.display = 'none';
                });
            }
        });
    });

    console.log(5);

    // 모달 창 외부 클릭 시 모달 창 닫기
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    console.log(6);

    const saveMenuItem = document.getElementById('saveMenuItem');
    if (saveMenuItem) {
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

            // [BORDER] 유저가 선택한 메뉴 아이템에 'selected' 클래스 추가
            // selected로 바뀐 메뉴 아이템에 border 적용
            const menuItem = document.querySelector(`.menu-item[data-menu-id="${menuId}"]`);
            if (menuItem) {
                menuItem.classList.add('selected');
            }

            // 버튼 상태 업데이트 및 모달 창 닫기
            updateButtonState();
            modal.style.display = 'none';
        });
    };
    
    console.log(7);

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

    console.log(8);

    // 버튼 활성화 토글 설정
    if (modal) {
        setupToggleButtons(['hotButton', 'iceButton']);
        setupToggleButtons(['regularButton', 'extraButton']);
        setupToggleButtons(['bigIceButton', 'regularIceButton', 'lessIceButton']);
    }

    console.log(9);
    console.log(10);
}

// [POST] GuestNameForm를 서버로 전송
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