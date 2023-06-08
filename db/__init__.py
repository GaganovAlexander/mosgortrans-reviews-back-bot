import psycopg2.extras

from configs import DB_USER, DB_PASSWORD, DB_NAME


conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                        host='127.0.0.1', port='5432')
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


import db.users as users
import db.innovations as innovations
import db.reviews as reviews
