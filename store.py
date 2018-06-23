from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
from datetime import date
import json
import pymysql


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='!Newyork17',
                             db='store_adv',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

@get("/admin")
def admin_portal():
	return template("pages/admin.html")

@get("/categories")
def category() :
    try :
        with connection.cursor() as cursor:
            sql = "SELECT * FROM CATEGORIES"
            cursor.execute(sql)
            get_cat = cursor.fetchall()
            result = {
            "STATUS" : "SUCCESS",
            "MSG" : "success",
            "CATEGORIES" : get_cat,
            "CODE" : 200
            }
    except :
        result={
            "STATUS" : "ERROR",
            "MSG" : "internal error",
            "CODE" : 500
        }
    return json.dumps(result)


@get("/product/<id>")
def get_a_product(id) :
        with connection.cursor() as cursor:
            sql = "SELECT * FROM PRODUCTS WHERE id='{}'".format(id)
            cursor.execute(sql)
            get_cat = cursor.fetchall()
            if get_cat:
                result = {
                    "STATUS": "ERROR",
                    "MSG": "product not found",
                    "CODE": 404
                }
            else:
                try:
                    with connection.cursor() as cursor:
                        sql = "SELECT * FROM PRODUCTS WHERE id='{}'".format(id)
                        cursor.execute(sql)
                        get_cat = cursor.fetchall()
                        result = {
                            "STATUS": "SUCCESS",
                            "MSG": "success",
                            "PRODUCT": get_cat,
                            "CODE": 200
                        }
                except :
                    result = {
                        "STATUS": "ERROR",
                        "MSG": "internal error",
                        "CODE": 500
                    }
        return json.dumps(result)


@get("/products")
def all_products() :
    try :
        with connection.cursor() as cursor:
            sql = "SELECT * FROM PRODUCTS"
            cursor.execute(sql)
            get_cat = cursor.fetchall()
            result={
                "STATUS": "SUCCESS",
                "MSG": "success",
                "PRODUCTS": get_cat,
                "CODE": 200
            }
    except :
        result = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CODE": 500
        }
    return json.dumps(result)


@get("/category/<id>/products")
def products_by_category(id) :
    try :
        with connection.cursor() as cursor:
            sql = "SELECT * FROM PRODUCTS as p LEFT JOIN CATEGORIES as c ON p.category=c.id WHERE p.category={}".format(id)
            cursor.execute(sql)
            get_cat = cursor.fetchall()
            result={
                "STATUS": "SUCCESS",
                "MSG": "success",
                "PRODUCTS": get_cat,
                "CODE": 200
            }
    except :
        result = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CODE": 500
        }
    return json.dumps(result)


@route("/category/<id>", method="DELETE")
def delete_category(id) :
    try:
        with connection.cursor() as cursor:
            sql="DELETE FROM CATEGORIES WHERE id='{}'".format(id)
            cursor.execute(sql)
            connection.commit()
            result={
                "STATUS": "SUCCESS",
                "MSG": "success",
                "CODE": 201
            }
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CODE": 500
        }
    return json.dumps(result)


@route("/product/<id>", method="DELETE")
def delete_product(id) :
    try :
        with connection.cursor() as cursor:
            sql = "DELETE FROM PRODUCTS WHERE id='{}'".format(id)
            cursor.execute(sql)
            connection.commit()
            result = {
                "STATUS": "SUCCESS",
                "MSG": "success",
                "CODE": 201
            }
    except :
        result = {
            "STATUS": "ERROR",
            "MSG": "product not found, internal error",
            "CODE": 500
        }
    return json.dumps(result)

@post("/category")
def add_category():
    cat_name = request.POST.get('name')
    name = json.dumps(cat_name)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO categories(name) VALUES({})".format(name)
            cursor.execute(sql)
            connection.commit()
            id = cursor.lastrowid
        result={
            "STATUS": "success",
            "CAT_ID": id,
            "CODE": 201
        }
    except:
        result = {
            "STATUS": "error",
            "MSG": "INTERNAL ERROR",
            "CODE": 500
        }
    return json.dumps(result)

@post("/product")
def add_product():
    get_id = json.dumps(request.POST.get('id'))
    getTitle = json.dumps(request.POST.get('title'))
    getCategory = request.POST.get('category')
    getPrice = request.POST.get('price')
    getDescription = json.dumps(request.POST.get('desc'))
    getImg_Url = json.dumps(request.POST.get('img_url'))
    getFavorite = request.POST.get('favorite')
    getDate = str(date.today())
    get_date=json.dumps(getDate)
    if getFavorite == 'on':
        getFavorite = 1
    else:
        getFavorite = 0
    if getCategory== '""':
        result = {
            "STATUS": "SUCCESS",
            "MSG": "bad request",
            "CODE": 400
        }
    if not getCategory== '""':
        try:
            with connection.cursor() as cursor:
                if get_id == '""':
                    sql = "INSERT INTO products(category,price,title,description,img_url,date_created,favorite)VALUES({},{},{},{},{},{},{})".format(
                        getCategory, getPrice, getTitle, getDescription, getImg_Url, get_date, getFavorite)
                else:
                    sql = "UPDATE products SET category={},price={},title={},description={},img_url={},date_created={},favorite={} WHERE id={}".format(
                        getCategory, getPrice, getTitle, getDescription, getImg_Url, get_date, getFavorite, get_id)
                cursor.execute(sql)
                connection.commit()
                id = cursor.lastrowid
            result={
                "STATUS": "SUCCESS",
                "MSG": "product updated/created successfully",
                "PRODUCT_ID": id,
                "CODE": 201
            }
        except:
            result = {
                "STATUS": "ERROR",
                "MSG": "INTERNAL ERROR",
                "CODE": 500
            }
    return json.dumps(result)



@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=7000)
