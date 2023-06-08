from psycopg2.extras import RealDictRow

from db import cur, conn


def create(telegram_id: int, nickname: str) -> str | None:
    '''Returns user nickname if they exist, otherwise returns None and add user to the database'''

    user = get(telegram_id)
    if user:
        return user['nickname']
    cur.execute('INSERT INTO users (telegram_id, nickname, points) VALUES (%s, %s, 0)',
                (telegram_id, nickname))
    conn.commit()

def get(telegram_id: int) -> RealDictRow:
    '''
    Returns all users fields by its telegram id. Fields are:
    telegram_id: int, nickname: str, points: int
    '''

    cur.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
    user = cur.fetchone()
    return user

def change_nickname(telegram_id: int, new_nickname: str):
    cur.execute('UPDATE users SET nickname = %s WHERE telegram_id = %s',
                (new_nickname, telegram_id))
    conn.commit()

def add_points(telegram_id: int, points: int):
    cur.execute('UPDATE users SET points = points + %s WHERE telegram_id = %s',
                (points, telegram_id))
    conn.commit()

def get_rating(telegram_id: int) -> list[RealDictRow]:
    '''
    Returns users rating by their points. 
    First 10 will be by order and last row will be requested user's position.
    Return fields are: nickname: str, points: int, user_position: int
    '''

    cur.execute('''
        SELECT nickname, points, ROW_NUMBER() OVER(ORDER BY POINTS DESC) pos
        FROM users LIMIT 10
    ''')
    rating = cur.fetchall()
    cur.execute(('''
        SELECT nickname, points, pos FROM 
        (SELECT *, ROW_NUMBER() OVER(ORDER BY POINTS DESC) pos
        FROM users) t
        WHERE telegram_id = %s
    '''), (telegram_id,))
    rating.append(cur.fetchone())
    return rating
