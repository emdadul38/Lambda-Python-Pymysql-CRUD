# Python with pymysql CRUD Using AWS Lambda

## First need to create AWS RDS Database Create

![Image of RDS](https://github.com/emdadul38/Lambda-Python-Pymysql-CRUD/blob/master/images/1.png)
![Image of RDS](https://github.com/emdadul38/Lambda-Python-Pymysql-CRUD/blob/master/images/2.png)
![Image of RDS](https://github.com/emdadul38/Lambda-Python-Pymysql-CRUD/blob/master/images/3.png)
![Image of RDS](https://github.com/emdadul38/Lambda-Python-Pymysql-CRUD/blob/master/images/4.png)
![Image of RDS](https://github.com/emdadul38/Lambda-Python-Pymysql-CRUD/blob/master/images/5.png)

## 1. Create rds_config
```python
db_username = "admin"
db_password = "password"
db_name = "database_name"
port = 3306
db_endpoint = "******.*****.us-west-1.rds.amazonaws.com"
```
## 2. Pymysql connection
```python
import pymysql

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    logger.error(e)
    sys.exit()
```

## 3. Insert Statement
```python
sql = "INSERT INTO `user` (`firstName`, `lastName`,  `gender`, `birthday`,`email`, `phone`) VALUES(%s, %s, %s, %s, %s, %s)"
val = (event["firstName"], event["lastName"], event["gender"], event["birthday"], event["email"], event["phone"])

with conn.cursor() as cur:
   cur.execute(sql, val)
   conn.commit()
   user_id = cur.lastrowid
```

## 4. Read Statement
```python
  cursor = conn.cursor(pymysql.cursors.DictCursor)
  cursor.execute("SELECT u.id, u.firstName,u.lastName,u.gender,u.email,u.phone, DATE_FORMAT(u.birthday, '%d-%m-%Y') as birthday FROM footscanningdb.user as u ")
  records = cursor.fetchall()
  return {
      'statusCode': 200,
      'body': records
  }
```

## 5. Edit Statement
```python
  column = ""
  cursor = conn.cursor(pymysql.cursors.DictCursor)

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
      
   if column:
      column = column[:-2]

      updateStatement = "UPDATE user set "+ column +" where id=" + event["id"]

      # Execute the SQL UPDATE statement
      cursor.execute(updateStatement)
      conn.commit()
```
