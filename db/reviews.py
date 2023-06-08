from datetime import datetime, timedelta

from psycopg2.errors import DatatypeMismatch

from db import cur, conn


def add(telegram_id: int, route_num: str, rating: int, clearness: bool, smothness: bool, conductors_work: bool,
        occupancy: bool, innovation_id: int, innovation: bool, text_review: str):
    '''
    Adds a new review to the database. Returns status code:
    0 if successful, 1 if user already did review last 10m
    and -1 if there was type error due to the request error
    '''

    cur.execute(
        'SELECT MAX(created_at) ca FROM reviews WHERE telegram_id = %s', (telegram_id,))
    last_review_time = cur.fetchone()['ca']
    if last_review_time is not None and datetime.now() - last_review_time <= timedelta(minutes=10):
        return 1
    try:
        cur.execute(
            'INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (telegram_id, route_num, rating, clearness, smothness, conductors_work,
            occupancy, innovation_id, innovation, text_review, datetime.now())
        )
        conn.commit()
        return 0
    except DatatypeMismatch:
        conn.rollback()
        return -1
    
def get(telegram_id: None | int = None):
    '''Returns all reviews of user with given telegram id otherwise returns all reviews'''
    
    if telegram_id is None:
        cur.execute('SELECT * FROM reviews')
        reviews = cur.fetchall()
    else:
        cur.execute('SELECT * FROM reviews WHERE telegram_id = %s',
                    (telegram_id,))
        reviews = cur.fetchall()
    return reviews
