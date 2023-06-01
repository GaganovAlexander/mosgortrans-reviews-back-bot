from datetime import datetime, timedelta

import psycopg2.extras
from psycopg2.errors import DatatypeMismatch

from configs import DB_USER, DB_PASSWORD, DB_NAME


conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASSWORD, host='127.0.0.1', port='5432')
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def create_tables():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS
    innovations (
        id BIGSERIAL PRIMARY KEY,
        route_number VARCHAR(15),
        name VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS users(
        telegram_id BIGINT PRIMARY KEY,
        nickname text,
        points BIGINT
    );
    CREATE TABLE IF NOT EXISTS
    reviews (
        telegram_id BIGINT NOT NULL,
        route_number VARCHAR(15) NOT NULL,
        rating SMALLINT NOT NULL,
        clearness BOOLEAN,
        smoothness BOOLEAN,
        conductors_work BOOLEAN,
        occupancy BOOLEAN,
        innovation_id BIGINT,
        innovation BOOLEAN,
        text_review TEXT,
        created_at TIMESTAMP NOT NULL,
        CONSTRAINT pk_reviews 
            PRIMARY KEY(telegram_id, created_at),
        CONSTRAINT fk_users
            FOREIGN KEY (telegram_id)
            REFERENCES users(telegram_id),
        CONSTRAINT fk_innovations
            FOREIGN KEY(innovation_id) 
            REFERENCES innovations(id)
    );
    ''')
    conn.commit()

def get_innovation(route_num: str):
    cur.execute('''SELECT id, name FROM innovations
                   WHERE route_number = %s
                   ORDER BY id DESC LIMIT 1''',
                (route_num,))
    innovation = cur.fetchone()
    return innovation

def add_review(telegram_id: int, route_num: str, rating: int, clearness: bool, smothness: bool,
               conductors_work: bool, occupancy: bool, innovation_id: int, innovation: bool, text_review: str) -> bool:
    try:
        cur.execute(
            'SELECT MAX(created_at) ca FROM reviews WHERE telegram_id = %s', (telegram_id,))
        last_review_time = cur.fetchone()['ca']
        if last_review_time is None or datetime.now() - last_review_time >= timedelta(minutes=10):
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
    return 1


def get_reviews(telegram_id: None | int = None):
    if telegram_id is None:
        cur.execute('SELECT * FROM reviews')
        reviews = cur.fetchall()
    else:
        cur.execute('SELECT * FROM reviews WHERE telegram_id = %s',
                    (telegram_id,))
        reviews = cur.fetchall()
    return reviews


def add_points(telegram_id: int, points: int):
    cur.execute('UPDATE users SET points = points + %s WHERE telegram_id = %s',
                (points, telegram_id))
    conn.commit()


def get_user(telegram_id: int):
    cur.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
    user = cur.fetchone()
    return user


def add_user(telegram_id: int, nickname: str):
    user = get_user(telegram_id)
    if user:
        return user['nickname']
    cur.execute('INSERT INTO users (telegram_id, nickname, points) VALUES (%s, %s, 0)',
                (telegram_id, nickname))
    conn.commit()


def change_nickname(telegram_id: int, new_nickname: str):
    cur.execute('UPDATE users SET nickname = %s WHERE telegram_id = %s',
                (new_nickname, telegram_id))
    conn.commit()


def get_rating(telegram_id: int):
    cur.execute('''
        SELECT nickname, points, ROW_NUMBER() OVER(ORDER BY POINTS DESC) pos
        FROM users LIMIT 10
    ''')
    rating = cur.fetchall()
    cur.execute(('''
        SELECT nickname, points, pos FROM (SELECT *, ROW_NUMBER() OVER(ORDER BY POINTS DESC) pos
        FROM users) t
        WHERE telegram_id = %s
    '''), (telegram_id,))
    rating.append(cur.fetchone())
    return rating
