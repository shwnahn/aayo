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

    try {
        const openModalBtn = document.getElementById('open-modal-btn');
        console.log('openmodal 있다')
        if (openModalBtn) {
            openModalBtn.addEventListener('click', function() {
                console.log('open modal');
                document.getElementById('share-modal').classList.remove('hidden');
            });
        }
    } catch (error) {
        console.log('openmodal 없다')
        console.error('Error adding event listener to open modal button:', error);
    }
    
    try {
        const shareCloseBtn = document.querySelector('.share-close');
        console.log('shareClose 있다')
        if (shareCloseBtn) {
            shareCloseBtn.addEventListener('click', function() {
                console.log('close modal');
                document.getElementById('share-modal').classList.add('hidden');
            });
        }
    } catch (error) {
        console.log('shareClose 없다')
        console.error('Error adding event listener to close modal button:', error);
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
