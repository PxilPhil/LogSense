from db_access import cursor, conn


def add_pc(user_id, hardware_uuid, client_name):
    #TODO: check if user exsists

    query = "INSERT INTO PC (USER_ID, hardwareUUID, clientName) VALUES (%s, %s, %s) RETURNING ID;"
    params = (str(user_id), str(hardware_uuid), str(client_name))

    pc_id = -1
    try:
        cursor.execute(query, params)
        pc_id = cursor.fetchone()[0]
        print("Insertion successful. PC ID:", pc_id)
    except Exception as e:
        print("Error occurred:", str(e))

    conn.commit()

    return pc_id


def get_pcs():
    query = """
        SELECT u.Name AS username, u.EMail AS email, pc.hardwareUUID, pc.clientName, pc.manufacturer, pc.model
        FROM logSenseUser u
        JOIN PC pc ON u.ID = pc.USER_ID;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    pcs = []
    for row in rows:
        pc = {'user_name': row[0], 'email': row[1], 'hardware_uuid': row[2], 'client_name': row[3], 'manufacturer': row[4], 'model': row[5]}
        pcs.append(pc)
    return pcs


def get_pcs_by_userid(user_id):
    query = """
        SELECT pc.hardwareUUID, pc.clientName, pc.manufacturer, pc.model
        FROM PC pc
        WHERE pc.USER_ID = %s;

    """
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    pcs = []
    for row in rows:
        pc = {'hardware_uuid': row[0], 'client_name': row[1], 'manufacturer': row[2], 'model': row[3]}
        pcs.append(pc)
    return pcs
