from requests import post

import flask
from flask_cors import CORS

import db
from configs import BOT_TOKEN


app = flask.Flask(__name__)
cors = CORS(app)


@app.route('/api/mosgortrans/reviews', methods=['POST', 'GET'])
def add_review():
    if flask.request.method == 'POST':
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
        
        # Checking validity of types
        if not(isinstance(review.get('telegram_id', int)) or
               isinstance(review.get('route_number', str)) or
               isinstance(review.get('rating', int)) or
               (isinstance(review.get('clearness'), bool) or review.get('clearness') is None) or
               (isinstance(review.get('smoothness'), bool) or review.get('smoothness') is None) or
               (isinstance(review.get('conductors_work'), bool) or review.get('conductors_work') is None) or
               (isinstance(review.get('occupancy'), bool) or review.get('occupancy') is None) or
               (isinstance(review.get('innovation_id'), int) or review.get('innovation_id') is None) or
               (isinstance(review.get('text_review'), str) or review.get('text_review') is None)):
            return "Fields types error, read documentation", 400

        # If previous checks are successful, adding reviews
        return_ = 'User already did review last 10m'
        text = 'Вы уже оставляли отзыв за последние 10 минут'
        if db.add_review(review.get('telegram_id'), review.get('route_number'), review.get('rating'), review.get('clearness'),
                         review.get('smoothness'), review.get('conductors_work'), review.get('occupancy'),
                         review.get('innovation_id'), review.get('innovation'), review.get('text_review')):
            # If review was successfully added and user haven't send review recently, add points to they
            db.add_points(review.get('telegram_id'), 100)
            text = 'Отзыв записан\n100 очков начислено'
            return_ = 'OK'

        post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
             json={'text': text, 'chat_id': review.get('telegram_id'), 'parse_mode': 'html'})

        return return_, 200
    else:
        return flask.jsonify(db.get_reviews())

@app.get('/api/mosgortrans/innovation')
def get_innovation():
    return flask.jsonify(db.get_innovation(flask.request.args.get('route_number')))
