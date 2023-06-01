from requests import post
import flask
from flask_cors import CORS

import db
from configs import BOT_TOKEN


app = flask.Flask(__name__)
cors = CORS(app)


@app.post('/api/mosgortrans/reviews')
def add_review():
    review = flask.request.json

    # Verify that all required fields are present
    if review.get('telegram_id') is None or review.get('route_number') is None or review.get('rating') is None:
        return "There not enough required fields", 400
    
    # Checking the availability of an innovation id if there is an assessment of it
    if review.get('innovation') is not None and review.get('innovation_id') is None:
        return "Innovation id is required if you send an innovation", 400
    
    # Cheking matching of innovation for presented route
    innovation = db.get_innovation(review.get('route_number'))
    if review.get('innovation_id') is not None and (innovation is None or review.get('innovation_id') != innovation.get('id')):
        return "Innovation id does not match route number", 400

    # If previous checks are successful, adding reviews
    insert_res = db.add_review(review.get('telegram_id'), review.get('route_number'), review.get('rating'), review.get('clearness'),
                               review.get('smoothness'), review.get('conductors_work'), review.get('occupancy'),
                               review.get('innovation_id'), review.get('innovation'), review.get('text_review'))
    if insert_res == 0:
        # If review was successfully added and user haven't send review recently, add points to they
        db.add_points(review.get('telegram_id'), 100)
        text = "<u>Большое спасибо за отзыв!</u> 🎉\n\nВам начислено 100 баллов. 👏\n\nДля просмотра баллов выберите опцию «Мой профиль»."+\
            "\nДля просмотра рейтинга, выберите опцию «Топ пользователей»."
        return_ = 'OK'
    elif insert_res == 1:
        return_ = 'User already did review last 10m'
        text = 'Отзыв можно оставлять не чаще раза в 10 минут.'
    else:
        return "Fields types error, read documentation", 400
    
    post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={'text': text, 'chat_id': review.get('telegram_id'), 'parse_mode': 'html'})
    return return_, 200

@app.get('/api/mosgortrans/innovation')
def get_innovation():
    return flask.jsonify(db.get_innovation(flask.request.args.get('route_number')))
