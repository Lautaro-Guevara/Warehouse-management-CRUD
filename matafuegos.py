import sys
import mysql.connector
from mysql.connector import Error
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QTextEdit
from PyQt6.QtCore import QDate

#-----------------------------------------------------------------------------------------------------------------------------

class MainWindow(QWidget):
    """
    
    """
    def __init__(self):
        super().__init__()
        
        self.connection = self.create_connection()
        self.initUI()




    def create_connection(self):
        """
        Create the connection with the database.
        The username, password and other details are already entered. This will be modified in the future to create a user login
        """
        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                port = 3306,
                user="root",
                password="tipsadb",
                database="extinguisher_db"
            )
            if connection.is_connected(): #Connection verification
                print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection




    def initUI(self):
        """
        
        """


        self.setWindowTitle("Fire extinguisher manager")
        self.layout = QVBoxLayout()


        label = QLabel(""" 
        Welcome to fire extinguisher manager
        Made by: Lautaro Guevara
        Final project CSE111
        v1.0
        """)
        self.layout.addWidget(label)


        self.stacked_widget = QStackedWidget()


        # Create the pages
        self.main_page = self.create_main_page()
        self.extinguisher_page = self.create_extinguisher_page()


        # Add pages to the QStackedWidget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.extinguisher_page)
        


        # Add QStackedWidget to the main layout
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)


        # Show home page
        self.stacked_widget.setCurrentWidget(self.main_page)




    def create_main_page(self):
        """
        
        """

        page = QWidget()
        layout = QVBoxLayout()


        #Create "Fire extinguisher manager" button
        extinguisher_button = QPushButton("Fire extinguisher manager") #Step 1: Create button using "QPushButton()" and assign it the name that will be displayed to the user
        extinguisher_button.clicked.connect(lambda: self.show_page(self.extinguisher_page)) #Step 2: Assign an action on click
        layout.addWidget(extinguisher_button) #Step 3: Add Button to Layout


        page.setLayout(layout) #The layout is inserted into the page
        return page




    def create_extinguisher_page(self):
        """
        Create the page where the application functions are located. It will appear once the "Fire extinguisher manager" button is clicked
        """
        page = QWidget()
        layout = QVBoxLayout()


        welcome_label = QLabel("Fire Extinguisher Manager") #Create the "" tag using ""
        layout.addWidget(welcome_label)




        #Create "Add Extinguisher manager" button
        add_extinguisher_button = QPushButton("Add Extinguisher")
        add_extinguisher_button.clicked.connect(lambda: self.open_new_window(AddExtinguisherWindow, self.connection))
        layout.addWidget(add_extinguisher_button)


        #Create "View Extinguisher" button
        view_extinguisher_button = QPushButton("View Extinguishers")
        view_extinguisher_button.clicked.connect(lambda: self.open_new_window(ViewExtinguishersWindow, self.connection))
        layout.addWidget(view_extinguisher_button)


        #Create "Movement Extinguisher" button
        movement_extinguisher_button = QPushButton("Movement Extinguisher")
        movement_extinguisher_button.clicked.connect(lambda: self.open_new_window(ExtinguisherMovement, self.connection))
        layout.addWidget(movement_extinguisher_button)


        #Create "Delete Extinguisher" button
        delete_extinguisher_button = QPushButton("Delete Extinguisher")
        delete_extinguisher_button.clicked.connect(lambda: self.open_new_window(DeleteExtinguisherWindow, self.connection))
        layout.addWidget(delete_extinguisher_button)


        #Create "Management Batches to Recharge" button
        create_batch_extinguisher_button = QPushButton("Management Batches to Recharge")
        create_batch_extinguisher_button.clicked.connect(lambda: self.open_new_window(BatchWindow, self.connection))
        layout.addWidget(create_batch_extinguisher_button)


        #Create "Back" button
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.show_page(self.main_page))
        layout.addWidget(back_button)


        page.setLayout(layout)
        return page



    def open_new_window(self, window_class, *args):
        self.new_window = window_class(*args)
        self.new_window.show()




    def show_page(self, page):
        self.stacked_widget.setCurrentWidget(page)



