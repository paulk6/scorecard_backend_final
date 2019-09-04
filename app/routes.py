from app import app, db
from flask import redirect, url_for, request, jsonify
import json
from flask_login import current_user, login_user
from app.models import Course, User, PlayerRound, Guest, Course, Club
import time
import jwt

@app.route('/api/retrieve/course', methods=['GET'])
def retrieveCourse():

    # grab the course id from headers passed in

    # query the database for that specific course


    # you'll get back a course object, you'll need to parse through the object and put the data into a dictionary so it can be turned into JSON


    # return a jsonified response, otherwise the frontend cannot render the information

    data = {}

    courses = Course.query.all()
    for course in courses:
        course_info = {}
        course_info['name'] = course.name
        course_info['state'] = course.state
        course_info['city'] = course.city
        data[course.name] = course_info

    return jsonify({ 'info': data })

@app.route('/api/retrieve/user', methods=['GET'])
def retrieveUser():
    token = request.headers.get('token')

    # get user id or none
    user = User.verify_token(token)
    print('user:')
    print(user)

    if not user:
        return jsonify({ 'message': 'Error #004: Invalid user' })

    data = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'nickname': user.nickname,
        'phone_number': user.phone_number,
        'handicap': user.handicap
    }

    return jsonify({ 'info': data })

@app.route('/api/retrieve/rounds', methods=['GET'])
def retrieveRounds():
    token = request.headers.get('token')

    # get user id or none
    user = User.verify_token(token)
    user_name = user.first_name

    rounds = PlayerRound.query.filter_by(user_id=user.user_id).all()

    #####################
    scorecard_id_list = []
    # get list of the scorecard id for each round the user has played in
    for round in rounds:
        scorecard_id_list.append(round.scorecard_id)

    all_players_round_list = []

    for id in scorecard_id_list:
        other_player_rounds = PlayerRound.query.filter_by(scorecard_id=id).all()
        all_players_round_list.append(other_player_rounds)

    print('**********************')
    print(all_players_round_list)
    print('**********************')


    #####################

    data = {}

    for round_list in all_players_round_list:
        data[round_list[0].scorecard_id] = {}
        for round in round_list:
            data[round.scorecard_id][round.user_id] = {}





    for round_list in all_players_round_list:
        for round in round_list:
            user_round = PlayerRound.query.filter_by(user_id=round.user_id).first()
            user_id = user_round.user_id
            user = User.query.filter_by(user_id=user_id).first()
            user_name = user.first_name
            data[round.scorecard_id][round.user_id]['first_name'] = user_name
            data[round.scorecard_id][round.user_id]['hole_1_score'] = round.hole_1_score
            data[round.scorecard_id][round.user_id]['hole_2_score'] = round.hole_2_score
            data[round.scorecard_id][round.user_id]['hole_3_score'] = round.hole_3_score
            data[round.scorecard_id][round.user_id]['hole_4_score'] = round.hole_4_score
            data[round.scorecard_id][round.user_id]['hole_5_score'] = round.hole_5_score
            data[round.scorecard_id][round.user_id]['hole_6_score'] = round.hole_6_score
            data[round.scorecard_id][round.user_id]['hole_7_score'] = round.hole_7_score
            data[round.scorecard_id][round.user_id]['hole_8_score'] = round.hole_8_score
            data[round.scorecard_id][round.user_id]['hole_9_score'] = round.hole_9_score
            data[round.scorecard_id][round.user_id]['total_score'] = round.total_score
    print(data)


    # for round in rounds :
    #     data[round.round_id] = {}
    #     print(data)

    # for round in rounds:
    #     data[round.round_id]['first_name'] = user_name
    #     data[round.round_id]['hole_1_score'] = round.hole_1_score
    #     data[round.round_id]['hole_2_score'] = round.hole_2_score
    #     data[round.round_id]['hole_3_score'] = round.hole_3_score
    #     data[round.round_id]['hole_4_score'] = round.hole_4_score
    #     data[round.round_id]['hole_5_score'] = round.hole_5_score
    #     data[round.round_id]['hole_6_score'] = round.hole_6_score
    #     data[round.round_id]['hole_7_score'] = round.hole_7_score
    #     data[round.round_id]['hole_8_score'] = round.hole_8_score
    #     data[round.round_id]['hole_9_score'] = round.hole_9_score
    #     data[round.round_id]['total_score'] = round.total_score
    #     print(data)

    return jsonify({ 'info': data })

@app.route('/api/retrieve/other_user', methods=['GET'])
def retrieveOtherUser():

    # get user id or none
    email = request.headers.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({ 'message': 'Error #004: Invalid user' })

    data = {
        'email': user.email,
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'nickname': user.nickname,
        'phone_number': user.phone_number,
        'handicap': user.handicap
    }

    return jsonify({ 'info': data })

@app.route('/api/register', methods=['GET', 'POST'])
def register():
    try:
        token = request.headers.get('token')

        print(token)

        # decode the token back to a dictionary
        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithm=['HS256']
        )

        print(data)

        # create the user and save
        user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'], phone_number=data['phone_number'], nickname=data['nickname'], handicap=data['handicap'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        return jsonify({ 'message': 'success' })
    except:
        return jsonify({ 'message': 'Error #001: User not created' })

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    try:
        token = request.headers.get('token')

        # decode the token back to a dictionary
        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithm=['HS256']
        )

        # query db to get user and check pass
        user = User.query.filter_by(email=data['email']).first()

        # if user doesn't exist or password incorrect, send fail msg
        if user is None or not user.check_password(data['password']):
            return jsonify({ 'message': 'Error #002: Invalid credentials' })

        # create a token and return it
        return jsonify({ 'message': 'success', 'token': user.get_token(), 'name': user.first_name })
    except:
        return jsonify({ 'message': 'Error #003: Failure to login' })

@app.route('/api/save/course', methods=['GET', 'POST'])
def saveCourse():
    try:
        token = request.headers.get('token')

        # decode the token back to a dictionary
        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithm=['HS256']
        )

        course = Course(name=data['name'], city=data['city'], state=data['state'])
        db.session.add(course)
        db.session.commit()
        return jsonify({ 'message' : 'success'})
    except:
        return jsonify({ 'message' : 'This course is already saved.'})


@app.route('/api/save/scorecard', methods=['GET', 'POST'])
def saveCard():
# try:
    # send over an array of each player in the round, loop through each player and commit them to the db
    players = request.headers.get('players')
    players = json.loads(players)
    course_info = request.headers.get('course_info')
    course_info = json.loads(course_info)

    course = Course.query.filter_by(name=course_info[0], city=course_info[1], state=course_info[2]).first()


    # query db for last scorecard entry
    last_entry = PlayerRound.query.all()[-1]

    scorecard_id = last_entry.scorecard_id + 1


    for player in players:
        playerRound = PlayerRound(hole_1_score=player['front_scores'][0], hole_2_score=player['front_scores'][1], hole_3_score=player['front_scores'][2], hole_4_score=player['front_scores'][3], hole_5_score=player['front_scores'][4], hole_6_score=player['front_scores'][5], hole_7_score=player['front_scores'][6], hole_8_score=player['front_scores'][7], hole_9_score=player['front_scores'][8],
        total_score=player['total'],
        scorecard_id=scorecard_id,
        user_id=player['user_id'],
        course_id=course.course_id)
        db.session.add(playerRound)
        db.session.commit()
    return jsonify({ 'message' : 'success'})
# except:
    return jsonify({ 'message' : 'The scorecard could not be saved.'})
