from dao.user_dao import UserDAO


nombre = input("Nombre: ")
password = input("Password: ")
UserDAO.login(nombre, password)

