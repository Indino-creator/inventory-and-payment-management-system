# Here we will input the payment that customers made during the day

# All the payment will be registered by the shop keeper at the time of the payment

import mysql.connector

conn=mysql.connector.connect (
   host="localhost",
   user="root",
   password="----",
   database="inventory"
)

cursor=conn.cursor()

if conn.is_connected():
    print("The Database is connected successfully")

else:
    print("The Database is not connected successfully")    


def insert_payment():
    person_name=str(input("Enter the name of the person- "))
    product_name=str(input("Enter the product name "))
    product_brand=str(input("Enter the product brand- "))
    payment_type=str(input("Enter type of the payment (paid/pending)- "))
    amount=int(input("Enter the amount of the payment- "))
    payment_method=str(input("Enter the method of the payment- "))
    description=str(input("Enter the descirption of the payments "))

    query="""INSERT INTO payments(
    PERSON_NAME,
    PRODUCT_NAME,
    PRODUCT_BRAND,
    PAYMENT_TYPE,
    AMOUNT,
    PAYMENT_METHOD,
    DESCRIPTION
    
    ) values(%s,%s,%s,%s,%s,%s,%s)"""

    values=(person_name,product_name,product_brand,payment_type,amount,payment_method,description)

    try:
        cursor.execute(query,values)
        conn.commit()
        print(f"Record inserted successfully. ID: {cursor.lastrowid}")
        print("Thank you for using our software")
    except mysql.connector.Error as error:
        conn.rollback()
        print(f"Failed to insert record: {error}")
    finally:  
          if conn.is_connected():
                      cursor.close()
                      conn.close()
    
    global data_location
    data_location=(cursor.lastrowid)
    return 
insert_payment()                      


# Here we will store the bill data so that we can pass it for the bill generation

loc=data_location