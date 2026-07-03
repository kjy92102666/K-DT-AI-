
from flask import Blueprint, jsonify, request,render_template

view_bp = Blueprint("view_route",__name__,url_prefix="/api/view")



@view_bp.route('/home',methods=['GET'])
def home():
    return render_template('index.html')

@view_bp.route('/page1',methods=['GET'])
def page1():
    return render_template('page1.html')

@view_bp.route('/class-id',methods=['GET'])
def class_id():
    return render_template('class-id.html')
    
@view_bp.route('/layout',methods=['GET'])
def layout():
    return render_template('layout.html')

@view_bp.route('/company',methods=['GET'])
def company():
    return render_template('company.html')
    
    
@view_bp.route('/front',methods=['GET'])
def front():
    return render_template('front.html')
    
    
@view_bp.route('/iris',methods=['GET'])
def iris():
    return render_template('iris.html')
    