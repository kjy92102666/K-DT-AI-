from flask import Blueprint, jsonify, request
import db # 루트 경로의 db.py를 임포트

user_bp = Blueprint("user_route",__name__,url_prefix="/api/user")
# url_prefix="/api/users" -> /api/users/login 으로 접속해야 한다.


#회원가입 post방식. api/user/create
@user_bp.route('/create',methods=['POST'])
def create():
    try:
        # 데이터 추출 (JSON -> Form -> Query Parameters 순으로 검색)
        data = request.get_json(silent=True) or {}
        id = data.get('id') or request.form.get('id') or request.args.get('id')
        pw = data.get('pw') or request.form.get('pw') or request.args.get('pw')
        nick = data.get('nick') or request.form.get('nick') or request.args.get('nick')
        address = data.get('address') or request.form.get('address') or request.args.get('address')
        point = data.get('point') or request.form.get('point') or request.args.get('point')

        # # 필수값 유효성 체크. 테이블에서 유니크키 설정도 하고 중복체크도 해서 처리하는게 좋다. 
        # #ID중복체크
        # if not id or not id.strip():
        #     return jsonify({'success': False, 'message': '아이디를 입력해주세요.', 'data': None})
        # # if not pw or not pw.strip():
        # #     return jsonify({'success': False, 'message': '비밀번호를 입력해주세요.', 'data': None})
        # #Nick중복체크
        # if not nick or not nick.strip():
        #     return jsonify({'success': False, 'message': '닉네임을 입력해주세요.', 'data': None})

        # 위에 유효성체크 간단하게 프론트엔드에서 잘 처리해서 넘겨주면 좋지만 이렇게 백단에서 처리해주는게 좋다.
        if not id or not nick or not address or not point.strip():
            return jsonify({'success': False, 'message': '필수 입력값을 입력해주세요.', 'data': None})

        # point 값 기본값 처리 및 타입 캐스팅
        if point is not None:
            try:
                point = int(point)
            except ValueError:
                point = 0
        else:
            point = 0

        conn = db.get_db()
        with conn.cursor() as cursor:
            # 2. 아이디 중복 체크
            cursor.execute("SELECT idx FROM user WHERE id = %s", (id,))
            exist_user = cursor.fetchone()
            if exist_user:
                return jsonify({
                    'success': False, 
                    'message': '이미 존재하는 아이디입니다.', 
                    'data': None
                })

            # 3. 회원 가입 DB 삽입
            cursor.execute("""
            INSERT INTO user (id, pw, nick, address, created_at, point) 
            VALUES 
            (%s, %s, %s, %s, now(), %s)
            """, (id, pw, nick, address, point))
            conn.commit()
            
            # 방금 가입한 유저의 AUTO_INCREMENT idx 가져오기
            inserted_idx = cursor.lastrowid
            
            return jsonify({
                'success': True, 
                'message': '회원가입 성공', 
                'data': {
                    'idx': inserted_idx,
                    'id': id,
                    'nick': nick
                }
            })

    except Exception as e:
        print(f"[디버그] 회원가입 에러: {e}")
        return jsonify({
            'success': False,
            'message': '회원가입 실패. 내부 서버에러 발생', 
            'error': str(e),
            'data': None
            })
    finally:
        db.close_db()




#/api/user/login?id=jmjm1111&pw=1234 ->POST방식
@user_bp.route('/login',methods=['POST'])
def login():
    try:
        # JSON Body, Form, Query Parameter 순서대로 id와 pw를 찾습니다.
        data = request.get_json(silent=True) or {}
        
        id = data.get('id') or request.form.get('id') or request.args.get('id')
        pw = data.get('pw') or request.form.get('pw') or request.args.get('pw')

        print(f"[디버그] 요청 Method: {request.method}")
        print(f"[디버그] Content-Type: {request.content_type}")
        print(f"[디버그] 전달받은 id: {repr(id)}, pw: {repr(pw)}")

        conn = db.get_db()
        
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE id = %s and pw=%s', (id,pw))
            user = cursor.fetchone() 
            
            print(f"[디버그] DB 조회 결과: {user}")

            # DB 조회 결과가 존재하는지 확인
            if user:
                return jsonify({
                    'data':{'success':True, 'message':'로그인 성공', 'user':user}
                    })
            else:
                return jsonify({
                    'data':{'success':False, 'message':'로그인 실패: 아이디 또는 비밀번호가 일치하지 않습니다.', 'user':None}
                    })
    except Exception as e:
        print(f"[디버그] 로그인 에러: {e}")
        return jsonify({
            'data': [],
            'success':False,
            'message':'회원조회 실패. 내부 서버에러 발생', 
            'error':':'+str(e)
            })
    finally:
        db.close_db()
        




#/api/user/get-user-by-id?id=jmjm1111 ->get방식
@user_bp.route('/get-user-by-id',methods=['GET'])
def get_user_by_id():
    try:
        id=request.args.get('id')
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE id = %s', (id,))
            user = cursor.fetchone() 
            return jsonify({
                'data':{'success':True, 'message':'회원조회 성공', 'user':user}
                })
    except Exception as e:
        return jsonify({
            'data': [],
            'success':False,
            'message':'회원조회 실패. 내부 서버에러 발생', 
            'error':':'+str(e)
            })
    finally:
        db.close_db()


@user_bp.route('/<idx>',methods=['GET'])
def get_user_by_idx(idx):
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE idx = %s', (idx,))
            user = cursor.fetchone()
            return jsonify({'data':{'success':True, 'message':'회원조회 성공', 'user':user}})
    except Exception as e:
        return jsonify({
            'data': [],
            'success':False,
            'message':'회원조회 실패. 내부 서버에러 발생', 
            'error':':'+str(e)
            })
    finally:
        db.close_db()
    

#회원조회 Back단
@user_bp.route('/all',methods=['GET'])
# get_user를 요청해라, 그리고String타입으로 uid를 요청한다. 띄워쓰기 금지!!.주로 파라미터1개만 사용
def get_all_user():

    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM user')
            users = cursor.fetchall()
            #db.close_db()  커넥션 닫기. 안하면 연결해놓고 그대로 둔다. 오라클이 막히거나 다른일이 생긴다.
            return jsonify({'data':{'success':True, 'message':'회원목록 조회 성공', 'users':users}})

    except Exception as e:
        #db.close_db() 얘도 생략가능. 어차피 finally에 있어서 
        return jsonify({
            'data': [],
            'success':False,
            'message':'회원목록 조회 실패. 내부 서버에러 발생', 
            'error':':'+str(e)
            })
    finally:
        db.close_db() # 여기서 닫아주므로써 두번 작성할 수고를 덜음.


    # 커넥션. 커서 연결시키는데 실제 커서에 집어넣는다. 
    # 연결 후 커서를 풀어줘야하는데 이 과정이 번거로우니 with로 처리한다.
    # 스프링에서는 이 과정을 커넥션풀이라 한다.
    

#예외처리



@user_bp.route('/test',methods=['GET'])
def user_test():
    return jsonify({'message':'라우터 테스트 성공!'})


