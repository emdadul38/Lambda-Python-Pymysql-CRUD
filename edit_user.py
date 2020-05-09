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
    # TODO implement
    try:
        print(event)
        column = ""
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print(event['body'])

        if event['body'].get("firstName") != None:
            column += " firstName = '"+ event['body']["firstName"] +"', "

        if event['body'].get("lastName") != None:
            column += " lastName = '"+ event['body']["lastName"] +"', "

        if event['body'].get("gender") != None:
            column += " gender = '"+ event['body']["gender"] +"', "

        if event['body'].get("birthday") != None:
            column += " birthday = '"+ event['body']["birthday"] +"', "

        if event['body'].get("email") != None:
            column += " email = '"+ event['body']["email"] +"', "

        if event['body'].get("phone") != None:
            column += " phone = '"+ event['body']["phone"] +"', "

        if event['body'].get("shippingAddress_id") != None:
            shippingAddress = event['body']["shippingAddress"]
            shippingAddress_id = str(event['body']["shippingAddress_id"])

            # call update address function
            updateAddress(shippingAddress, shippingAddress_id)

        if event['body'].get("billingAddress_id") != None:
            billingAddress =  event['body']["billingAddress"]
            billingAddress_id = str(event['body']["billingAddress_id"])

            # call update address function
            updateAddress(billingAddress, billingAddress_id)

        if column:
            column = column[:-2]

            updateStatement = "UPDATE user set "+ column +" where id=" + event["id"]

            # Execute the SQL UPDATE statement
            cursor.execute(updateStatement)
            conn.commit()

        # Type base update
        type = ""
        if event['body'].get("type") != None:
            type = event['body']["type"]

        if type == "practitioner":
            column_prac = ""
            if event['body'].get("email") != None:
                column_prac += " email = '"+ event['body']["email"] +"', "

            if event['body'].get("phone") != None:
                column_prac += " phone = '"+ event['body']["phone"] +"', "

            column_prac = column_prac[:-2]
            pracStatement = "UPDATE practitioner set "+ column_prac +" where user=" + event["id"]

            cursor.execute(pracStatement)
            conn.commit()

        if type == "patient":
            column_patient = ""
            if event['body'].get("practitioner") != None:
                column_patient += " practitioner = '"+ event['body']["practitioner"] +"', "

            if event['body'].get("height") != None:
                column_patient += " height = "+ str(event['body']["height"]) +", "

            if event['body'].get("weight") != None:
                column_patient += " weight = "+ str(event['body']["weight"]) +", "

            column_patient = column_patient[:-2]
            patientStatement = "UPDATE patient set "+ column_patient +" where user=" + event["id"]

            cursor.execute(patientStatement)
            conn.commit()

        # records = cursor.fetchall()
        return {
            'statusCode': 200,
            'body': "Ok"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def updateAddress(address, id):

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    updateStatement = "UPDATE address set street1 = '"+ address["street1"] + "', street2 = '"+ address["street2"] + "', city= '"+ address["city"] +"', zip= '"+ str(address["zip"]) +"', state = '" + address["state"] + "', country = '" + address["country"] +"' where id=" + id

    print(updateStatement)
    cursor.execute(updateStatement)
    conn.commit()
