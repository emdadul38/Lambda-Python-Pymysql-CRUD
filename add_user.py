import sys
import json
import pymysql
import rds_config
import logging

rds_host = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = rds_config.port

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def lambda_handler(event, context):
    # print(conn.open)
    shipping_address = event['shippingAddress']
    billing_address = event['billingAddress']

    # Add shipping Address and retrun address_id
    shipping_address_id = insertAddress(shipping_address)

    # Add Billing Address and retrun address_id
    billing_address_id = insertAddress(billing_address)

    sql = "INSERT INTO `user` (`firstName`, `lastName`,  `gender`, `birthday`,`email`, `phone`, `shippingAddress`, `billingAddress`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (event["firstName"], event["lastName"], event["gender"], event["birthday"], event["email"], event["phone"], shipping_address_id, billing_address_id)

    with conn.cursor() as cur:
        cur.execute(sql, val)
        conn.commit()
        user_id = cur.lastrowid

        if event["type"] == "practitioner":
            practitioner = "INSERT INTO `practitioner` (`user`, `facility`,  `unit`) VALUES(%s, %s, %s)"
            data = (user_id, event["facility"], event["unit"])

            cur.execute(practitioner, data)
            conn.commit()

        else:
            patient = "INSERT INTO `patient` (`user`,  `practitioner`, `height`,  `weight`) VALUES(%s, %s, %s, %s)"
            patient_data = (user_id, event["practitioner_id"], event["height"], event["weight"])
            cur.execute(patient, patient_data)
            conn.commit()

    return {
        'statusCode': 200,
        'body': json.dumps('Data has been inserted successfully')
    }

def insertAddress(address):

    with conn.cursor() as cur:

        sql = "INSERT INTO address (street1, street2, city, zip, state, country) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (address["street1"], address["street2"], address["city"], address["zip"], address["state"], address["country"])
        cur.execute(sql, val)
        conn.commit()

        if cur.lastrowid:
            return cur.lastrowid
        else:
            return False
