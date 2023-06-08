from db import cur


def get(route_num: str):
    '''Returns latest innovation for a given route'''
    
    cur.execute('''SELECT id, name FROM innovations
                   WHERE route_number = %s
                   ORDER BY id DESC LIMIT 1''',
                (route_num,))
    innovation = cur.fetchone()
    return innovation
