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

records = []
def lambda_handler(event, context):
    # TODO implement

    try:

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT u.id, u.firstName,u.lastName,u.gender,u.email,u.phone, DATE_FORMAT(u.birthday, '%d-%m-%Y') as birthday, u.shippingAddress as shippingAddress_id, u.billingAddress as billingAddress_id, billing_address.street1 as billing_street1, billing_address.street2 as billing_street2, billing_address.city as billing_city, billing_address.zip as billing_zip, billing_address.state as billing_state, billing_address.country as billing_country, shipping_address.street1 as shipping_street1, shipping_address.street2 as shipping_street2, shipping_address.city as shipping_city, shipping_address.zip as shipping_zip, shipping_address.state as shipping_state, shipping_address.country as shipping_country, p.practitioner as practitioner_id, p.height, p.weight,  p_prac.user as user_id, prac_user.firstName as practitioner_firstName, prac_user.lastName as practitioner_lastName, p_prac.facility, p_prac.unit FROM footscanningdb.user as u LEFT join footscanningdb.address as billing_address on billing_address.id = u.billingAddress LEFT JOIN footscanningdb.address shipping_address on shipping_address.id = u.shippingAddress INNER JOIN footscanningdb.patient as p on  p.user = u.id LEFT JOIN footscanningdb.practitioner as p_prac on  p_prac.id = p.practitioner LEFT JOIN footscanningdb.user as prac_user on p_prac.user = prac_user.id")
        records = cursor.fetchall()
        return {
            'statusCode': 200,
            'body': records
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
