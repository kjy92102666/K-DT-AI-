from flask import Blueprint, jsonify, request
import db # 루트 경로의 db.py를 임포트

payment_bp = Blueprint("payment_route",__name__,url_prefix="/api/payment")

# 회원 포인트로 물건을 몇개 사겠다. 
#1.user,item 조회( idx로 조회)) / count
#2.user의 point >= price*count. 잔액 체크.
#3.count >= stock. 재고 체크.

# -> 결제진행. 1)user의 point를 차감(price*count만큼). 2)item의 stock 차감 (Count만큼). 3) payment 추가(insert)

#user_idx로 결제한 내역 조회
@payment_bp.route('/get-payment-history/<user_idx>', methods=['GET'])
def get_payment_by_user(user_idx):
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT * FROM payment AS p
            INNER JOIN user AS u
            ON p.user_idx = u.idx
            INNER JOIN item AS i
            ON p.item_idx = i.idx
            WHERE u.idx = %s""",(user_idx,))
            payments = cursor.fetchall()
            return jsonify({'data': payments, 'success': True, 'message': '결제내역조회 성공'})
    except Exception as e:
        return jsonify({
            'data': [],
            'success': False,
            'message': '결제내역조회 실패, 내부 서버에러',
            'error': str(e)
        })
    finally:
        db.close_db()


# 1.결제 로직
@payment_bp.route('/buy-item', methods=['POST'])
def buy_item():
    conn = None
    try:
        data = request.get_json()
        user_idx = data.get('user_idx') #구매자 인덱스
        item_idx = data.get('item_idx') #상품 인덱스
        count = data.get('count')       #구매 수량

        #print(f"{'user_idx':str(user_idx), 'item_idx':str(item_idx),'count':str(count)}") 여기서 오류가 나고있다.
        #필수 입력항목 체크
        if not user_idx or not item_idx or not count:
            return jsonify({
                'data': None,
                'success': False,
                'message': '필수 입력 항목을 확인해주세요'
            })
        
        #conn과 cursor 설정.
        conn = db.get_db()

        
        with conn.cursor() as cursor:
            #1)user,item 조회( idx로 조회)) / count
            cursor.execute("SELECT * FROM user WHERE idx = %s", (user_idx,))
            user = cursor.fetchone()
            if not user:
                return jsonify({'data':None,'success':False,'message':'회원이 존재하지 않습니다'})

            cursor.execute("SELECT * FROM item WHERE idx = %s", (item_idx,))
            item = cursor.fetchone()
            if not item:
                return jsonify({'data':None,'success':False,'message':'상품이 존재하지 않습니다'})
        
            if not user or not item:
                return jsonify({
                    'data': None,
                    'success': False,
                    'message': '회원 또는 상품이 존재하지 않습니다'
                })
            
        #가격 계산
            total_price = item['price'] * count

        #user의 잔액이 더 적으면 오류 반환.
            if user['point'] < total_price:
                return jsonify({'data':None,'success':False,'message':'잔액이 부족합니다'})
            
        #재고 비교
            if item['stock'] < count:
                return jsonify({'data':None,'success':False,'message':'재고가 부족합니다'})
            
        #결제진행. 1)user의 point를 차감(price*count만큼). 2)item의 stock 차감 (Count만큼). 3) payment 추가(insert)
            cursor.execute("UPDATE user SET point = point - %s WHERE idx = %s", (total_price, user_idx))
            cursor.execute("UPDATE item SET stock = stock - %s WHERE idx = %s", (count, item_idx))
            cursor.execute("""
            INSERT INTO payment 
            (user_idx, item_idx, count, total_price, created_at) 
            VALUES (%s, %s, %s, %s, now())""", (user_idx, item_idx, count, total_price))
            conn.commit()
            return jsonify({'data':None, 'success':True, 'message':'결제가 완료되었습니다'})
    
    except Exception as e:
        conn.rollback()     #pymysql의 트랜잭션기능. 추가/수정/삭제 중에 2가지 이상 들어가면 적용시켜줘야한다.
        return jsonify({
            'data': [],
            'success': False,
            'message': '결제 실패, 내부 서버에러',
            'error': str(e)
        })
    finally:
        db.close_db()
        

#>> 완벽하게 하는방법은 없다. 하지만 실패했을때 되돌리는 방법으로 처리한다. transaction.
#conn.rollback()     #pymysql의 트랜잭션기능. 추가/수정/삭제 중에 2가지 이상 들어가면 적용시켜줘야한다.
# 2.이 회원이 결제한 내역 조회

