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
    const openModalBtn = document.getElementById('open-modal-btn');
    const shareModal = document.querySelector('.share-modal');
    const shareCloseBtn = document.querySelector('.share-close');

    if (openModalBtn && shareModal) {
        console.log('openModal 버튼과 모달 요소 찾음');
        openModalBtn.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            console.log('open modal 버튼 클릭됨');
            alert('open modal');
            shareModal.classList.remove('hidden');
        });
    } else {
        // alert('openModal 버튼 또는 모달 요소를 찾을 수 없음');
    }
    
    if (shareCloseBtn && shareModal) {
        console.log('shareClose 버튼과 모달 요소 찾음');
        shareCloseBtn.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            console.log('close modal 버튼 클릭됨');
            shareModal.classList.add('hidden');

        });
    } else {
        // alert('shareClose 버튼 또는 모달 요소를 찾을 수 없음');
    }
    
    console.log('main.js DOM fully loaded');
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
