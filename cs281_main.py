import sqlite3
import PySimpleGUI as sg
from datetime import timedelta, date
import random
import re

# DB Connect

con = sqlite3.connect('database.db')
print(con)
cur = con.cursor()


class project_ui:
    def __init__(self):
        self.layout = None
        self.window = None
        self.login_user_name = 0
        self.login_user_type = 0
        self.sup_id = 0
        self.cust_id = 0
        self.total_price = 0
        self.order_id = 0

    def window_welcome(self):

        self.layout = [[sg.Text('Welcome to the Online Shopping System. Please enter your information.')],
                       [sg.Button('New Customer')],
                       [sg.Button('New Supplier')],
                       [sg.Button('Login Screen')]]
        return sg.Window('Login Window', self.layout)

    def window_login(self):
        self.layout = [[sg.Text('Please enter your information to login your account')],
                       [sg.Text('User_name:', size=(10, 1)), sg.Input(size=(10, 1), key='user_name')],
                       [sg.Text('Password:', size=(10, 1)), sg.Input(size=(10, 1), key='password')],
                       [sg.Button('Login'), sg.Button('Back to Main')]]
        return sg.Window('Login Window', self.layout)

    def window_sup(self):
        self.layout = [
            [sg.Button('Add a new product! ')],
            [sg.Button('Delete a product')],
            [sg.Button('Update a product')],
            [sg.Button('Logout')]]

        return sg.Window('Enrol Window', self.layout)

    def window_ship(self):
        return None

    def window_cust(self):
        self.layout = [
            [sg.Button('List the products')],
            [sg.Button('Old Orders')],
            [sg.Button('Logout')]]

        return sg.Window('Customer Window', self.layout)

    def window_create_supplier(self):
        self.layout = [[sg.Text('user_name:', size=(12, 1)), sg.Input(key='user_name', size=(10, 1))],
                       [sg.Text('name:', size=(12, 1)), sg.Input(key='name', size=(10, 1))],
                       [sg.Text('surname:', size=(12, 1)), sg.Input(key='surname', size=(10, 1))],
                       [sg.Text('phone_number:', size=(12, 1)), sg.Input(key='pno', size=(10, 1))],
                       [sg.Text('password:', size=(12, 1)), sg.Input(key='pword', size=(10, 1))],
                       [sg.Text('e_mail:', size=(12, 1)), sg.Input(key='mail', size=(10, 1))],
                       [sg.Text('shop_name:', size=(12, 1)), sg.Input(key='shop_name', size=(10, 1))],
                       [sg.Text('url:', size=(12, 1)), sg.Input(key='url', size=(10, 1))],
                       [sg.Text('work_address:', size=(12, 1)), sg.Input(key='work_address', size=(10, 1))],

                       [sg.Button('Enrol')]]
        # print(layout)
        # cur.execute("params")
        return sg.Window('Enrol Window', self.layout)

    def insert_supplier(self, values):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        user_list = []
        u_name = values['user_name']
        p_name = values['name']
        p_surname = values['surname']
        password = values['pword']
        phone_number = values['pno']
        e_mail = values['mail']
        shop_name = values['shop_name']
        url = values['url']
        work_address = values['work_address']
        cur.execute('SELECT user_name FROM user')
        a = list(cur.fetchall())
        print(a)
        for i in range(0, len(a)):
            user_list.append((a[i][0]))
        if u_name in user_list:
            sg.popup('User Name already taken')
        else:
            if u_name == '' or p_name == '' or p_surname == '' or password == '' or phone_number == '' or e_mail == '':
                sg.popup('All areas must be filled!')
            elif not (re.fullmatch(regex, e_mail)):
                sg.popup('Invalid Email')       
            elif len(phone_number) != 10:
                sg.popup('Wrong Tel no!')
            else:
                cur.execute('SELECT MAX(sup_id) FROM supplier')
                row = cur.fetchone()
                id = int(row[0]) + 1
                cur.execute('INSERT INTO User VALUES (?,?,?,?,?,?)',
                            (u_name, p_name, p_surname, phone_number, password, e_mail))
                cur.execute('INSERT INTO supplier VALUES (?,?,?,?,?)', (id, url, shop_name, work_address, u_name))
                con.commit()
                self.window.close()
                self.window = self.window_welcome()

    def window_add_product(self):
        cat = []
        for row in cur.execute('SELECT DISTINCT CAT_NAME FROM category'):
            cat.append(row)
        self.layout = [[sg.Text('description:', size=(12, 1)), sg.Input(key='description', size=(10, 1))],
                       [sg.Text('price:', size=(12, 1)), sg.Input(key='price', size=(10, 1))],
                       [sg.Text('stock count:', size=(12, 1)), sg.Input(key='stock_count', size=(10, 1))],
                       [sg.Text('supplier id:' + str(self.sup_id))],
                       [sg.Listbox(cat, size=(20, 5), key='cat')],
                       [sg.Button('Add')], [sg.Button('Back to Supplier Menu')]]

        return sg.Window('Add Window_', self.layout)

    def window_delete_product(self):
        products = []

        for product in cur.execute('SELECT product_id, description FROM products_supplies WHERE sup_id = ?',
                                   (self.sup_id,)):
            products.append(product)

        if len(products) == 0:
            sg.popup("There is no product for this user")
            return self.window_sup()
        self.layout = [[sg.Listbox(products, size=(20, 5), key='pid')],
                       [sg.Button('Delete'), sg.Button('Back to Supplier Menu')]]

        return sg.Window('Delete Product', self.layout)

    def insert_product(self, values):

        cur.execute('SELECT MAX(product_id) FROM products_supplies')
        row = int(cur.fetchone()[0])

        product_id = row + 1
        description = values['description']
        price = values['price']
        stock_count = values['stock_count']
        cat_name = values['cat']
        print(cat_name)
        cur.execute('SELECT description FROM products_supplies WHERE description=?', (description,))
        products = cur.fetchone()
        print(products)
        if products is not None:
            sg.popup('Already Added Product!')
        else:
            if len(cat_name) != 0:
                cat_id = ''.join(cat_name[0])
                cat_id = (cur.execute('SELECT CAT_DID FROM category WHERE CAT_NAME=?', (cat_id,)))
                cat_id = cur.fetchone()
                cat_id = ''.join(cat_id[0])
                print(cat_id)
            else:
                cat_id = ''

            if (product_id == '' or description == '' or price == '' or stock_count == '' or cat_id == ''):
                sg.popup("There is missing information, try again!")
            elif not price.isnumeric() or not price.isnumeric():
                sg.popup("Price or Stock must be numeric!")


            else:
                cur.execute('INSERT INTO products_supplies VALUES (?,?,?,?,?)',
                            (product_id, description, price, stock_count, self.sup_id))
                cur.execute('INSERT INTO has2 VALUES (?,?)', (product_id, cat_id))
                con.commit()
                sg.popup("Added Successfully")
                self.window.close()
                self.window = self.window_sup()

    def window_list_products(self):
        cur.execute('''SELECT products_supplies.description,  products_supplies.price,supplier.shop_name,
        CAT_NAME,products_supplies.product_id FROM category, products_supplies, has2,supplier WHERE 
        products_supplies.product_id=has2.product_id  AND supplier.sup_id=products_supplies.sup_id
        AND has2.CAT_DID=category.CAT_DID AND products_supplies.stock_count >0 ''')
        list_pro = cur.fetchall()

        self.layout = []
        self.layout.append(
            [sg.Text("Product", size=(15, 1)), sg.Text("Price", size=(15, 1)), sg.Text("Shop Name", size=(15, 1)),
             sg.Text("Category", size=(15, 1))])
        for i in range(0, len(list_pro)):
            temp = [sg.Text(list_pro[i][0], size=(15, 1)), sg.Text(list_pro[i][1], size=(15, 1)),
                    sg.Text(list_pro[i][2], size=(15, 1)), sg.Text(list_pro[i][3], size=(15, 1)),
                    sg.Button("Add Product", key=(('Add',list_pro[i][4]))),sg.Button("Evaluations of Product", key=(('Yorum',list_pro[i][4])))]
            cur.execute('SELECT stock_count FROM products_supplies WHERE product_id= ? ', (list_pro[i][4],))
            self.layout.append(temp)

        self.layout.append([sg.Button('Back'), sg.Button('Payment Stage')])
        return sg.Window('List Products', self.layout)

    def button_login(self, values):
        uname = values['user_name']
        upass = values['password']
        if uname == '':
            sg.popup('ID cannot be empty')
        elif upass == '':
            sg.popup('Password cannot be empty')
        else:
            # first check if this is a valid user
            cur.execute('SELECT user_name, name, surname FROM user WHERE user_name = ? AND password = ?',
                        (uname, upass))
            row = cur.fetchone()
            if row is None:
                sg.popup('ID or password is wrong!')
            else:
                self.login_user_name = row[0]
                self.name_of_user = row[1]
                print(uname)
                cur.execute('SELECT user_name FROM customer WHERE user_name = ?', (uname,))
                row_customer = cur.fetchone()
                cur.execute('SELECT user_name FROM supplier WHERE user_name = ?', (uname,))
                row_supplier = cur.fetchone()
                cur.execute('SELECT user_name FROM shipment_company WHERE user_name = ?', (uname,))
                row_shipment = cur.fetchone()
                if row_shipment is not None:
                    self.login_user_type = 'Shipment'
                    sg.popup('Welcome, ' + self.name_of_user + ' ( Shipment Company)')
                    self.window.close()
                    self.window = self.window_ship()
                elif row_supplier is not None:
                    self.login_user_type = 'Supplier'
                    sg.popup('Welcome, ' + self.name_of_user + ' ( Supplier)')
                    self.window.close()
                    cur.execute('SELECT sup_id FROM supplier WHERE user_name=?', (uname,))
                    self.sup_id = cur.fetchone()
                    self.sup_id = int(''.join(filter(str.isdigit, self.sup_id)))

                    self.window = self.window_sup()

                elif row_customer is not None:
                    self.login_user_type = 'Customer'
                    sg.popup('Welcome, ' + self.name_of_user + ' (Customer)')
                    self.window.close()
                    cur.execute('SELECT customer_id FROM customer WHERE user_name=?', (uname,))
                    self.cust_id = cur.fetchone()
                    self.cust_id = int(''.join(filter(str.isdigit, self.cust_id)))
                    self.window = self.window_cust()
                else:
                    sg.popup('DB Error')

    def update_product(self):
        products = []

        for product in cur.execute('SELECT product_id, description FROM products_supplies WHERE sup_id = ?',
                                   (self.sup_id,)):
            products.append(product)

        if len(products) == 0:
            sg.popup("There is no product for this user")
            return self.window_sup()
        self.layout = [[sg.Listbox(products, size=(20, 5), key='pid')],
                       [sg.Button('Select to Update')], [sg.Button('Back to Supplier Menu')]]

        return sg.Window('Update Product', self.layout)

    def update_details(self, values):
        details = []
        details = cur.execute('SELECT description,price,stock_count FROM products_supplies WHERE product_id = ?',
                              (values["pid"][0][0],))
        details = cur.fetchone()
        self.layout = [[sg.Text("Details:  " + details[0]), sg.Input(key='new_description', size=(10, 1))],
                       [sg.Text("Price:  " + str(details[1])), sg.Input(key='new_price', size=(10, 1))],
                       [sg.Text("stock_count:  " + str(details[2])), sg.Input(key='new_stock', size=(10, 1))],
                       [sg.Button('OK'), sg.Button('Back to Supplier Menu')]]
        return sg.Window('Update Detail', self.layout)

    def window_pay(self, cart_list, adres, payment_method):
        self.layout = []
        self.total_price = 0
        for el in cart_list:
            pro_price = cur.execute('SELECT price FROM products_supplies WHERE product_id = ?', (el,))
            pro_price = cur.fetchone()
            self.total_price += (pro_price[0])
            pro_name = cur.execute('SELECT description FROM products_supplies WHERE product_id = ?', (el,))
            pro_name = cur.fetchone()
            temp = [sg.Text((pro_name[0]), size=(15, 1)), sg.Text((pro_price[0]), size=(15, 1))]
            self.layout.append(temp)
        temp = [sg.Text('Total:' + str(self.total_price))]
        self.layout.append(temp)
        temp = [sg.Text('Payment Method:' + str(payment_method)), sg.Button('Update Payment Method')]
        self.layout.append(temp)
        temp = [sg.Text('Address:' + str(adres)), sg.Button('Update Address')]
        self.layout.append(temp)
        temp = [sg.Button('Pay!')]
        self.layout.append(temp)
        return sg.Window('Cart', self.layout)

    def window_address(self):
        self.layout = [[sg.Text("New Address:  "), sg.Input(key='new_address', size=(10, 1))],
                       [sg.Button('Confirm Address')]]
        return sg.Window('Update Address', self.layout)

    def window_new_payment_method(self):
        payment_types = ['Cash', 'Credit Card', 'EFT']
        self.layout = [[sg.Listbox(payment_types, size=(20, 5), key='pay')], [sg.Button('Confirm Payment Type')]]
        return sg.Window('Update Payment Method', self.layout)

    def create_order(self, adres, payment_method, cart_list):
        cur.execute('SELECT MAX(order_id) FROM order_delivery')
        max_order = cur.fetchone()
        order_num = int(max_order[0]) + 1
        shipcompid = []
        cur.execute('SELECT shipment_id FROM shipment_company')
        shipment_ids = cur.fetchall()
        a = list(shipment_ids)
        for i in range(0, len(a)):
            shipcompid.append((a[i][0]))
        shipcompany = (random.choice(shipcompid))
        todaysDate = date.today().strftime('%d-%m-%Y')
        EndDate = date.today() + timedelta(days=3)
        estimated_delivery_date = EndDate.strftime('%d-%m-%Y')
        cur.execute('INSERT INTO order_delivery VALUES (?,?,?,?,?,?,?,?)', (
            order_num, todaysDate, adres, payment_method, estimated_delivery_date, shipcompany, self.cust_id,
            self.total_price))
        con.commit()
        unique_pro = set(cart_list)
        countvspro = dict((i, cart_list.count(i)) for i in cart_list)
        counts = []
        for el in unique_pro:
            count = countvspro[el]
            cur.execute('INSERT INTO include VALUES (?,?,?) ', (el, order_num, count))
            con.commit()

    def oldorders(self, cust_id):

        self.layout = []
        cur.execute(
            '''SELECT product_id FROM order_delivery, include WHERE order_delivery.order_id=include.order_id AND customer_id=? ''',
            (cust_id,))
        order_products = cur.fetchall()
        list_products = [i[0] for i in order_products]
        cur.execute('SELECT total_price, date,order_id FROM order_delivery WHERE customer_id=?', (cust_id,))
        order_ids = cur.fetchall()
        if not order_ids:
            self.layout.append([[sg.Text('No Past Order!')]])
        else:
            u = []
            for el in order_ids:
                el = {'Order_id': str(el[2]), 'Date': str(el[1]), 'Total Price ': str(el[0])}
                u.append(el)
            self.layout.append([sg.Listbox(u, size=(50, 5), key='order_id')])
            det_but = [sg.Button('Order Details')]
            self.layout.append(det_but)
        ev_order = [sg.Button('Evaluate Order-Shipment')]
        self.layout.append(ev_order)
        back_but = [sg.Button('Back')]
        self.layout.append(back_but)
        return sg.Window('Add Window', self.layout)

    def see_details(self, order_id1):
        products = []
        self.layout = []
        for row in cur.execute(
                'SELECT description, products_supplies.product_id FROM products_supplies,include WHERE '
                'include.product_id=products_supplies.product_id AND order_id=?',
                (order_id1,)):
            products.append(row)
        self.layout.append([sg.Listbox(products, size=(50, 5), key='product')])
        ev_p = [sg.Button('Evaluate Product')]
        self.layout.append(ev_p)
        back_but = [sg.Button('Back')]
        self.layout.append(back_but)
        return sg.Window('Order Detail', self.layout)

    def evaluate_shipment(self):
        list_of_points = [1,2,3,4,5]
        self.layout = [[sg.Text("Comments:  "), sg.Input(key='com', size=(20, 2))],
                       [sg.Text("Points(1-5):  "), sg.Listbox(list_of_points, size=(20, 5), key='points')],
                       [sg.Button('Approve'), sg.Button('Back')]]

        return sg.Window('Shipment Evaluation', self.layout)

    def evaluate_product(self):
        list_of_points = [1,2,3,4,5]
        self.layout = [[sg.Text("Comments:  "), sg.Input(key='com', size=(20, 2))],
                       [sg.Text("Points(1-5):  "), sg.Listbox(list_of_points, size=(20, 5), key='points')],
                       [sg.Button('Evaluate'), sg.Button('Back')]]

        return sg.Window('Product Evaluation', self.layout)
    
    def print_ev(self,product_ev):
        self.layout = []
        self.layout.append([sg.Text("Star", size=(3, 1)), sg.Text("Comment", size=(15, 1))])
        if product_ev==[]:
            self.layout.append([sg.Text("No Past Evaluations!", size=(15, 1))])
        else:
            for el in product_ev: 
                self.layout = [[sg.Text("Stars: "+el[0])],
                               [sg.Text("Comment:" + el[1])]]
        back_but = [sg.Button('Back to Product List')]
        self.layout.append(back_but)
        return sg.Window('Product Comments', self.layout)
                           
