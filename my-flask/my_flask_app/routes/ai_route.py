from flask import Blueprint, jsonify, request
import joblib
import numpy as np



# 붓꽃 품종 이름 배열 (0: setosa, 1: versicolor, 2: virginica)
target_names = ['setosa', 'versicolor', 'virginica']
ai_bp = Blueprint("ai_route",__name__,url_prefix="/api/ai")

loaded_model = joblib.load("models/iris_model_v1.0.0_ac_1.0.pkl")

@ai_bp.route('/predict-iris',methods=['POST'])
def predict_iris():
    
    data = request.get_json()
    sepal_length = data.get('sepal_length')
    sepal_width = data.get('sepal_width')
    petal_length = data.get('petal_length')
    petal_width = data.get('petal_width')

    #9.임의의 값으로 예측
    new_data = np.array([[float(sepal_length), float(sepal_width), float(petal_length), float(petal_width)]])
    prediction = loaded_model.predict(new_data)
    class_nmuber = prediction[0]
    
    predicted_species = target_names[class_nmuber]
    
    return jsonify({
        "success": True,
        "message": "아이리스 예측 성공, data는 예측 결과를 담고 있습니다.",
        "class_name": predicted_species,
    })
    