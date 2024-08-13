document.addEventListener('DOMContentLoaded', function() {
    console.log('room.js DOM loading');

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
    console.log('room.js DOM fully loaded');
});
