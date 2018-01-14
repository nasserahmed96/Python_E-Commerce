from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from mysql.connector import errorcode
import mysql.connector
from .forms import Register, Login, Products
from django.template import loader
from smtplib import SMTP
import smtplib
# Create your views here.

logged_in = 0

#Home page 
def index(request):
    if logged_in == 1:
        message = "Welcome back"
        return render(request, 'MDC_Website/MDC_Home.html', {'message':message})
    return render(request, 'MDC_Website/MDC_Home.html')

#Account view to manage user products
def account(request, user_id):
    return HttpResponse(request)


#Get the products for this department

def showProducts(request):
    products = Products()
    if products.is_valid():
        department_name = products.cleaned_data['department_name_field']
        try:
            cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1', database = 'Medical_Device_Company_DB')
            cursor = cnx.cursor()
            query = "SELECT p_name FROM products WHERE p_department=(SELECT dep_id FROM department WHERE dep_name='Luxery')"
            cursor.execute(query)
            cnx.commit()
            cnx.close()
            return render(request, 'MDC_Website/MDC_Products.html', {'products':cursor})

        except mysql.connector.Error:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Something wrong"
        else:
            message = "Search complete"
            cnx.close() 
        
    return render(request, 'MDC_Website/MDC_Products.html')
#Get the products
def products(request):
    products_names = []
    products_description = []
    products_price = []
    products = [products_names, products_description, product_price]
    departments = ("SELECT p_name, p_price, p_description FROM product")
    #product_info = ("SELECT p_name, p_descrption, p_price FROM product WHERE p_department=(SELECT dep_id FROM department WHERE"
    #        " dep_name='{}')".format(department_name))
    try:
        cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1', database = 'Medical_Device_Company_DB')
        cursor = cnx.cursor()
        cursor.execute(departments)
        for product_name, product_price, product_description in cursor:
            products_names.append(str(product_name[0]))
            products_description.appned(str(product_description[0]))
            products_price.append(str(products_price[0]))
        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
            message = "Something wrong with our database"
        else:
            message = err
    else:
        cnx.close()

    return render(request, 'MDC_Website/MDC_Products.html', {'products':product_results})        

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
                cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1', database = 'Medical_Device_Company_DB')
                cursor = cnx.cursor()
                user_add = ("INSERT INTO user (u_name, u_password,u_address, u_age, u_disease, u_email, u_description, u_chronic_disease, u_categoury) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
                user_data = (user_name, user_password,user_address, user_age, user_disease, user_email, user_description, user_chronic_disease, 
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
            return render(request, 'MDC_Website/MDC_Register.html', {'form':form, 'welcome_message':welcome_message})
    else:
        form = Register()
    return render(request, 'MDC_Website/MDC_Register.html', {'form':form}) 
    
def login(request):
    if request.method == 'POST':
        login_form = Login(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data['user_name']
            user_password = login_form.cleaned_data['user_password']
            logged_user = ''
            try:
                i = 0
                cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1',
                        database = 'Medical_Device_Company_DB')
                cursor = cnx.cursor()
                login_query = ("SELECT u_name FROM user WHERE u_email=%s AND u_password=%s")
                email_password = (user_email, user_password)
                cursor.execute(login_query, email_password)
                #check for user email and password
                for u_name in cursor:
                    i = i + 1
                    logged_user = u_name
                if i == 1:
                    logged_in = 1
                    message = "Welcome back: {}".format(logged_user)
                    return render(request, 'MDC_Website/MDC_Home.html', {'message':message})
                elif i > 1:
                    message = "Duplicate user name and password"
                else:
                    message = "Wrong user name or password"
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENEIED.ERROR or err.errno == errorcode.ER_BAD_DB_ERR:
                    message = "Sorry somthing wrong with our database"
                    return render(request, 'MDC_Website/MDC_Login.html', {'login_form':login_form, 'message':message})
            else:
                cnx.close() 
            return render(request, 'MDC_Website/MDC_Login.html', {'login_form':login_form, 'message':message})
    else:
        login_form = Login()
    return render(request, 'MDC_Website/MDC_Login.html',{'login_form':login_form})


def account(request):

    return HttpResponse("Welcome to user account")
