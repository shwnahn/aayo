const menuItems = document.querySelectorAll('.menu-item');

menuItems.forEach(item => {
    item.addEventListener('click', function() {
        // 메뉴 항목의 데이터 속성 값을 가져와 모달 창에 표시
        const menuName = this.querySelector('.menu-name').textContent;
        console.log(menuName);

        // 모달 창의 제목과 이미지 설정
    });
})

console.log(1);
console.log(2);
console.log(3);
console.log(4);
console.log(5);
console.log(6);
console.log(7);
console.log(8);
console.log(9);
console.log(10);