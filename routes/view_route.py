
from flask import Blueprint, jsonify, request,render_template

view_bp = Blueprint("view_route",__name__,url_prefix="/api/view")



@view_bp.route('/home',methods=['GET'])
def home():
    return render_template('index.html')

