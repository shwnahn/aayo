document.addEventListener('DOMContentLoaded', function() {
    const guestNameForm = document.getElementById('guestNameForm-container');
    
    updateButtonState();

    guestNameInput.addEventListener('input', updateButtonState);

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
    // 메뉴 검색창 가져오기
    const searchInput = document.getElementById('menuSearch');

    searchInput.addEventListener('input', function () {
        // '검색어 입력' 이벤트리스너 추가
        const searchTerm = this.value.toLowerCase();
        // 대소문자 구분 없이 검색 가능하도록 toLowercase함수 적용
        menuItems.forEach(item => {
            const menuName = item.querySelector('.menu-name').textContent.toLowerCase();
            // 메뉴 아이템의 메뉴 이름을 가져와서 소문자로 변경 후 저장
            if (menuName.includes(searchTerm)) {
            // 메뉴 이름에 유저가 입력한 검색어가 포함되는 경우
                item.style.display = '';
                // 그 메뉴 아이템만 보여줌
            } else {
                item.style.display = 'none'
            }
        });
    });

    // 선택된 메뉴 이름 업데이트 함수
    function updateSelectedMenuNames() {
        const selectedMenuNames = Array.from(selectedOptions).map(option => {
            const menuItem = document.querySelector(`.menu-item[data-menu-id="${option.id}"]`);
            // selectedOption 집합의 option에 저장된 id와 동일한 id를 가진 메뉴 아이템을 불러와서,
            return menuItem ? menuItem.querySelector('.menu-name').textContent : '';
            // (삼항 연산자) 그 메뉴 아이템의 메뉴 이름을 반환, 만약 메뉴 아이템이 존재하지 않으면(거의 그럴 일 없음) 빈 문자열을 반환
        })
        document.getElementById('selectedMenuNames').textContent = selectedMenuNames.join(', ');
        // 저장된 메뉴 배열의 요소들을 ', '로 구분하여 텍스트로 표시! 
    }

    // 모달 초기화 함수
    function resetModal() {
        ['hotButton', 'iceButton', 'regularButton', 'extraButton', 'bigIceButton', 'regularIceButton', 'lessIceButton'].
        forEach(id => {
            document.getElementById(id).classList.remove('active');
        });
        document.getElementById('additionalInstructions').value = '';
    }

    // 확인 버튼 상태 업데이트 함수
    function updateButtonState() {
        confirmButton.disabled = selectedOptions.size === 0;

        // 로그인 버튼 상태
        const submitButton = document.getElementById('goToOrderBtn');
        
        if (guestNameInput.value.trim() === '') {
            // 이름이 비어있을 경우 버튼을 비활성화하고 회색으로 변경
            submitButton.disabled = true;
            submitButton.style.backgroundColor = '#d3d3d3';
            submitButton.style.cursor = 'not-allowed';
        } else {
            // 이름이 입력되었을 경우 버튼을 활성화하고 노란색으로 변경
            submitButton.disabled = false;
            submitButton.style.backgroundColor = '#ffc107';
            submitButton.style.cursor = 'pointer';
        }
    }

    function toggleButtonActive(button) {
        button.classList.toggle('active');
    }

    // 메뉴 상세 선택 - 버튼 활성화 토글 설정 함수
    function setupToggleButtons(buttonIds) {
        buttonIds.forEach(id => {
            const button = document.getElementById(id);
            if (button) {
                button.addEventListener('click', function() {
                    console.log(`Button clicked: ${id}`);
                    buttonIds.forEach(btnId => {
                        document.getElementById(btnId).classList.remove('active');
                    });
                    this.classList.add('active');
                    console.log(`Active button: ${id}`);
                });
            } else {
                console.warn(`Button not found: ${id}`);
            }
        });
    }

    // 각 메뉴 항목에 클릭 이벤트 리스너 추가
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const menuId = this.getAttribute('data-menu-id');
            const menuName = this.querySelector('.menu-name').textContent;
            const menuImageSrc = this.querySelector('.menu-image')?.src;

            // 선택된 메뉴를 다시 클릭할 시 선택 취소
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
                selectedOptions.delete(Array.from(selectedOptions).find(option => option.id === menuId));
                updateButtonState();
                updateSelectedMenuNames();
                alert('커스텀을 수정하시겠습니까?')
                resetModal(); // 모달 초기화 (기존 선택내역 초기화)
                modal.style.display = 'block' // 사용자 편의를 위해 모달을 다시 열어줌
                return;
            }

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

            const closeBtn = modal.querySelector('.close');
            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    modal.style.display = 'none';
                });
            }
        });
    });

    // 모달 창 외부 클릭 시 모달 창 닫기
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // 모달창에서 '내 메뉴 저장하기' 버튼 클릭 시 선택된 옵션 저장
    const saveMenuItem = document.getElementById('saveMenuItem');
    if (saveMenuItem) {
        saveMenuItem.addEventListener('click', function() {
            const menuId = this.getAttribute('data-menu-id');
            const temperature = document.querySelector('#hotButton.active, #iceButton.active') ? document.querySelector('#hotButton.active, #iceButton.active').textContent.trim() : '';
            const size = document.querySelector('#regularButton.active, #extraButton.active') ? document.querySelector('#regularButton.active, #extraButton.active').textContent.trim() : '';
            const ice = document.querySelector('#bigIceButton.active, #regularIceButton.active, #lessIceButton.active') ? document.querySelector('#bigIceButton.active, #regularIceButton.active, #lessIceButton.active').textContent.trim() : '';
            const note = document.getElementById('additionalInstructions').value;

            // 필수 항목 검증
            if (!temperature) {
                alert('온도를 선택해주세요!');
                return;
            }
            if (!size) {
                alert('크기를 선택해주세요!');
                return;
            }
            if (!ice) {
                alert('얼음 양을 선택해주세요!');
                return;
            }
            // 선택된 옵션들을 Set에 추가
            selectedOptions.add({
                id: menuId,
                options: { 
                    temperature, size, ice, note
                }
            });
            
            // selected_menu_ids.add(menuId);  // 수정된 부분
            const menuItem = document.querySelector(`.menu-item[data-menu-id="${menuId}"]`);
            if (menuItem) {
                menuItem.classList.add('selected');
            }

            updateButtonState();
            updateSelectedMenuNames();
            modal.style.display = 'none';

            console.log('메뉴가 저장되었습니다:', menuId);
        });
    };
    
    // 메뉴 폼 제출 처리
    const menuForm = document.getElementById('menuForm');
    menuForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (selectedOptions.size === 0) {
            alert('최소 하나의 메뉴를 선택해주세요.');
            return;
        }

        const submitButton = this.querySelector('button[type="submit"]');
        if (submitButton.disabled) {return;}
        submitButton.disabled = true;

        const formData = new FormData(menuForm);
        // menus 데이터를 JSON 문자열로 변환하여 추가
        formData.append('menus', JSON.stringify(Array.from(selectedOptions)));
        

        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(async response => {
            // 응답이 JSON이 아닌 경우를 처리
            if (!response.ok) {
                const text = await response.text();
                throw new Error(text);
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
    });

    // 버튼 활성화 토글 설정
    if (modal) {
        setupToggleButtons(['hotButton', 'iceButton']);
        setupToggleButtons(['regularButton', 'extraButton']);
        setupToggleButtons(['bigIceButton', 'regularIceButton', 'lessIceButton']);
    }
}

// GuestNameForm 제출 처리
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