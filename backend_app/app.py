import flask
from flask_cors import CORS

from requests import post

import db
from configs import BOT_TOKEN


app = flask.Flask(__name__)
cors = CORS(app)


@app.route('/api/mosgortrans/reviews', methods=['POST', 'GET'])
def add_review():
    if flask.request.method == 'POST':
        return_ = 'User already did review last 10m'
        text = 'Вы уже оставляли отзыв за последние 10 минут'

        review = flask.request.json

        if not (review.get('telegram_id') and review.get('route_number') and  review.get('rating')):
            return "There not enough required fields", 400
        if not (review.get('innovation') is None and review.get('innovation_id')):
            return "Innovation id is required if you send an innovation", 400
        innovation = db.get_innovation(review.get('route_number'))
        if review.get('innovation_id') and (not innovation or review.get('innovation_id') != innovation.get('id')):
            return "Innovation id does not match route number", 400
        
        if db.add_review(review.get('telegram_id'), review.get('route_number'), review.get('rating'), review.get('clearness'),
                         review.get('smoothness'), review.get('conductors_work'), review.get('occupancy'),
                         review.get('innovation_id'), review.get('innovation'), review.get('text_review')):
            db.add_points(review.get('telegram_id'), 100)
            text = 'Отзыв записан\n100 очков начислено'
            return_ = 'OK'

        post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
             json={'text': text, 'chat_id': review.get('telegram_id'), 'parse_mode': 'html'})

        return return_
    else:
        return flask.jsonify(db.get_reviews())

@app.get('/api/mosgortrans/innovation')
def get_innovation():
    return flask.jsonify(db.get_innovation(flask.request.args.get('route_number')))

if __name__ == '__main__':
    db.create_tables()
    app.run(host='127.0.0.1', port=8000, debug=False)
