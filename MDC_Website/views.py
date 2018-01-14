from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from mysql.connector import errorcode
import mysql.connector
from .forms import Register, Login, Products
from django.template import loader
from smtplib import SMTP
import smtplib
from django.views.decorators.http import require_http_methods


# Create your views here.


#Home page 
def index(request):
    return render(request, 'MDC_Website/MDC_Home.html')


#Get the products for this department
def showProducts(request):
    message = "Bism Allah"
    try:
        cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1',
                database = 'Medical_Device_Company_DB')
        cursor = cnx.cursor(buffered = True)
        query = ("SELECT p_id,p_name, p_price, p_description,p_image FROM product")
        cursor.execute(query)
        cnx.commit()
        data = cursor
        cnx.close()
        return render(request, 'MDC_Website/MDC_Products.html', {'products': data})
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Something wrong"
        else:
            message = err
    else:
        message = "Search complete"
        cnx.close() 
    return render(request, 'MDC_Website/MDC_Products.html', {'message': message})


#Show product details
def viewProduct(request, product_id):
    data = []
    if request.method == "GET":
        try:
            cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1',
                    database = 'Medical_Device_Company_DB')
            cursor = cnx.cursor(buffered = True)
            query = ("SELECT p_name, p_price, p_description,"
                    "p_image from product where p_id = {}".format(product_id))
            cursor.execute(query)
            cnx.commit()
            data = cursor
            cnx.close()
            return render(request, 'MDC_Website/MDC_viewProduct.html', {'product': data,
                'product_id': product_id})
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Something wrong"
            else:
                message = err
        else:
            message = "Done"
            cnx.close()
    if request.method == "POST":
        if 'user_id' not in request.session:
            return render(request, 'MDC_Website/MDC_viewProduct.html', {'message': "You should log in first"})
        else:
            try:
                cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1',
                        database = 'Medical_Device_Company_DB')
                cursor = cnx.cursor(buffered = True)
                query = ("INSERT INTO user_product (u_id, p_id) VALUES ({}, {})".format(
                    request.session['user_id'], product_id))
                cursor.execute(query)
                cnx.commit()
                cnx.close()
                return render(request, 'MDC_Website/MDC_viewProduct.html',{"products":data, "message": "Done"})
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    message = "Something is wrong with permissions"
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    message = "Something is wrong with our DB"
                else:
                    message = err
            else:
                message = "Done"
                cnx.close()


    return render(request, 'MDC_Website/MDC_viewProduct.html', {'message':message})


def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_password = form.cleaned_data['user_password']
            user_address = form.cleaned_data['user_address']
            user_age = form.cleaned_data['user_age']
            user_disease = form.cleaned_data['user_disease']
            user_email = form.cleaned_data['user_email']
            user_description = form.cleaned_data['user_description']
            user_chronic_disease = form.cleaned_data['user_chronic_disease']
            user_categoury = form.cleaned_data['user_categoury']
            mdc_email = "servertest587@gmail.com"
            try:
                cnx = mysql.connector.connect(user = 'root', password = 'Nasora44',
                        host = '127.0.0.1', database = 'Medical_Device_Company_DB')
                cursor = cnx.cursor()
                user_add = ("INSERT INTO user (u_name, u_password,u_address, u_age, u_disease, u_email,"
                        "u_description, u_chronic_disease, u_categoury) VALUES"
                       " (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
                user_data = (user_name, user_password,user_address, user_age, user_disease,
                        user_email, user_description, user_chronic_disease, 
                        user_categoury)
                cursor.execute(user_add, user_data)
                cnx.commit()
                cursor.close()
                cnx.close()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    welcome_message = "Sorry something wrong with our DB please try again later"
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    welcome_message = "Something wrong with our DB server we trying to solve it"
                else:
                    welcome_message = err
            else:
                msg = "Thx for registration"
                email = smtplib.SMTP(host = 'smtp.gmail.com', port = 587)
                email.starttls()
                email.login(user = 'servertest587', password = 'GMAILTEST587')
                email.ehlo()
                email.sendmail(mdc_email, user_email, msg)
                email.quit()
                welcome_message = "Thx for registration"
                cnx.close()
            return render(request, 'MDC_Website/MDC_Register.html',
                    {'form':form, 'welcome_message':welcome_message})
    else:
        form = Register()
    return render(request, 'MDC_Website/MDC_Register.html', {'form':form}) 
    
def login(request):
    user_id=''
    user_password = ''
    user_name = ''
    if request.method == 'POST':
        login_form = Login(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data['user_name']
            user_password = login_form.cleaned_data['user_password']
            try:
                i = 0
                cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1',
                        database = 'Medical_Device_Company_DB')
                cursor = cnx.cursor()
                login_query = ("SELECT u_name, u_id FROM user WHERE u_email=%s AND u_password=%s")
                email_password = (user_email, user_password)
                cursor.execute(login_query, email_password)
                #check for user email and password
                for u_name, u_id in cursor:
                    i = i + 1
                    user_id = u_id
                    user_name = u_name
                if i == 1:
                    request.session['user_id'] = user_id
                    request.session['user_name'] = user_name
                    request.session.modified = True
                    message = ('Welcome back {}'.format(request.session['user_name']))
                    return render(request, 'MDC_Website/MDC_Home.html', {'message':message})
                elif i > 1:
                    message = "Duplicate user name and password"
                else:
                    message = "Wrong user name or password"
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENEIED.ERROR or err.errno == errorcode.ER_BAD_DB_ERR:
                    message = "Sorry somthing wrong with our database"
                    return render(request, 'MDC_Website/MDC_Login.html',
                            {'login_form':login_form, 'message':message})
            else:
                cnx.close() 
            return render(request, 'MDC_Website/MDC_Login.html', {'login_form':login_form, 'message':message})
    else:
        login_form = Login()
    return render(request, 'MDC_Website/MDC_Login.html',{'login_form':login_form})

def account(request):
    data = []
    #There is an error in the query: subquery return more than one row
    try:
        query = "SELECT order_id, p_id FROM user_product WHERE u_id = {}".format(request.session['user_id']) 
        cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1',
                database = 'Medical_Device_Company_DB')
        cursor = cnx.cursor(buffered = True)
        cursor.execute(query)
        data = cursor
        cnx.commit()
        message = "Hello:{} ".format(request.session['user_name'])
        return render(request, 'MDC_Website/MDC_Account.html', {'message': message, 'products': data})
    except mysql.connector.Error as err:
        message = err
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            message = "Something wrong with permissions"
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            message = "Something wrong with our database"
        return render(request, 'MDC_Website/MDC_Account.html', {'message':message})
    else:
        cnx.close()
        return render(request, 'MDC_Website/MDC_Account.html', {'message':"Execute else"})
    return render(request, 'MDC_Website/MDC_Account.html', {'message': message})
def logout(request):
    try:
        del request.session['user_id']
        request.session.flush()
    except KeyError:
        pass
    return render(request, 'MDC_Website/MDC_Home.html')
#This function is used to do all the DB stuff in order to speed up the website and reduce the lines of code
def dataBase(query):
    try:
        cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1',
                database = 'Medical_Device_Company_DB')
        cursor = cnx.cursor()
        cursor.execute(query)
        cursor.commit()
        return cursor
    except mysql.connector.Error as err:
        message = err
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            message = "Something wrong with permissions"
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            message = "Something wrong with our Database"
    else:
        cursor.close()
        cnx.close()