class AddExtinguisherWindow(QWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()



    def initUI(self):
        self.setWindowTitle("Add Extinguisher")
        layout = QVBoxLayout()


        label = QLabel("Register the information of the new extinguisher")
        layout.addWidget(label)


        #Id input
        id_label = QLabel("Fire Extinguisher ID") #Create the "Fire Extinguisher ID" label using "QLabel()"
        self.id_input = QLineEdit() #Declare the input as a text input using "QLineEdit()"
        self.id_input.setPlaceholderText("Enter fire extinguisher ID (numbers only)") #Set a placeholder to the id_input
        layout.addWidget(id_label) #Add the widget (id_label) to the layout
        layout.addWidget(self.id_input) #Add the widget (id_input) to the layout


        # Load capacity input
        capacity_label = QLabel("Capacity:") #Create the "Capacity" label using "Qlabel()"
        self.capacity_combo = QComboBox() #Declare input as a dropdown list of items using QComboBox()
        capacities = ["1 kg", "2.5 kg", "5 kg", "10 kg"] #Set the list of items to be used in "capacity_combo"
        self.capacity_combo.addItems(capacities) #Add the list of items to "capacity_combo"
        layout.addWidget(capacity_label) #Add the widget (capacity_label) to the layout
        layout.addWidget(self.capacity_combo) #Add the widget (capacity_combo) to the layout


        # Input for expiration date (date)
        expiry_date_label = QLabel("Expiration date:") #Create the "Expiration date" label using "QLabel"
        self.expiry_date_edit = QDateEdit() #Declare input as date using "QDateEdit"
        self.expiry_date_edit.setCalendarPopup(True) #Allow the use of a calendar window
        self.expiry_date_edit.setDate(QDate.currentDate())  # Default current date
        layout.addWidget(expiry_date_label)
        layout.addWidget(self.expiry_date_edit)


        # Input for expiration Hydraulic Test Date (date)
        expiry_ht_date_label = QLabel("Hydraulic Test Expiration Date:") #Create the "Hydraulic Test Expiration Date" Label using "QLabel()"
        self.expiry_ht_date_edit = QDateEdit()
        self.expiry_ht_date_edit.setCalendarPopup(True)
        self.expiry_ht_date_edit.setDate(QDate.currentDate())  # Default current date
        layout.addWidget(expiry_ht_date_label)
        layout.addWidget(self.expiry_ht_date_edit)


        # Button to register the extinguisher
        register_button = QPushButton("Register Fire Extinguisher") 
        register_button.clicked.connect(self.register_extinguisher)
        layout.addWidget(register_button)


        self.setLayout(layout)



    def register_extinguisher(self):
        """
        Take the entered data and execute the query that inserts the data into the database
        """

        # Get the entered values
        id_extinguisher = self.id_input.text() #Takes the value entered in the "id_input"
        capacity = self.capacity_combo.currentText() #Takes the value entered in the "capacity_combo"
        expiry_date = self.expiry_date_edit.date().toString("yyyy-MM-dd") #Takes the value entered in the "expiry_date_edit" input and converts it to a text string that the database can interpret correctly
        expiry_ht_date = self.expiry_ht_date_edit.date().toString("yyyy-MM-dd") #Takes the value entered in the "expiry_ht_date_edit" input and converts it to a text string that the database can interpret correctly


        # Validation for the id_extinguisher (should be numeric)
        if not id_extinguisher.isdigit():
            print("ID del matafuego debe ser numérico.")
            return


        cursor = None
        try:
            cursor = self.db_connection.cursor()
            query = """
            INSERT INTO extinguisher (id_extinguisher, admission_date, extinguisher_capacity, extinguisher_expiration_date, extinguisher_expiration_ht_date)
            VALUES (%s, CURDATE(), %s, %s, %s)
            """

            cursor.execute(query, (id_extinguisher, capacity, expiry_date, expiry_ht_date))
            self.db_connection.commit()
            print("Extinguisher registered")
        except Error as e:
            print(f"Error {e}")
        finally:
            if cursor:
                cursor.close()


class ViewExtinguishersWindow(QWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()


    def initUI(self):
        self.setWindowTitle("View Extinguishers")
        self.setGeometry(100, 100, 1000, 600)
        layout = QVBoxLayout()


        label = QLabel("These are all registered fire extinguishers") #Create the "" tag using ""
        layout.addWidget(label)


        # Create the table to display the data
        self.table = QTableWidget()
        layout.addWidget(self.table)


        self.load_data()


        back_button = QPushButton("Back")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)


        self.setLayout(layout)


    def load_data(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM extinguisher")
            rows = cursor.fetchall()


            # Configurar la tabla
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(rows[0]) if rows else 0)
            self.table.setHorizontalHeaderLabels([i[0] for i in cursor.description])


            # Poblar la tabla con los datos
            for row_idx, row in enumerate(rows):
                for col_idx, item in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))


            cursor.close()
        except Error as e:
            print(f"Error loading data: {e}")


