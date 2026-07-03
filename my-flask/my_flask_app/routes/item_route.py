from flask import Blueprint, jsonify, request
import db # 루트 경로의 db.py를 임포트

item_bp = Blueprint("item_route",__name__,url_prefix="/api/item")
# user_route.py 참고해서 ai를 활용해서 만들어봐라. 
# 1.상품등록 POST 
# 2.상품전체조회 GET
# 3.상품명으로 조회 GET
# 4.상품삭제 DELETE
# 5.상품 정보변경 (name,maker,price 변경)PUT >> 단일 데이터 변경시 기존 데이터는 그대로 유지되도록.
#>>실무에서 어떻게 활용하는지 
# 1.상품등록 POST

# 상품등록
@item_bp.route('/create', methods=['POST'])
def create():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        maker = data.get('maker')
        stock = data.get('stock')

        if not name or price is None:
            return jsonify({
                'data': None,
                'success': False,
                'message': 'name, price 필수 입력 항목을 확인해주세요'
            })

        conn = db.get_db()
        with conn.cursor() as cursor:
            result = cursor.execute("""
            INSERT INTO item (name, price, created_at, maker, stock)
            VALUES
            (%s, %s, now(), %s, %s)
            """, (name, price, maker, stock if stock is not None else 0))
            print(result)
            conn.commit()
            return jsonify({'data': None, 'success': True, 'message': '상품등록 성공'})
    except Exception as e:
        return jsonify({
            'data': [],
            'success': False,
            'message': '상품등록 실패, 내부 서버에러',
            'error': str(e)
        })
    finally:
        db.close_db()


# idx로 상품조회
@item_bp.route('/get-item/<idx>', methods=['GET'])
def get_item_by_idx(idx):
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM item WHERE idx = %s", (idx,))
            item = cursor.fetchone()
            return jsonify({'data': item, 'success': True, 'message': '상품조회 성공'})
    except Exception as e:
        return jsonify({
            'data': [],
            'success': False,
            'message': '상품조회 실패, 내부 서버에러',
            'error': str(e)
        })
    finally:
        db.close_db()


# 전체 상품조회
@item_bp.route('/all', methods=['GET'])
def get_all_items():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM item")
            items = cursor.fetchall()
            return jsonify({'data': items, 'success': True, 'message': '상품조회 성공'})
    except Exception as e:
        return jsonify({
            'data': [],
            'success': False,
            'message': '상품조회 실패, 내부 서버에러',
            'error': str(e)
        })
    finally:
        db.close_db()


# 상품명으로 조회
@item_bp.route('/get-by-name', methods=['GET'])
def get_item_by_name():
    try:
        name = request.args.get('name')

        if not name:
            return jsonify({
                'data': None,
                'success': False,
                'message': 'name 필수 입력 항목을 확인해주세요'
            })

        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM item WHERE name = %s", (name,))
            items = cursor.fetchall()
            return jsonify({'data': items, 'success': True, 'message': '상품조회 성공'})
    except Exception as e:
        return jsonify({
            'data': [],
            'success': False,
            'message': '상품조회 실패, 내부 서버에러',
            'error': str(e)
        })
    finally:
        db.close_db()


# 상품삭제
@item_bp.route('/delete/<idx>', methods=['DELETE'])
def delete_item(idx):
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM item WHERE idx = %s", (idx,))
            item = cursor.fetchone()
            if not item:
                return jsonify({'data': None, 'success': False, 'message': '상품이 존재하지 않습니다'})

            cursor.execute("DELETE FROM item WHERE idx = %s", (idx,))
            conn.commit()
            return jsonify({'data': None, 'success': True, 'message': '상품삭제 성공'})
    except Exception as e:
        return jsonify({
            'data': [],
            'success': False,
            'message': '상품삭제 실패, 내부 서버에러',
            'error': str(e)
        })
    finally:
        db.close_db()


# 상품정보 업데이트
@item_bp.route('/update', methods=['POST'])
def update_item():
    try:
        data = request.get_json()
        idx = data.get('idx')
        name = data.get('name')
        price = data.get('price')
        maker = data.get('maker')
        stock = data.get('stock')

        if not idx:
            return jsonify({
                'data': None,
                'success': False,
                'message': 'idx 필수 입력 항목을 확인해주세요'
            })

        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM item WHERE idx = %s", (idx,))
            item = cursor.fetchone()
            if not item:
                return jsonify({'data': None, 'success': False, 'message': '상품이 존재하지 않습니다'})

            cursor.execute("""
            UPDATE item
            SET name = %s, price = %s, maker = %s, stock = %s
            WHERE idx = %s
            """, (
                name if name is not None else item['name'],
                price if price is not None else item['price'],
                maker if maker is not None else item['maker'],
                stock if stock is not None else item['stock'],
                idx
            ))
            # ★ 입력값을 넣지 않았을때 기존 값 그대로.
            conn.commit()
            return jsonify({'data': None, 'success': True, 'message': '상품정보 업데이트 성공'})
    except Exception as e:
        return jsonify({
            'data': [],
            'success': False,
            'message': '상품정보 업데이트 실패, 내부 서버에러',
            'error': str(e)
        })
    finally:
        db.close_db()
           