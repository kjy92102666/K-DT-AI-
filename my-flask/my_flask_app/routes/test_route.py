from flask import Blueprint, jsonify, request,render_template

test_bp = Blueprint("test_route",__name__,url_prefix="/api/view")

# URL 경로(Route) 설정 127.0.0.1:5000'/'이 슬래쉬임. 요청경로
# @app.route('/test',methods=['GET']) #post는 당연히 405
# def hello_world():
#     return 'Hello, flask1'

@test_bp.route('/test2',methods=['GET'])
def hello_world2():
    return 'Hello, flask2'

# 스크립트가 직접 실행될 때 서버 구동
if __name__ == '__main__':
    test_bp.run(debug=True)


@test_bp.route('/test22',methods=['GET'])
def hello_world22():
    return 'Hello, flask22'

@test_bp.route('/get_items',methods=['GET'])
def get_items():
    item_name=request.args.get('item_name')
    item_price=request.args.get('item_price')
    print(item_name)
    print(item_price)

    return '아이템 조회 성공'