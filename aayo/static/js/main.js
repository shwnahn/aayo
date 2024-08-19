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

document.addEventListener('DOMContentLoaded', function () {
  // 카카오톡 공유 버튼
  // SDK를 초기화 (HTTP 환경에서는 실제로 초기화되지 않을 수 있음)
  Kakao.init('{{ KAKAO_APP_KEY }}');

  console.log('Kakao SDK 초기화 상태:', Kakao.isInitialized());

  // 방 링크 가져오기
  const roomLink = document.getElementById('roomLink').href;

  // 카카오톡 공유 버튼 이벤트 리스너
  document
    .getElementById('kakaoShareBtn')
    .addEventListener('click', function () {
      console.log('카카오 공유 버튼이 클릭되었습니다.');

      // 공유할 내용 객체 생성
      const shareContent = {
        objectType: 'feed',
        content: {
          title: '아아요! 에 초대합니다',
          description: '함께 메뉴를 골라보아요!',
          imageUrl: 'https://aayo.kr/static/images/aayologo.png',
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
      };

      // 콘솔에 공유 내용 출력
      console.log('공유할 내용:', JSON.stringify(shareContent, null, 2));

      // alert으로 공유 내용 표시
    //   alert(
    //     '카카오톡 공유 내용:\n\n' +
    //       '제목: ' +
    //       shareContent.content.title +
    //       '\n' +
    //       '설명: ' +
    //       shareContent.content.description +
    //       '\n' +
    //       '링크: ' +
    //       shareContent.content.link.webUrl +
    //       '\n\n' +
    //       '실제 환경에서는 카카오톡 공유 다이얼로그가 열립니다.'
    //   );

      // HTTP 환경에서는 실제 Kakao.Link.sendDefault 함수가 작동하지 않으므로 주석 처리
        Kakao.Link.sendDefault(shareContent);
    });
});