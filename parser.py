import sys
import xml.dom.minidom as miniDom
import mysql.connector as myConnector

xhtmlFile = sys.argv[1]
productID = sys.argv[2]
doc = miniDom.parse(xhtmlFile)
root = doc.documentElement

#############################################################################################################
#Retrieving Data
#############################################################################################################
productName = root.getElementsByTagName("title")[0].childNodes[0].nodeValue
productDescription = root.getElementsByTagName("meta")[2].getAttribute("content")
productURL = root.getElementsByTagName("meta")[11].getAttribute("content")
#Assigns product price and image url based on store
#RiteAid
if(productURL.find("riteaid") != -1):
	store = "RiteAid"
	productName = productName.replace(" | Rite Aid","");
	productPrice = root.getElementsByTagName("meta")[12].getAttribute("content")
	imageURL = root.getElementsByTagName("meta")[9].getAttribute("content")
	#productReview = 5.0

#Ulta	
else:
	store = "Ulta"
	productName = productName.replace(" | Ulta Beauty","");
	productPrice = root.getElementsByTagName("meta")[13].getAttribute("content")
	imageURL = root.getElementsByTagName("meta")[8].getAttribute("content")
	#productReview = root.getElementsByTagName("p")[7].childNodes[0].nodeValue;
#Need to get Product Reviews
productReview = 5.0
#############################################################################################################

#############################################################################################################
#FOR TESTING PURPOSES
#############################################################################################################

"""
print(productID)
print(productName)
print(productDescription)
print(productURL)
print(productPrice)
print(imageURL)

print(store)
print(productReview)
"""


"""
dummy = root.getElementsByTagName("script")

for i in range(len(dummy)):
	print(i)
	print(dummy[i].getAttribute("type"))

	for j in range(len(dummy[i].childNodes)):
		print(j)
		print(dummy[i].childNodes[j].nodeValue)
"""
#############################################################################################################

#############################################################################################################
#INSERTING AND UPDATING DATABASE
#############################################################################################################
def insert(cursor,store):
    if (store=="RiteAid"): 
    	query = '''INSERT INTO RiteAid(productID,productName,productDescription,productPrice,productURL,imageURL,productReview) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    else: 
    	query = '''INSERT INTO Ulta(productID,productName,productDescription,productPrice,productURL,imageURL,productReview) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    info = (productID,productName,productDescription,productPrice,productURL,imageURL,productReview)
    cursor.execute(query, info)


def update(cursor,store):
    if (store=="RiteAid"): 
    	query1 = 'UPDATE RiteAid SET productPrice=%s WHERE productID=%s'
    	query2 = 'UPDATE RiteAid SET productReview=%s WHERE productID=%s'
    else: 
    	query1 = 'UPDATE Ulta SET productPrice=%s WHERE productID=%s'
    	query2 = 'UPDATE Ulta SET productReview=%s WHERE productID=%s'
    cursor.execute(query1, (productPrice,productID))
    cursor.execute(query2, (productReview,productID))

try:
    cnx = myConnector.connect(host='localhost', user='root', password='hello', database='demo')
    cursor = cnx.cursor()
    
    existCheckQuery = f"SELECT COUNT(*) FROM {store} WHERE productID = {productID}"
    cursor.execute(existCheckQuery)
    data = cursor.fetchone()
    if(data[0]==0):
    	insert(cursor,store)
    	cnx.commit()
    else:
    	update(cursor,store)
    	cnx.commit()
    	
    cursor.close()
except myConnector.Error as err:
    print(err)
finally:
    try:
        cnx
    except NameError:
        pass
    else:
        cnx.close()
#############################################################################################################
