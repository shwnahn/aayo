document.addEventListener('DOMContentLoaded', function() {
    console.log('main.js DOM loading');
    
    // 링크 공유하기 버튼 눌렀을 때 클립보드에 링크 복사 AJAX
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    const roomLink = document.getElementById('roomLink');
    if (copyLinkBtn && roomLink) {
        console.log('Event listener added');
        copyLinkBtn.addEventListener('click', function() {
            console.log('copyLinkBtn clicked', new Date().getTime());
            const linkToCopy = roomLink.href;
            console.log('방 링크:', linkToCopy)
            navigator.clipboard.writeText(linkToCopy).then(() => {
                alert("방 링크가 클립보드에 복사되었습니다!");
            }).catch(err => {
                console.error('클립보드 복사 실패:', err);
                // API 호출 오류날 때 대체기능 함수
                fallbackCopyTextToClipboard(linkToCopy);
            });
        });
    };

    // 링크 공유하기 버튼 눌렀을 때 모달 뜨는 기능
    const openHeartBtn = document.getElementById('open-modal-btn');
    const heartModal = document.querySelector('.share-modal');
    const heartCloseBtn = document.querySelector('.share-close');
    const modalOverlay = document.getElementById('modal-overlay');


    if (openHeartBtn && heartModal) {
        console.log('openModal 버튼과 모달 요소 찾음');
        openHeartBtn.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            console.log('open modal 버튼 클릭됨');
            heartModal.classList.remove('hidden');
            modalOverlay.classList.remove('hidden');

        });
    } else {
        // alert('openModal 버튼 또는 모달 요소를 찾을 수 없음');
    }
    
    if (heartCloseBtn && heartModal) {
        console.log('shareClose 버튼과 모달 요소 찾음');
        heartCloseBtn.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            console.log('close modal 버튼 클릭됨');
            heartModal.classList.add('hidden');
            modalOverlay.classList.add('hidden');


        });
    } else {
        // alert('shareClose 버튼 또는 모달 요소를 찾을 수 없음');
    }
    
    console.log('main.js DOM fully loaded');

});

// 하트 버튼 눌렀을 때 후원 모달 뜨게
document.addEventListener('DOMContentLoaded', function() {
    const openHeartBtn = document.getElementById('open-heart-btn');
    const heartModal = document.getElementById('heart-modal');
    const heartCloseBtn = document.querySelector('.heart-close');
    const modalOverlay = document.getElementById('modal-overlay');


    if (openHeartBtn && heartModal) {
        console.log('heartModal 버튼과 모달 요소 찾음');
        openHeartBtn.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            console.log('heart modal 버튼 클릭됨');
            heartModal.classList.remove('hidden');
            modalOverlay.classList.remove('hidden');

        });
    } else {
        console.error('openHeartBtn 또는 heartModal 요소를 찾을 수 없음');
    }

    if (heartCloseBtn && heartModal) {
        console.log('heartClose 버튼과 모달 요소 찾음');
        heartCloseBtn.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            console.log('close modal 버튼 클릭됨');
            heartModal.classList.add('hidden');
            modalOverlay.classList.add('hidden');

        });
    } else {
        console.error('heartCloseBtn 또는 heartModal 요소를 찾을 수 없음');
    }

    console.log('DOM fully loaded');
});
    
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

// Kakao SDK를 비동기적으로 로드
(function loadKakaoSDK() {
    const script = document.createElement('script');
    script.src = "https://t1.kakaocdn.net/kakao_js_sdk/2.7.2/kakao.min.js";
    script.integrity = "sha384-TiCUE00h649CAMonG018J2ujOgDKW/kVWlChEuu4jK2vxfAAD0eZxzCKakxg55G4";
    script.crossOrigin = "anonymous";
    script.onload = initKakao;
    document.head.appendChild(script);
})();

function initKakao() {
    if (typeof Kakao === 'undefined') {
        console.error('Kakao SDK가 로드되지 않았습니다.');
        return;
    }

    // SDK 초기화
    Kakao.init('{{ KAKAO_APP_KEY }}');
    console.log('Kakao SDK 초기화 상태:', Kakao.isInitialized());

    // 카톡 공유 버튼 이벤트 리스너 설정
    const kakaoShareBtn = document.getElementById('kakaoShareBtn');
    if (kakaoShareBtn) {
        kakaoShareBtn.addEventListener('click', shareKakao);
    } else {
        console.error('카카오 공유 버튼을 찾을 수 없습니다.');
    }
}

function shareKakao() {
    const roomLink = document.getElementById('roomLink')?.href;
    if (!roomLink) {
        console.error('방 링크를 찾을 수 없습니다.');
        return;
    }

    Kakao.Share.sendDefault({
        objectType: 'feed',
        content: {
            title: '아아요! 에 초대합니다',
            description: '함께 메뉴를 골라보아요!',
            imageUrl: '/static/images/aayo_logo_yellow.png', // 절대 경로로 수정
            link: {
                mobileWebUrl: roomLink,
                webUrl: roomLink,
            },
        },
        buttons: [
            {
                title: '메뉴 고르러 가기',
                link: {
                    mobileWebUrl: roomLink,
                    webUrl: roomLink,
                },
            },
        ],
    }).then(function(response) {
        console.log(response);
    }).catch(function(error) {
        console.error('카카오 공유 중 오류 발생:', error);
    });
}