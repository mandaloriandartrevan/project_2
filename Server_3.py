import socket  
import threading  
import time  
from datetime import datetime  # Импортируем модуль datetime  

clients = []  

def handle_client(client_socket, address):  
    """Обрабатывает подключение клиента."""  
    connection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущее время подключения  
    print(f"Client connected: {address} at {connection_time}")  
    clients.append((address, connection_time))  # Добавляем клиента и время подключения в список  

    while True:  
        try:  
            # Получаем данные от клиента  
            data = client_socket.recv(1024)  
            if not data:  
                break  
            
            # Если полученные данные не пустые, сохраняем их как изображение  
            with open(".jpg", "wb") as image_file:  
                image_file.write(data)  
            
            print(f"Screenshot saved from {address}")  
        except Exception as e:  
            print(f"Error: {e}")  
            break  

    print(f"Client disconnected: {address}")  
    clients.remove((address, connection_time))  # Удаляем клиента из списка  
    client_socket.close()  

def start_server():  
    """Запускает сервер."""  
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server.bind(("localhost", 8888))  # Замените на нужный адрес и порт  
    server.listen(5)  
    print("Server started, waiting for connections...")  

    while True:  
        client_socket, address = server.accept()  
        threading.Thread(target=handle_client, args=(client_socket, address)).start()  

def print_connected_clients():  
    """Выводит список всех подключенных клиентов."""  
    while True:  
        if clients:  
            print("\nConnected clients:")  
            for client in clients:  
                print(f"Domain/Computer: {client[0]}, IP: {client[1]}, Connection Time: {client[2]}")  
        else:  
            print("\nNo connected clients.")  
        time.sleep(10)  # Обновление каждые 10 секунд  

if __name__ == "__main__":  
    server_thread = threading.Thread(target=start_server)  
    server_thread.start()  

    print_connected_clients()  # Запускаем вывод списка клиентов