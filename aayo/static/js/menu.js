const selectedOptions = new Set();

document.addEventListener('DOMContentLoaded', function() {
    const guestNameForm = document.getElementById('guestNameForm');
    if (guestNameForm) {
        console.log('guestName 입력 필요');
        guestNameForm.addEventListener('submit', handleGuestNameSubmit);
    } else {
        loadSelectedOptions();
        console.log(selectedOptions);
        setupMenuInteractions();
        updateUIFromSelectedOptions();
    }
});

// # 서버(html 코드)에서 가져온 데이터를 사용해 selectedOptions에 기존값 불러오기
function loadSelectedOptions() {
    const selectedMenuIds = JSON.parse(document.getElementById('selectedMenuIds').textContent);
    const selectedMenuOptions = JSON.parse(document.getElementById('selectedMenuOptions').textContent);
    // selectedOptions에 메뉴 ID와 옵션을 한 번에 추가
    selectedMenuIds.forEach(id => {
        selectedOptions.add({
            id: id,
            options: selectedMenuOptions[id]
        });
    });
}

// # GuestNameForm 제출 처리
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

// [UI 업데이트] selected 클래스 추가하는 함수
function updateItemClassSelected(menuItem, isSelected) {
    if (isSelected) {
        menuItem.classList.add('selected');
    } else {
        menuItem.classList.remove('selected');
    }
}

// [UI 업데이트] 확인 버튼 상태 업데이트 함수
function updateConfirmButtonState() {
    const confirmButton = document.getElementById('confirmButton');
    if (confirmButton) {
        confirmButton.disabled = selectedOptions.size === 0;
    }
}

// [UI 업데이트] 선택된 메뉴 이름 상단 요약 - 업데이트 함수
function updateSelectedMenuNames() {
    const selectedMenuNames = Array.from(selectedOptions).map(option => {
        // selectedOption 집합의 option에 저장된 id와 동일한 id를 가진 메뉴 아이템을 불러와서,
        const menuItem = document.querySelector(`.menu-item[data-menu-id="${option.id}"]`);
        // (삼항 연산자) 그 메뉴 아이템의 메뉴 이름을 반환, 만약 메뉴 아이템이 존재하지 않으면(거의 그럴 일 없음) 빈 문자열을 반환
        return menuItem ? menuItem.querySelector('.menu-name').textContent : '';
    });

    const selectedMenuNamesElement = document.getElementById('selectedMenuNames');
    
    if (selectedMenuNames.length === 0) { // 선택한 메뉴 아이템이 없는 경우(배열의 길이가 0인 경우)
        selectedMenuNamesElement.textContent = "메뉴를 선택해주세요.";
    } else {
        selectedMenuNamesElement.textContent = selectedMenuNames.join(', ');
    }
}

// # 전체 아이템 UI 업데이트
function updateUIFromSelectedOptions() {
    // 모든 메뉴 항목에 대해 selected 상태를 업데이트
    document.querySelectorAll('.menu-item').forEach(item => {
        const menuId = item.getAttribute('data-menu-id');
        const isSelected = Array.from(selectedOptions).some(option => {
            // menuId와 option.id를 같은 자료형으로 변환 후 비교 (number로 변환)
            return Number(option.id) === Number(menuId);
        });
        // isSelected에 따라 클래스 업데이트
        updateItemClassSelected(item, isSelected);
    });
     
    // 선택된 메뉴 이름 업데이트
    updateSelectedMenuNames();
    // 확인 버튼 상태 업데이트
    updateConfirmButtonState();
}


// [메뉴 선택 상호작용] 메뉴 검색창 코드
function setupSearchFunctionality(menuItems) {
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
}

