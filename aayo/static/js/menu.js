document.addEventListener('DOMContentLoaded', function() {
    const guestNameForm = document.getElementById('guestNameForm');
    if (guestNameForm) {
        console.log('guestName 입력 필요');
        guestNameForm.addEventListener('submit', handleGuestNameSubmit);
    } else {
        console.log(selectedOptions);
        setupMenuInteractions(); // 메뉴 선택 상호작용 - 모달 창(주문 상세 페이지) 상세 정보를 클릭하고 그걸 db로 보내는 ajax
        markSelectedMenus(); // 기존 선택 메뉴 표시 함수 호출
        updateSelectedMenuNames();  // 페이지 로드 시 기존 선택 메뉴 이름 업데이트
        updateButtonState();  // 확인 버튼 상태 업데이트 함수
    }
});

const selectedOptions = new Set();
const confirmButton = document.getElementById('confirmButton');

// 확인 버튼 상태 업데이트 함수
function updateButtonState() {
    if (confirmButton) {
        confirmButton.disabled = selectedOptions.size === 0;
    }
}

// GuestNameForm 제출 처리
function handleGuestNameSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const submitButton = e.target.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    // [POST] GuestNameForm
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

 // 메뉴 선택 시 'Selected' 클래스 추가 함수
function markSelectedMenus() {
    const selectedMenuIds = JSON.parse(document.getElementById('selectedMenuIds').textContent);
    const selectedMenuOptions = JSON.parse(document.getElementById('selectedMenuOptions').textContent);
    selectedMenuIds.forEach(id => {
        const menuItem = document.querySelector(`.menu-item[data-menu-id="${id}"]`);
        if (menuItem) {
            menuItem.classList.add('selected');
            const selectedOption = {
                id: id,
                options: selectedMenuOptions[id]  // 메뉴 옵션 업데이트
            };
            selectedOptions.add(selectedOption);  // selectedOptions에 기존 선택된 메뉴 추가
            console.log('selectedOption:', selectedOption);
        }
    });
    updateSelectedMenuNames();
    updateButtonState();  // 페이지 로드 시 확인 버튼 상태 업데이트
}

// 선택된 메뉴 이름 상단 요약 - 업데이트 함수
function updateSelectedMenuNames() {
    const selectedMenuNames = Array.from(selectedOptions).map(option => {
        // selectedOption 집합의 option에 저장된 id와 동일한 id를 가진 메뉴 아이템을 불러와서,
        const menuItem = document.querySelector(`.menu-item[data-menu-id="${option.id}"]`);
        // (삼항 연산자) 그 메뉴 아이템의 메뉴 이름을 반환, 만약 메뉴 아이템이 존재하지 않으면(거의 그럴 일 없음) 빈 문자열을 반환
        return menuItem ? menuItem.querySelector('.menu-name').textContent : '';
    })
    // 저장된 메뉴 배열의 요소들을 ', '로 구분하여 텍스트로 표시! 
    document.getElementById('selectedMenuNames').textContent = selectedMenuNames.join(', ');
}

