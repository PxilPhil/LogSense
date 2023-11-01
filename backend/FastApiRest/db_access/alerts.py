from __future__ import annotations

import json
from datetime import datetime
from typing import List

import psycopg2.errorcodes

from psycopg2 import extras
import psycopg2

from exceptions.InvalidParametersException import InvalidParametersException
from db_access import conn_pool
from psycopg2 import extras

from db_access.data_helper import get_pc_state_df, update_disk_df
from db_access.helper import get_pcid_by_stateid
from exceptions.DataBaseExcepion import DataBaseException
from exceptions.DataBaseInsertExcepion import DataBaseInsertException
from model.alerts import CustomAlerts, CustomAlert, IngestCustomAlert, CustomAlertDBObject, CustomCondition


def ingestCustomAlerts(alerts: CustomAlerts):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        insert_query = """
            INSERT INTO anomaly (user_id, type, severity_level, message, condition)
            VALUES %s RETURNING id
        """
        alert_tuples = []
        for alert in alerts.custom_alert_list:
            conditions_json = json.dumps([condition.dict() for condition in alert.conditions])
            alert_tuples.append((alert.user_id, alert.type, alert.severity_level, alert.message, conditions_json))
        psycopg2.extras.execute_values(cursor, insert_query, alert_tuples)

        anomaly_id = cursor.fetchone()[0]

        conn.commit()
        return anomaly_id
    except Exception as e:
        print(str(e))
    finally:
        conn_pool.putconn(conn)

def getCustomAlerts(user_id: int) -> CustomAlerts:
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """SELECT 
                    id,
                    user_id,
                    type,
                    severity_level,
                    message,
                    condition::text 
                    FROM anomaly WHERE user_id = %s;"""
        cursor.execute(query, (user_id,))

        anomalies = cursor.fetchall()

        custom_alerts = CustomAlerts(
            custom_alert_list=[
                CustomAlert(
                    id=anomaly[0],
                    user_id=anomaly[1],
                    type=anomaly[2],
                    message=anomaly[4],
                    severity_level=anomaly[3],
                    conditions=json.loads(anomaly[5], object_hook=lambda d: CustomCondition(**d))
                )
                for anomaly in anomalies
            ]
        )

        return custom_alerts
    except Exception as e:
        print(str(e))
        # Handle exceptions as needed.
        raise e  # DataBaseException()
    finally:
        conn_pool.putconn(conn)


def deleteCustomAlerts(alert_id: int):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
            DELETE FROM anomaly WHERE id = %s
        """
        cursor.execute(query, (alert_id,))
        conn.commit()
        return True, "Delete successful!"
    except psycopg2.DatabaseError as e:
        if e.pgcode == "23503":
            return False, "The specified ID was not found."
        else:
            return False, "An error occurred:"+ e.__str__()

    finally:
        conn_pool.putconn(conn)