// [메뉴 선택 상호작용] 메뉴선택 modal 셋업 코드
function setupMenuModal(modal, menuName, menuImageSrc, menuCategory, menuNote, menuId) {
    const modalTitle = document.getElementById('menuDetailModalLabel');
    const modalMenuCategory = document.getElementById('menuCategory');
    const modalMenuNote = document.getElementById('menuNote');
    const modalImage = document.getElementById('modalMenuImage');
    modalTitle.textContent = menuName;
    modalMenuCategory.textContent = menuCategory !== 'None' ? menuCategory : '';
    modalMenuNote.textContent = menuNote !== 'None' ? menuNote : '';
    // 해당 메뉴 이미지 없으면 display: none
    if (menuImageSrc) {
        modalImage.src = menuImageSrc;
        modalImage.style.display = 'block';
    } else {
        modalImage.style.display = 'none';
    }

    resetModal();
    openMenuModal();
    document.getElementById('saveMenuItem').setAttribute('data-menu-id', menuId); // menuId 저장

    // 닫기 버튼에 이벤트리스너 추가
    const closeBtn = modal.querySelector('.close');
    if (closeBtn && !closeBtn.dataset.listenerAdded) {
        closeBtn.addEventListener('click', function() {
            closeMenuModal();
        });
        closeBtn.dataset.listenerAdded = 'true'; // 이벤트 리스너 중복 방지 플래그 설정
    }
}

// # 메뉴 선택 상호작용 - 모달 창(주문 상세 페이지) 상세 정보를 클릭하고 그걸 db로 보내는 ajax
function setupMenuInteractions() {
    console.log('# setupMenuInteractions 함수 실행');
    const menuItems = document.querySelectorAll('.menu-item');
    const modal = document.getElementById('menuDetailModal');
    
    
    // 메뉴 검색창 이벤트리스너 추가
    setupSearchFunctionality(menuItems);

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
            console.log("Clicked menu ID:", menuId);  // menuId가 올바르게 출력되는지 확인
            if (!menuId) {
                console.error("Menu ID not found! Something is wrong.");
                return;  // menuId가 null이거나 undefined이면 동작 중단
            }
            const menuName = this.querySelector('.menu-name').textContent;
            const menuImageSrc = this.querySelector('.menu-image')?.src;
            const menuCategory = this.getAttribute('data-menu-category');
            const menuNote = this.getAttribute('data-menu-note');

            // 이미 선택된 메뉴를 다시 클릭할 시 선택 취소 및 커스텀 초기화
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');

                // selectedOptions에서 해당 메뉴를 삭제합니다.
                const existingSelection = Array.from(selectedOptions).find(option => Number(option.id) === Number(menuId)); // Number로 비교
                if (existingSelection) {
                    selectedOptions.delete(existingSelection); // Set에서 해당 메뉴 삭제
                }

                // UI 업데이트: 해당 메뉴 항목에서 'selected' 클래스 제거
                updateItemClassSelected(this, false);
                updateConfirmButtonState();
                // UI 업데이트: 선택된 메뉴 이름 상단 요약에서 해당 아이템 삭제
                updateSelectedMenuNames();

                // 커스텀 옵션 초기화 후 사용자에게 다시 설정할 수 있도록 모달을 재오픈
                alert('커스텀 내역을 수정하시겠습니까?');

                setupMenuModal(modal, menuName, menuImageSrc, menuCategory, menuNote, menuId);
                return;
            }

            setupMenuModal(modal, menuName, menuImageSrc, menuCategory, menuNote, menuId);
        });
    });

    // 모달 창 외부 클릭 시 모달 창 닫기
    window.onclick = function(event) {
        if (event.target == modal) {
            closeMenuModal()
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

            // 중복 항목 업데이트 로직 추가
            const existingOption = Array.from(selectedOptions).find(option => Number(option.id) === Number(menuId)); // Number로 비교
            if (existingOption) {
                existingOption.options = { temperature, size, ice, note };
            } else {
                selectedOptions.add({
                    id: menuId,
                    options: { 
                        temperature, size, ice, note
                    }
                });
            }
            console.log(selectedOptions);

            // UI 업데이트: 선택된 메뉴 항목에 'selected' 클래스 추가
            const menuItem = document.querySelector(`.menu-item[data-menu-id="${menuId}"]`);
            if (menuItem) {
                updateItemClassSelected(menuItem, true);
            }

            updateConfirmButtonState();
            updateSelectedMenuNames();
            closeMenuModal()

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

function openMenuModal() {
    const modal = document.getElementById('menuDetailModal');
    modal.classList.add('show');
    modal.style.display = 'block';
    // const shareBtn = document.getElementById('open-modal-btn');
    // shareBtn.classList.add('hidden');
}
function closeMenuModal() {
    const modal = document.getElementById('menuDetailModal');
    modal.classList.remove('show');
    modal.style.display = 'none';
    // const shareBtn = document.getElementById('open-modal-btn');
    // shareBtn.classList.remove('hidden');
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