// 메뉴 선택 상호작용 - 모달 창(주문 상세 페이지) 상세 정보를 클릭하고 그걸 db로 보내는 ajax
function setupMenuInteractions() {
    console.log('# 메뉴 선택 함수 실행');
    const menuItems = document.querySelectorAll('.menu-item');
    console.log('menuItems:', menuItems);
    const modal = document.getElementById('menuDetailModal');
    console.log('modal:', modal);
    const modalTitle = document.getElementById('menuDetailModalLabel');
    console.log('modalTitle:', modalTitle);
    const modalMenuCategory = document.getElementById('menuCategory');
    const modalMenuNote = document.getElementById('menuNote');

    const modalImage = document.getElementById('modalMenuImage');
    console.log('modalImage:', modalImage);
    
    // 메뉴 검색창 이벤트리스너 추가
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

    // 각 메뉴 항목에 클릭 이벤트 리스너 추가 [ 모달을 여는 코드 ]
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const menuId = this.getAttribute('data-menu-id');
            const menuName = this.querySelector('.menu-name').textContent;
            const menuImageSrc = this.querySelector('.menu-image')?.src;
            const menuCategory = this.getAttribute('data-menu-category');
            const menuNote = this.getAttribute('data-menu-note');

            // 선택된 메뉴를 다시 클릭할 시 선택 취소 [ 커스텀 초기화 코드 ]
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
                selectedOptions.delete(Array.from(selectedOptions).find(option => option.id === menuId));
                updateButtonState();
                updateSelectedMenuNames();
                alert('커스텀을 수정하시겠습니까?')
                resetModal(); // 모달 초기화 (기존 선택내역 초기화)
                openModal(); // 사용자 편의를 위해 모달을 다시 열어줌
                return;
            }
            
            modalTitle.textContent = menuName;
            if (menuCategory == 'None') {
                modalMenuCategory.textContent = '';
            } else {
                modalMenuCategory.textContent = menuCategory;
            }
            if (menuNote == 'None') {
                modalMenuNote.textContent = '';
            } else {
                modalMenuNote.textContent = menuNote;
            }

            // 해당 메뉴 이미지 없으면 display: none
            if (menuImageSrc) {
                modalImage.src = menuImageSrc;
                modalImage.style.display = 'block';
            } else {
                modalImage.style.display = 'none';
            }

            // 모달 초기화 후 열기
            resetModal();
            openModal();;
            saveMenuItem.setAttribute('data-menu-id', menuId);

            // 닫기 버튼에 이벤트리스너 추가
            const closeBtn = modal.querySelector('.close');
            if (closeBtn && !closeBtn.dataset.listenerAdded) {
                closeBtn.addEventListener('click', function() {
                    closeModal()
                });
                closeBtn.dataset.listenerAdded = 'true'; // 이벤트 리스너 중복 방지 플래그 설정
            }
        });
    });

    // 모달 창 외부 클릭 시 모달 창 닫기
    window.onclick = function(event) {
        if (event.target == modal) {
            closeModal()
        }
    }

    // hot 버튼이 클릭 되면 얼음 선택 옵션 버튼들이 비활성화되도록 만들기
    const hotButton = document.getElementById('hotButton');
    const iceButton = document.getElementById('iceButton');
    const iceOptions = document.querySelectorAll('#bigIceButton, #regularIceButton, #lessIceButton');
    const iceOptionsGroup = document.querySelector('.custom-ice');
    if (hotButton && iceButton) {
        
        function disableIceOptions() {
            // button.style.display = 'none'; 에서 buttonGroup class hidden 으로 작동하도록 수정!
            iceOptionsGroup.classList.add('hidden');
            iceOptions.forEach(button => {
                // disabled 대신 아예 사라지게 만듦
                button.classList.remove('active');
            });
        }

        function enableIceOptions() {
            // button.style.display = 'block'; -> buttonGroup class에서 remove hidden 으로 작동하도록 수정!
            iceOptionsGroup.classList.remove('hidden'); 
        }

        // pointerdown -> 터치, 클릭 모두 인식
        hotButton.addEventListener('click', disableIceOptions);
        iceButton.addEventListener('click', enableIceOptions);
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

            console.log('Selected temperature:', temperature); // 디버깅용
            console.log('Selected ice:', ice); // 디버깅용

            // 필수 항목 검증
            if (!temperature) {
                alert('온도를 선택해주세요!');
                return;
            }
            // if (!size) {
            //     alert('크기를 선택해주세요!');
            //     return;
            // }
            // // ice 버튼을 눌렀을 때만 얼음 양 선택을 필수로 하도록 만들기
            // if (temperature.includes('ICE') && !ice) {
            //     alert('얼음 양을 선택해주세요!');
            //     return;
            // }
            // 선택된 옵션들을 Set에 추가 - selectedOptions
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
            closeModal()

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
        // selectedOptions 데이터를 JSON 문자열로 변환 - 'menu_details' 라는 key로 formData 추가
        formData.append('menu_details', JSON.stringify(Array.from(selectedOptions)));
        
        // [POST] MenuForm Formdata 제출
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


function openModal() {
    const modal = document.getElementById('menuDetailModal');
    const shareBtn = document.getElementById('open-modal-btn');
    modal.classList.add('show');
    modal.style.display = 'block';
    shareBtn.classList.add('hidden');
}
function closeModal() {
    const modal = document.getElementById('menuDetailModal');
    const shareBtn = document.getElementById('open-modal-btn');
    modal.classList.remove('show');
    modal.style.display = 'none';
    shareBtn.classList.remove('hidden');
}

// 모달 초기화 함수
function resetModal() {
    ['hotButton', 'regularButton', 'extraButton', 'bigIceButton', 'regularIceButton', 'lessIceButton'].
    // icebutton은 기본값이므로 제거함.
    forEach(id => {
        document.getElementById(id).classList.remove('active');
    });
    document.getElementById('additionalInstructions').value = '';
}