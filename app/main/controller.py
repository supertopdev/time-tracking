from datetime import datetime, timedelta
from flask import jsonify, request, make_response, abort
from flask_login import login_required, current_user
from app import db
from app.main import main_bp
from app.models import Users, UsersInfo
from app.main.serializer import UsersInfoSchema
from app.util.manager_view import UserWeekInfo, ManagerView
import json

# Add Tracking time for week
@main_bp.route('/user/info', methods=['POST'])
# @login_required
def addUserInfo():
    """
    Add user time info for a week
    """
    # userId = current_user.id
    # if current_user.role == 1:
    #     abort(400, 'Manager cannot add work logs')
    data = json.loads(request.data).get('postdata')
    userId = data.get('user_id')
    date_str = data.get('date')
    if not date_str:
        abort(400, 'No date provided')

    info = data.get('info')
    if not info:
        abort(400, 'User data not provided')
    
    try:
        data['date'] = datetime.strptime(date_str, '%d-%m-%Y')
    except ValueError as e:
        abort(400, 'Incorrect date format provided')

    # data['user_id'] = userId
    # --- Check if already exists
    user_info = UsersInfo.query.filter_by(user_id=userId, date=data['date']).first()
    if user_info:
        for key in data:
            setattr(user_info, key, data[key])
        try:
            db.session.add(user_info)
            db.session.commit()
            response = {
                "status" : "User info updated"
            }
        except Exception as e:        
            abort(500, str(e))
        
    # --- Add new user info
    else:
        try:
            user_time = UsersInfo(**data)
            db.session.add(user_time)
            db.session.commit()
            response = {
                "status" : "User info added"
            }
        except Exception as e:
            abort(500, str(e))
    
    return make_response(jsonify(response), 200)

# Display Tracking time for week
@main_bp.route('/user/info/<int:userId>/<string:date>', methods=['GET'])
# @login_required
def getUserInfo(date, userId):
    """
    Get user time info for a week
    """
    # userId = current_user.id
    # if current_user.role == 1:
    #     abort(400, 'Manager has no work logs')

    # --- Check format of date
    try:
        date = datetime.strptime(date, '%d-%m-%Y').date()
    except ValueError as e:
        abort(400, 'Incorrect date format provided')
    
    user_info = UsersInfo.query.filter_by(user_id=userId, date=date).first()
    if not user_info:
        abort(400, "No info available")

    response = UsersInfoSchema().dump(user_info).data

    return make_response(jsonify(response), 200)

# Check the tracking time when current user is manager (viewId: 1, 2, 3)
@main_bp.route('/manager/<int:viewId>/<string:date>', methods=['GET'])
# @login_required
def getManagerView(viewId,date):
    """
    Get authorized views for Manager (View 1,2,3)
    """

    # if current_user.role != 1:
    #     abort(400, 'Not authorized')
    
    # --- Check format of date
    try:
        if validate(date):
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
        date = datetime.strptime(date, '%d-%m-%Y').date()
    except ValueError as e:
        abort(400, 'Incorrect date format provided')

    users_info_data = UsersInfo.query.filter_by(date=date).all()
    users_info = UsersInfoSchema(many=True).dump(users_info_data).data

    if viewId == 3:
        response = users_info

    else:
        user_details = []
        for user_info in users_info:
            user_details.append(UserWeekInfo(user_info))
        
        manager_view = ManagerView(user_details)

        if viewId == 1:
            response = manager_view.getChargeCodeTotal()
        elif viewId == 2:
            response = manager_view.getTotalHours()
        else:
            abort(400, "Invalid manager view ID")
            
    return make_response(jsonify(response), 200)

@main_bp.route('/manager/week_ranges', methods=['GET'])
# @login_required
def getWeekDates():
    """
    Get week ranges from DB.
    Response will be of format :

    [
        {
            "end_date": "25-06-2019",
            "start_date": "19-06-2019"
        },
        {
            "end_date": "02-07-2019",
            "start_date": "26-06-2019"
        }
    ]
    """
    unique_dates_object = UsersInfo.query.distinct(UsersInfo.date).order_by(UsersInfo.date.asc()).all()

    response = []
    for idx, unique_date in enumerate(unique_dates_object):
        response.append({
            "value" : idx + 1,
            "start_date" : unique_date.date.strftime("%Y-%m-%d"),
            "end_date" : (unique_date.date + timedelta(days=6)).strftime("%Y-%m-%d")
        })

    return make_response(jsonify(response), 200)

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except:
        return False