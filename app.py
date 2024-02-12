from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from models import db, Users

app = Flask(__name__)

# 세션, 쿠키 관리에 사용되는 비밀키
app.config['SECRET_KEY'] = 'cj0423'
# DB 접속 정보
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/cj0423'

# 수정 내역 추적 비활성화 => 성능향상
SQLALCHEMY_TRAK_MODIFICATIONS = False
# 생성되는 쿼리문을 확인 가능하도록 함
SQLALCHEMY_ECHO = True

#서로 다른 포트를 사용 가능하도록 해줌
CORS(app, supports_credentials=True)

db.init_app(app)

# 유효성 검사, JSON 직렬화 기능 초기화
ma=Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','password')

users_schema = UserSchema(many=True)
user_schema = UserSchema()

#app 시작 시 db 생성
with app.app_context():
    db.create_all()

#시작 페이지
@app.route('/')
def index():
    return "<p>Hello, World!</p>"

#전체 인원정보
@app.route('/users', methods=['GET'])
def listusers():
    all_users = Users.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)

#상세 인원정보
@app.route('/userdetails/<id>',methods=['GET'])
def userdetails(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)

#인원정보 생성
@app.route('/newuser',methods=['POST'])
def newuser():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    users = Users(name=name, email=email, password=password)

    db.session.add(users)
    db.session.commit()
    return user_schema.jsonify(users)

#인원정보 수정
@app.route('/userupdate/<id>', methods=['PUT'])
def userupdate(id):
    user = Users.query.get(id)

    name = request.json['name']
    email = request.json['email']

    user.name = name
    user.email = email
    
    db.session.commit()
    return user_schema.jsonify(user)

#인원정보 삭제
@app.route('/userdelete/<id>', methods=['DELETE'])
def userdelete(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__ == "__main__":
    app.run(debug=True)