Xyz = project_ui()
Xyz.window = Xyz.window_welcome()
cart_list = []
shop_active = 0
while True:
    event, values = Xyz.window.read()
    print(event)
    print(values)
    print(shop_active)
    
    if shop_active == 1 and event != 'Back' and event !='Back to Product List':
        
        if event == 'Payment Stage':
            shop_active = 0
            payment_method = cur.execute('SELECT default_payment_method FROM customer WHERE customer_id = ?',
                                         (Xyz.cust_id,))
            payment_method = cur.fetchone()
            payment_method = ''.join(payment_method[0])
            adres = cur.execute('SELECT address  FROM customer WHERE customer_id = ?', (Xyz.cust_id,))
            adres = cur.fetchone()
            adres = ''.join(adres[0])
            Xyz.window.close()
            Xyz.window = Xyz.window_pay(cart_list, adres, payment_method)

        elif event != 'Payment Stage':
            event=[event]
            d=dict(event)
            key_event=list(d.keys())[0]
            if key_event=='Add':
                product_id = d['Add']
                cur.execute('SELECT stock_count FROM products_supplies WHERE product_id= ? ', (product_id,))
                stock_count = cur.fetchone()
                if stock_count[0] == 0:
                    sg.popup('No stock!')
                else:
                    stock_count = stock_count[0] - 1
                    print(stock_count)
                    cur.execute('UPDATE products_supplies SET stock_count= ? WHERE product_id= ? ',
                            (stock_count, product_id))
                    cart_list.append(d['Add'])
                    con.commit()
            elif key_event=='Yorum':
                product_id = d['Yorum']
                Xyz.window.close()
                product_ev=[]
                for row in cur.execute('SELECT prod_star,prod_comment FROM evaluate_product WHERE product_id= ? ',(product_id,)):
                     product_ev.append(row)
                Xyz.window= Xyz.print_ev (product_ev)
                                 
                
    if event=='Back to Product List':
        Xyz.window.close()
        Xyz.window = Xyz.window_list_products()
        
    if event=='Back to Main':
        Xyz.window.close()
        Xyz.window = Xyz.window_welcome()
    if event == 'Update Address':
        Xyz.window.close()
        Xyz.window = Xyz.window_address()
    if event == 'Update Payment Method':
        Xyz.window.close()
        Xyz.window = Xyz.window_new_payment_method()
        print(values)

    if event == 'Confirm Payment Type':
        Xyz.window.close()
        payment_method = values['pay'][0]
        Xyz.window = Xyz.window_pay(cart_list, adres, payment_method)

    if event == 'Confirm Address':
        Xyz.window.close()
        adres = values['new_address']
        Xyz.window = Xyz.window_pay(cart_list, adres, payment_method)

    if event == 'Back to Supplier Menu':
        Xyz.window.close()
        Xyz.window = Xyz.window_sup()

    if event == 'Pay!':
        Xyz.window.close()
        Xyz.create_order(adres, payment_method, cart_list)
        sg.popup('Order Created!')

    if event == 'Add':
        Xyz.insert_product(values)

    if event == 'Login Screen':
        Xyz.window.close()
        Xyz.window = Xyz.window_login()
    if event == 'New Supplier':
        new_user = 'supplier'
        Xyz.window.close()
        Xyz.window = Xyz.window_create_supplier()
    if event == 'Enrol':
        if new_user == 'supplier':
            Xyz.insert_supplier(values)

    if event == 'Login':
        print(values)
        Xyz.button_login(values)

    if event == 'Old Orders':
        Xyz.window.close()
        print("values", values)
        Xyz.window = Xyz.oldorders(Xyz.cust_id)
    if event == 'Order Details':
        order_id1 = values['order_id'][0]['Order_id']
        Xyz.window.close()
        Xyz.window = Xyz.see_details(order_id1)

    if event == 'Back' and Xyz.login_user_type == 'Customer':
        Xyz.window.close()
        Xyz.window = Xyz.window_cust()
        shop_active = 0

    if event == 'Add a new product! ':
        Xyz.window.close()
        Xyz.window = Xyz.window_add_product()

    if event == 'Delete a product':
        Xyz.window.close()
        Xyz.window = Xyz.window_delete_product()

    if event == 'Main Page':
        Xyz.window.close()
        Xyz.window = Xyz.window_welcome()

    if event == 'List the products':
        Xyz.window.close()
        Xyz.window = Xyz.window_list_products()
        shop_active = 1
    if event == 'Delete':
        Xyz.window.close()

        cur.execute('DELETE FROM products_supplies WHERE product_id = ?', (values["pid"][0][0],))
        cur.execute('DELETE FROM has2 WHERE product_id = ?', (values["pid"][0][0],))
        con.commit()
        sg.popup("The product is successfully deleted")

        Xyz.window = Xyz.window_sup()
    if event == 'Update a product':
        Xyz.window.close()
        Xyz.window = Xyz.update_product()
    if event == 'Select to Update':
        Xyz.window.close()
        Xyz.window = Xyz.update_details(values)
        p_id = values["pid"][0][0]
        print(p_id)
    if event == 'OK':
        Xyz.window.close()
        print(values)
        details = ["description", "price", "stock_count"]
        i = -1
        for el_details in ["new_description", "new_price", "new_stock"]:
            i = i + 1
            if values[el_details] != '':
                cur.execute('UPDATE products_supplies SET ' + details[i] + '=? WHERE product_id=?', (values[
                                                                                                         el_details],
                                                                                                     p_id))
                con.commit()
        sg.popup("The product is successfully updated")
        Xyz.window = Xyz.window_sup()
    if event == 'Logout':
        Xyz.window.close()
        sg.popup('Bye')
        Xyz.login_user_name = 0
        Xyz.login_user_type = 0
        Xyz.sup_id = 0
        cart_list = []
        Xyz.window = Xyz.window_welcome()
        Xyz.cust_id = 0


    if event == 'Evaluate Order-Shipment':
        Xyz.order_id = values.get("order_id")[0].get("Order_id")
        Xyz.window.close()
        Xyz.window = Xyz.evaluate_shipment()
    if event=='Evaluate Product':
        Xyz.product_id = values['product'][0][1]
        Xyz.window.close()
        Xyz.window = Xyz.evaluate_product()
        


    if event == 'Approve':
        print("Values----", values)

        try:

            cur.execute("INSERT INTO evaluate_delivery VALUES (?,?,?,?)", (values.get("points")[0], values.get("com"), Xyz.cust_id, Xyz.order_id))
            con.commit()
        except:
            sg.popup('Already Evaluated!')
            con.rollback()
           

        Xyz.window.close()
        Xyz.window = Xyz.window_cust()
        
    if event == 'Evaluate':
        print("Values----", values)
        cur.execute("SELECT sup_id FROM products_supplies WHERE product_id=?",(Xyz.product_id,))
        sup_id=cur.fetchone()[0]
        try:
            cur.execute("INSERT INTO evaluate_product VALUES (?,?,?,?,?)", (Xyz.product_id,Xyz.cust_id,sup_id,values.get("points")[0],values.get("com")))
            con.commit()
        except:
            sg.popup('Already Evaluated')
            con.rollback()

        Xyz.window.close()
        Xyz.window = Xyz.window_cust()


    elif event == sg.WIN_CLOSED:
        break

Xyz.window.close()
