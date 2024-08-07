document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loading');

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

    // 카페 선택 안하고 넘어가는 것 막는 코드
    const createRoomForm = document.getElementById('createRoomForm');
    if (createRoomForm) {
        createRoomForm.addEventListener('submit', function(e) {
            if (!cafeInput.value) {
                e.preventDefault(); // 폼 제출을 막습니다.
                alert('카페를 선택해주세요!');
            }
        });
    }
    
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
    };
    
    console.log('DOM fully loaded');
});

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
