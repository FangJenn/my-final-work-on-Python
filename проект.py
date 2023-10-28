

# Импортируем необходимые модули для работы с GUI и БД
from tkinter import Tk, Label, Entry, Button, messagebox, ttk
import sqlite3



# Создаем класс для работы со списком сотрудников
class EmployeesList:
    def __init__(self):
        self.connection = sqlite3.connect('employees.db')  # Подключаемся к базе данных
        self.cursor = self.connection.cursor()  # Создаем курсор для выполнения SQL-запросов


    def create_table(self):
        # Создаем таблицу сотрудников, если она не существует
        query = """CREATE TABLE IF NOT EXISTS employees
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   full_name TEXT,
                   phone TEXT,
                   email TEXT,
                   salary FLOAT)"""
        self.cursor.execute(query)
        self.connection.commit()


    def add_employee(self):
        # Получаем данные о новом сотруднике из полей ввода
        full_name = self.full_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        salary = self.salary_entry.get()


        if full_name and phone and email and salary:  # Проверяем, что все поля заполнены
            # Вставляем нового сотрудника в таблицу
            query = """INSERT INTO employees (full_name, phone, email, salary)
                       VALUES (?, ?, ?, ?)"""
            self.cursor.execute(query, (full_name, phone, email, salary))
            self.connection.commit()
            messagebox.showinfo("Success", "Employee has been added successfully.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")


    def delete_employee(self):
        # Получаем ID удаляемого сотрудника
        employee_id = self.selected_employee_id.get()

        if employee_id:  # Проверяем, что сотрудник выбран
            # Удаляем сотрудника из таблицы по его ID
            query = "DELETE FROM employees WHERE id = ?"
            self.cursor.execute(query, (employee_id,))
            self.connection.commit()
            messagebox.showinfo("Success", "Employee has been deleted successfully.")
        else:
            messagebox.showerror("Error", "Please select an employee.")


    def search_employee(self):
        # Получаем ФИО сотрудника, по которому будет осуществляться поиск
        search_name = self.search_entry.get()

        # Ищем сотрудников в таблице по ФИО
        query = "SELECT * FROM employees WHERE full_name LIKE ?"
        self.cursor.execute(query, ('%' + search_name + '%',))
        employees = self.cursor.fetchall()

        # Очищаем виджет Treeview перед выводом новой информации
        self.treeview.delete(*self.treeview.get_children())

        if employees:
            for employee in employees:
                # Добавляем найденных сотрудников в виджет Treeview
                self.treeview.insert('', 'end', text=employee[0], values=(employee[1], employee[2], employee[3], employee[4]))
        else:
            messagebox.showinfo("No Results", "No employees found.")


    def update_employee(self):
        # Получаем ID сотрудника, который будет обновляться
        employee_id = self.selected_employee_id.get()

        if employee_id:  # Проверяем, что сотрудник выбран
            # Получаем новые данные о сотруднике из полей ввода
            full_name = self.full_name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            salary = self.salary_entry.get()

            if full_name and phone and email and salary:  # Проверяем, что все поля заполнены
                # Обновляем информацию о сотруднике в таблице
                query = """UPDATE employees
                           SET full_name = ?, phone = ?, email = ?, salary = ?
                           WHERE id = ?"""
                self.cursor.execute(query, (full_name, phone, email, salary, employee_id))
                self.connection.commit()
                messagebox.showinfo("Success", "Employee has been updated successfully.")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")
        else:
            messagebox.showerror("Error", "Please select an employee.")

    def create_gui(self):
        # Создаем графический интерфейс
        root = Tk()
        root.title("Employees List")
        root.geometry("600x400")

        # Создаем метки и поля ввода для каждого атрибута сотрудника
        full_name_label = Label(root, text="Full Name:")
        full_name_label.pack()
        self.full_name_entry = Entry(root)
        self.full_name_entry.pack()

        phone_label = Label(root, text="Phone:")
        phone_label.pack()
        self.phone_entry = Entry(root)
        self.phone_entry.pack()

        email_label = Label(root, text="Email:")
        email_label.pack()
        self.email_entry = Entry(root)
        self.email_entry.pack()

        salary_label = Label(root, text="Salary:")
        salary_label.pack()
        self.salary_entry = Entry(root)
        self.salary_entry.pack()

        # Создаем кнопку для добавления сотрудника
        add_button = Button(root, text="Add Employee", command=self.add_employee)
        add_button.pack()

        # Создаем кнопку для удаления сотрудника
        delete_button = Button(root, text="Delete Employee", command=self.delete_employee)
        delete_button.pack()

        # Создаем метку и поле ввода для поиска сотрудника по ФИО
        search_label = Label(root, text="Search by Name:")
        search_label.pack()
        self.search_entry = Entry(root)
        self.search_entry.pack()

        # Создаем кнопку для поиска сотрудника
        search_button = Button(root, text="Search", command=self.search_employee)
        search_button.pack()

        # Создаем кнопку для обновления информации о сотруднике
        update_button = Button(root, text="Update Employee", command=self.update_employee)
        update_button.pack()

        # Создаем виджет Treeview для отображения списка сотрудников
        self.treeview = ttk.Treeview(root, columns=("full_name", "phone", "email", "salary"), show="headings")
        self.treeview.heading("full_name", text="Full Name")
        self.treeview.heading("phone", text="Phone")
        self.treeview.heading("email", text="Email")
        self.treeview.heading("salary", text="Salary")
        self.treeview.pack()

        # Получаем список всех сотрудников из таблицы и добавляем их в виджет Treeview
        query = "SELECT * FROM employees"
        self.cursor.execute(query)
        employees = self.cursor.fetchall()

        for employee in employees:
            self.treeview.insert('', 'end', text=employee[0], values=(employee[1], employee[2], employee[3], employee[4]))

        # Обработка выделения сотрудника в виджете Treeview
        def select_employee(event):
            selected_item = self.treeview.focus()
            selected_employee = self.treeview.item(selected_item)
            self.selected_employee_id.set(selected_employee["text"])
            selected_employee_data = selected_employee["values"]
            self.full_name_entry.delete(0, 'end')
            self.full_name_entry.insert(0, selected_employee_data[0])
            self.phone_entry.delete(0, 'end')
            self.phone_entry.insert(0, selected_employee_data[1])
            self.email_entry.delete(0, 'end')
            self.email_entry.insert(0, selected_employee_data[2])
            self.salary_entry.delete(0, 'end')
            self.salary_entry.insert(0, selected_employee_data[3])

        self.treeview.bind('<ButtonRelease-1>', select_employee)

        # Переменная для хранения ID выбранного сотрудника
        self.selected_employee_id = Tk().StringVar()

        root.mainloop()


if __name__ == '__main__':
    employees_list = EmployeesList()
    employees_list.create_table()
    employees_list.create_gui()