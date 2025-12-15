import socket
import threading
import time

# адреса та порт сервера
HOST = '127.0.0.1'
PORT = 5000

# максимальна кількість повідомлень для одного клієнта
MAX_MESSAGES = 5


def handle_client(client_socket, client_address):
    """
    Обслуговування одного клієнта.
    Кожен клієнт працює в окремому потоці.
    """
    print(f"Клієнт підключився: {client_address}")

    # лічильник
    message_id = 0

    # таймаут, щоб сервер не зависав при відсутності відповіді
    client_socket.settimeout(5)

    try:
        # надсилаємо обмежену кількість повідомлень
        while message_id < MAX_MESSAGES:

            # формуємо повідомлення з унікальним ID
            message = f"MSG:{message_id}"
            delivered = False

            # повторюємо відправку, поки не отримаємо ACK
            while not delivered:
                try:
                    # надсилаємо повідомлення клієнту
                    client_socket.send(message.encode())
                    print(f"Відправлено {message} клієнту {client_address}")

                    # очікуємо підтвердження доставки
                    response = client_socket.recv(1024).decode()

                    # перевірка підтвердження
                    if response == f"ACK:{message_id}":
                        print(f"Підтверджено отримання {message}")
                        delivered = True
                        message_id += 1
                    else:
                        print("Невірне підтвердження, повторна відправка")

                except socket.timeout:
                    print("Таймаут. Повторна відправка повідомлення")

            # пауза
            time.sleep(1)

    except (ConnectionResetError, BrokenPipeError):
        print(f"Клієнт {client_address} відключився")

    finally:
        # закриваємо з’єднання з клієнтом
        client_socket.close()
        print(f"З’єднання з {client_address} завершено")


def start_server():
    """
    Запуск сервера та очікування клієнтів
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Сервер запущено, очікування клієнтів...")

    while True:
        # приймаємо нового клієнта
        client_socket, client_address = server_socket.accept()

        # запускаємо окремий потік для клієнта
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True
        )
        client_thread.start()


if __name__ == "__main__":
    start_server()


# cd D:\exam
# python server.py