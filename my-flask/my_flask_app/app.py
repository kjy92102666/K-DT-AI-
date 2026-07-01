import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask import Flask,render_template
import json
from flask import make_response
from routes.view_route import view_bp
from routes.ai_route import ai_bp
from routes.user_route import user_bp
from routes.test_route import test_bp
from routes.item_route import item_bp
from routes.payment_route import payment_bp

#__init__.py 파일

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

#블루 프린트 등록
app.register_blueprint(ai_bp)
app.register_blueprint(view_bp)
app.register_blueprint(user_bp)
app.register_blueprint(test_bp)
app.register_blueprint(item_bp)
app.register_blueprint(payment_bp)

# 한글이 깨지지 않게 설정 
app.json.ensure_ascii = False

#데이터 받는방법 3가지. 화요일에 진행. 
#1. params 방식
#2. query String방식
#3. body 방식

'''
#1. params 방식 .../<value>
@app.route('/get_user/<string:uid>',methods=['GET'])
# get_user를 요청해라, 그리고String타입으로 uid를 요청한다. 띄워쓰기 금지!!.주로 파라미터1개만 사용
def get_user(uid):
    return '회원조회 성공'
'''


#2.query String 방식 .../<value>?key=value&key=value.
# request.args : 딕셔너리 처럼 생겼으며 키값만 가지고 오는 방식
# response

    #f'{item_names}' 출력문 이 함수가 리턴 되는지 확인.



# URL 경로(Route) 설정 127.0.0.1:5000'/'이 슬래쉬임. 요청경로
# @app.route('/test',methods=['GET']) #post는 당연히 405
# def hello_world():
#     return 'Hello, flask1'


# 스크립트가 직접 실행될 때 서버 구동
if __name__ == '__main__':
    app.run(debug=True)