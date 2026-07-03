$(document).ready(function () {
    $('#submit-btn').on('click', function () {
        // 1. 입력 창에서 4개의 값을 가져옵니다.
        var sepalLength = $('#sepal_length').val();
        var sepalWidth = $('#sepal_width').val();
        var petalLength = $('#petal_length').val();
        var petalWidth = $('#petal_width').val();

        // 결과창 초기화
        $('#prediction-result').hide();
        $('#result-box').removeClass('setosa versicolor virginica');

        // 콘솔창에 값 출력 (디버깅용)
        console.log('Sepal Length:', sepalLength);
        console.log('Sepal Width:', sepalWidth);
        console.log('Petal Length:', petalLength);
        console.log('Petal Width:', petalWidth);

        // 2. 비어 있는 입력값이 있는지 유효성 검사
        if (!sepalLength || !sepalWidth || !petalLength || !petalWidth) {
            alert('모든 입력 값을 입력해주세요!');
            return;
        }

        var request_data = {
            "sepal_length": sepalLength,
            "sepal_width": sepalWidth,
            "petal_length": petalLength,
            "petal_width": petalWidth
        }

        // 3. Flask 예측 API(/api/ai/predict-iris)로 데이터 전송 (AJAX)
        $.ajax({
            url: '/api/ai/predict-iris', // 상대 경로를 사용하면 CORS 에러가 발생하지 않습니다.
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(request_data), // JSON 문자열로 변환하여 전송해야 415 에러가 나지 않습니다.
            success: function (response) {
                if (response.success && response.class_name) {
                    var species = response.class_name.toLowerCase();

                    // 예측 결과 및 입력했던 4개 값을 함께 알림창으로 보여줍니다.
                    // alert('예측 결과 품종: ' + response.class_name +
                    //     '\n\n[입력한 정보]' +
                    //     '\n꽃받침 길이: ' + sepalLength + 'cm' +
                    //     '\n꽃받침 너비: ' + sepalWidth + 'cm' +
                    //     '\n꽃잎 길이: ' + petalLength + 'cm' +
                    //     '\n꽃잎 너비: ' + petalWidth + 'cm');

                    // 한글 표시와 영문 표시 조합
                    var displayName = response.class_name;
                    if (species === 'setosa') displayName = 'Setosa (세토사)';
                    else if (species === 'versicolor') displayName = 'Versicolor (버시컬러)';
                    else if (species === 'virginica') displayName = 'Virginica (버지니카)';

                    // 결과 카드 데이터 설정 및 품종별 테마 클래스 추가
                    $('#result-species-name').text(displayName);
                    $('#result-box').addClass(species);

                    var details = '꽃받침: ' + sepalLength + 'cm × ' + sepalWidth + 'cm' +
                        '\n꽃잎: ' + petalLength + 'cm × ' + petalWidth + 'cm';
                    $('#result-input-details').text(details);

                    // 결과창 표시
                    $('#prediction-result').fadeIn();
                } else {
                    alert('예측 실패: ' + (response.message || '알 수 없는 오류'));
                }
            },
            error: function (xhr, status, error) {
                console.error(error);
                alert('서버 요청 중 오류가 발생했습니다.');
            }
        });
    });
});
//     const $form = $('#iris-predict-form');
//     const $btn = $('#btn-predict');
//     const $spinner = $btn.find('.spinner');
//     const $btnText = $btn.find('.btn-text');
//     const $resultCard = $('#result-card');
//     const $resultSpecies = $('#result-species');
//     const $resultDesc = $('#result-description');
//     const $errorMsg = $('#error-msg');

//     // Species details for better user experience
//     const speciesInfo = {
//         'setosa': {
//             name: 'Iris Setosa (세토사)',
//             desc: '꽃잎(Petal)과 꽃받침(Sepal)이 상대적으로 짧고 둥근 형태를 띱니다. 주로 습하고 서늘한 기후에서 자생하며, 세 품종 중 구분이 가장 뚜렷합니다.'
//         },
//         'versicolor': {
//             name: 'Iris Versicolor (버시컬러)',
//             desc: '푸른빛과 보랏빛이 어우러진 중간 크기의 품종입니다. 세토사보다 꽃받침과 꽃잎이 더 길며, 여러 가지 색상이 섞여 있어 "변색 붓꽃"이라고도 불립니다.'
//         },
//         'virginica': {
//             name: 'Iris Virginica (버지니카)',
//             desc: '꽃받침과 꽃잎이 세 품종 중 가장 크고 화려합니다. 보랏빛이 강하며, 크기와 비율 면에서 버시컬러와 유사해 세밀한 구분이 필요한 품종입니다.'
//         }
//     };

//     $form.on('submit', function (e) {
//         e.preventDefault();

//         // Hide previous outputs
//         $errorMsg.hide().text('');
//         $resultCard.removeClass('show setosa versicolor virginica').hide();

//         // Get values
//         const sepalLength = parseFloat($('#sepal_length').val());
//         const sepalWidth = parseFloat($('#sepal_width').val());
//         const petalLength = parseFloat($('#petal_length').val());
//         const petalWidth = parseFloat($('#petal_width').val());

//         // Simple validation
//         if (isNaN(sepalLength) || isNaN(sepalWidth) || isNaN(petalLength) || isNaN(petalWidth)) {
//             $errorMsg.text('모든 필드에 올바른 숫자를 입력해 주세요.').fadeIn();
//             return;
//         }

//         // Show loading state
//         $btn.prop('disabled', true);
//         $spinner.show();
//         $btnText.text('분석 중...');

//         // Send AJAX request
//         $.ajax({
//             url: '/api/ai/predict-iris',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 sepal_length: sepalLength,
//                 sepal_width: sepalWidth,
//                 petal_length: petalLength,
//                 petal_width: petalWidth
//             }),
//             success: function (response) {
//                 if (response.success && response.class_name) {
//                     const species = response.class_name.toLowerCase();
//                     const info = speciesInfo[species] || { name: response.class_name, desc: '알 수 없는 품종입니다.' };

//                     // Display result with theme styling
//                     $resultSpecies.text(info.name);
//                     $resultDesc.text(info.desc);

//                     $resultCard.show().addClass(species);
//                     setTimeout(function () {
//                         $resultCard.addClass('show');
//                     }, 50);
//                 } else {
//                     $errorMsg.text(response.message || '예측 실패: 알 수 없는 오류가 발생했습니다.').fadeIn();
//                 }
//             },
//             error: function (xhr, status, error) {
//                 console.error('API Error:', error);
//                 $errorMsg.text('서버와 통신하는 중 문제가 발생했습니다. 입력값을 확인해 주세요.').fadeIn();
//             },
//             complete: function () {
//                 // Restore button state
//                 $btn.prop('disabled', false);
//                 $spinner.hide();
//                 $btnText.text('분석하기');
//             }
//         });
//     });
// });
