$(document).ready(function () {
    //문서가 준비됐을때 실행되는 함수
    $('#btn').on('click', function () {
        // 현재 텍스트가 'front'인지 확인
        // if ($('#target-text').text() === 'front') {
        //     $('#target-text').text('back');  // 'front'이면 'back'으로 변경
        // } else {
        //     $('#target-text').text('front'); // 'back'이면 다시 'front'로 변경
        // }
        // input 창에 입력된 현재 값을 가져옵니다.
        var inputValue = $('#input-text').val();

        // 1. 만약 입력창이 비어있다면, 토글 동작을 하지 않고 경고를 띄웁니다. (선택 사항)
        if (!inputValue) {
            alert('텍스트를 입력해주세요!');
            return;
        }

        // 2. 현재 글자가 'front'라면 입력받은 값으로 변경합니다.
        if ($('#target-text').text() === 'front') {
            $('#target-text').text(inputValue);
        } else {
            // 3. 이미 입력받은 값으로 바뀌어 있는 상태라면 다시 'front'로 되돌립니다.
            $('#target-text').text('front');
        }

        //강사님 풀이
        // var v = $('#input-text').val();
        // $('#text-value').text(v);
    });
});