class ExtinguisherMovement(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Extinguisher Movement")
        layout = QVBoxLayout()


        label = QLabel("Fire Extinguisher Delivery")
        layout.addWidget(label)


        #Input -- List of the avaliable extinguishers
        id_label = QLabel("Extinguisher ID")
        self.id_combo = QComboBox()
        extenguishers_avaliable = self.view_id_extinguisher()
        self.id_combo.addItems(extenguishers_avaliable)
        layout.addWidget(id_label)
        layout.addWidget(self.id_combo)


        #Input -- Ubication
        ubication_label = QLabel("Move to...")
        self.ubication_input = QLineEdit()
        self.ubication_input.setPlaceholderText("Type ubication")
        layout.addWidget(ubication_label)
        layout.addWidget(self.ubication_input)


        #Input -- Date
        deliver_date_label = QLabel("Deliver date")
        self.deliver_date_edit = QDateEdit()
        self.deliver_date_edit.setCalendarPopup(True)
        self.deliver_date_edit.setDate(QDate.currentDate()) #Current date by default
        layout.addWidget(deliver_date_label)
        layout.addWidget(self.deliver_date_edit)


        # Confirm movement
        confirm_button = QPushButton("Confirm Movement")
        confirm_button.clicked.connect(self.confirm_deliver)
        layout.addWidget(confirm_button)


        # Back Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)

        self.setLayout(layout)


    def confirm_deliver(self):
        id_extinguisher = self.id_combo.currentText()
        ubication = self.ubication_input.text()
        deliver_date = self.deliver_date_edit.date().toString("yyyy-MM-dd")


        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """
            UPDATE extinguisher_db.extinguisher
            SET last_ubication = extinguisher_ubication,
                extinguisher_ubication = %s,
                last_movement_date = %s
            WHERE id_extinguisher = %s
            """


            cursor.execute(query, (ubication, deliver_date, id_extinguisher))
            self.connection.commit()


            print("Extinguisher movement confirmed successfully")


        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()


    def view_id_extinguisher(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id_extinguisher FROM extinguisher_db.extinguisher;")
            rows = cursor.fetchall()
            cursor.close()


            id_list = [str(row[0]) for row in rows]
            return id_list
        except Error as e:
            print(f"Error: {e}")
            return []




class DeleteExtinguisherWindow(QWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Delete Extinguisher")
        layout = QVBoxLayout()

        label = QLabel("Esta es una nueva ventana")
        layout.addWidget(label)


        #Input -- List of the avaliable extinguishers
        id_label = QLabel("Extinguisher ID")
        self.id_combo = QComboBox()
        extenguishers_avaliable = self.view_id_extinguisher()
        self.id_combo.addItems(extenguishers_avaliable)
        layout.addWidget(id_label)
        layout.addWidget(self.id_combo)
       
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_extinguisher)
        layout.addWidget(delete_button)
   
        self.setLayout(layout)


    def delete_extinguisher(self):
        id_extinguisher = self.id_combo.currentText()
        try:
            cursor = self.db_connection.cursor()
            query = """
            DELETE FROM extinguisher_db.extinguisher WHERE id_extinguisher = %s;
            """
            cursor.execute(query, (id_extinguisher,))
            self.db_connection.commit()


            print(f"Extinguisher {id_extinguisher} eliminated")
           


        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:                                                        
                cursor.close()


    def view_id_extinguisher(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id_extinguisher FROM extinguisher_db.extinguisher;")
            rows = cursor.fetchall()
            cursor.close()


            id_list = [str(row[0]) for row in rows]
            return id_list
        except Error as e:
            print(f"Error: {e}")
            return []



class BatchWindow(QWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()
        


    def initUI(self):
        self.setWindowTitle("Batchs Management")
        layout = QVBoxLayout()


        self.stacked_widget = QStackedWidget()

        #Create Pages
        self.main_page = self.create_main_page()
        self.start_batch = self.create_start_batch_page()
        self.finish_batch = self.create_finish_batch_page()

        # Add pages to the QStackedWidget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.start_batch)
        self.stacked_widget.addWidget(self.finish_batch)

        #
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.stacked_widget.setCurrentWidget(self.main_page)


    def create_main_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Batchs Management")
        layout.addWidget(label)


        #
        start_batch_button = QPushButton("Start a Batch")
        start_batch_button.clicked.connect(lambda: self.show_page(self.start_batch))
        layout.addWidget(start_batch_button)

        #
        finish_batch_button = QPushButton("Finish a Batch")
        finish_batch_button.clicked.connect(lambda: self.show_page(self.finish_batch))
        finish_batch_button.clicked.connect(self.view_batches)
        layout.addWidget(finish_batch_button)

        #Create "Back" button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)


        page.setLayout(layout)
        return page
    
    def create_start_batch_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Start a Batch")
        layout.addWidget(label)

        # IDs List
        id_label = QLabel("Extinguisher ID")
        self.id_combo = QComboBox()
        extinguisher_avaliable = self.view_id_extinguisher()
        self.id_combo.addItems(extinguisher_avaliable)
        self.id_combo.currentIndexChanged.connect(self.update_extinguisher_info)
        layout.addWidget(id_label)
        layout.addWidget(self.id_combo)


        # Text Box Information
        self.extinguisher_info = QTextEdit()
        self.extinguisher_info.setReadOnly(True)
        layout.addWidget(self.extinguisher_info)

        #Add Button
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_to_batch)
        layout.addWidget(add_button)

        # List of Extinguisher
        self.batch_list = []
        self.batch_table = QTableWidget(0,3)
        self.batch_table.setHorizontalHeaderLabels(["ID","Capacity","Expiration Date"])
        layout.addWidget(self.batch_table)

        # Remove Button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_from_batch)
        layout.addWidget(remove_button)

        # Finish Button
        finish_button = QPushButton("Finish")
        finish_button.clicked.connect(self.set_batch)
        layout.addWidget(finish_button)

        #Back Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.show_page(self.main_page))
        layout.addWidget(back_button)


        page.setLayout(layout)
        return page

    def create_finish_batch_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Finish Batch")
        layout.addWidget(label)
        self.view_batches()

        #
        batch_label = QLabel("Batch ID")
        self.batch_combo = QComboBox()
        batches_avaliable = self.view_batches()
        self.batch_combo.addItems(batches_avaliable)
        layout.addWidget(self.batch_combo)
        layout.addWidget(batch_label)

        
        #
        recharge_date_label = QLabel("Recharge Date")
        self.recharge_date_edit = QDateEdit()
        self.recharge_date_edit.setCalendarPopup(True)
        self.recharge_date_edit.setDate(QDate.currentDate())
        layout.addWidget(recharge_date_label)
        layout.addWidget(self.recharge_date_edit)

        #
        finish_button = QPushButton("Finish Batch")
        finish_button.clicked.connect(self.complete_batch)
        layout.addWidget(finish_button)

        #Back Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.show_page(self.main_page))
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page



    def view_id_extinguisher(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id_extinguisher FROM extinguisher_db.extinguisher;")
            rows = cursor.fetchall()
            cursor.close()


            id_list = [str(row[0]) for row in rows]
            return id_list
        except Error as e:
            print(f"Error: {e}")
            return []
        
    def view_batches(self):
        batches = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id_batch FROM extinguisher_db.batch;")
            rows = cursor.fetchall()
            batches = [str(row[0]) for row in rows]
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()

        return batches

    
    def complete_batch(self):
        batch_id = self.batch_combo.currentText()
        expiry_date = self.recharge_date_edit.date().addYears(1).toString("yyyy-MM-dd")
        hydraulic_test_date = self.recharge_date_edit.date().addYears(4).toString("yyyy-MM-dd")

        cursor = None
        if len(batch_id) > 0:
            try:
                cursor =self.db_connection.cursor()

                #
                update_query = """
                UPDATE extinguisher_db.extinguisher
                SET extinguisher_expiration_date = %s, extinguisher_expiration_ht_date = %s
                WHERE id_extinguisher IN (
                    SELECT id_extinguisher
                    FROM extinguisher_db.extinguisher_in_batch
                    WHERE id_batch = %s
                );
                """

                cursor.execute(update_query, (expiry_date,hydraulic_test_date,batch_id))


                #
                delete_batch_extinguisher_query = """
                DELETE FROM extinguisher_db.extinguisher_in_batch WHERE id_batch = %s;
                """

                cursor.execute(delete_batch_extinguisher_query, (batch_id,))

                #
                delete_batch_query = """
                DELETE FROM extinguisher_db.batch WHERE id_batch = %s;
                """

                cursor.execute(delete_batch_query, (batch_id,))

                self.db_connection.commit()

                print(f"Batch N°{batch_id} completed")

            except Error as e:
                print(f"Error: {e}")

            finally:
                if cursor:
                    cursor.close()


    
    def update_extinguisher_info(self):
        id_extinguisher = self.id_combo.currentText()

        try:
            cursor = self.db_connection.cursor()
            query= """
            SELECT 
                id_extinguisher,
                extinguisher_capacity,
                extinguisher_expiration_date
            FROM
                extinguisher_db.extinguisher
            WHERE
                id_extinguisher = %s;
            """
            cursor.execute(query, (id_extinguisher,))
            result = cursor.fetchone()
            if result:
                self.extinguisher_info.setText(f"ID: {result[0]}\nCapacity: {result[1]}\nExpiration Date: {result[2]}")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()


    def add_to_batch(self):
        id_extinguisher = int(self.id_combo.currentText())

        if id_extinguisher not in [item[0] for item in self.batch_list]:
            try:
                cursor = self.db_connection.cursor()
                query= """
                    SELECT 
                        id_extinguisher,
                        extinguisher_capacity,
                        extinguisher_expiration_date
                    FROM
                        extinguisher_db.extinguisher
                    WHERE
                        id_extinguisher = %s;
                    """
                cursor.execute(query, (id_extinguisher,))
                result = cursor.fetchone()
                if result:
                    self.batch_list.append(result)
                    self.update_batch_table()
            except Error as e:
                print(f"Error: {e}")
            finally:
                if cursor:
                    cursor.close()

    def remove_from_batch(self):
        id_extinguisher = int(self.id_combo.currentText())
        self.batch_list = [item for item in self.batch_list if item[0] != id_extinguisher]
        self.update_batch_table()
        

    
    def update_batch_table(self):
        self.batch_table.setRowCount(len(self.batch_list))
        for row_index, extinguisher in enumerate(self.batch_list):
            for col_index, value in enumerate(extinguisher):
                self.batch_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    
    def set_batch(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO extinguisher_db.batch (creation_date) VALUES (CURDATE())")
            batch_id = cursor.lastrowid

            for extinguisher in self.batch_list:
                cursor.execute("INSERT INTO extinguisher_db.extinguisher_in_batch (id_extinguisher, id_batch) VALUES (%s, %s)", (extinguisher[0], batch_id))
                               
            self.db_connection.commit()
            print(f"Batch {batch_id} sucessfully created")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            


    def show_page(self, page):
        self.stacked_widget.setCurrentWidget(page)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
