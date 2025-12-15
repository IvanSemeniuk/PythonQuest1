import socket
import time

# адреса та порт сервера
HOST = '127.0.0.1'
PORT = 5000


def start_client():
    """
    Функція запуску клієнта
    """
    # створюємо TCP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # підключаємося до сервера
    client_socket.connect((HOST, PORT))
    print("Підключено до сервера")

    try:
        while True:
            # отримуємо повідомлення від сервера
            data = client_socket.recv(1024).decode()

            # якщо сервер нічого не надіслав — виходимо
            if not data:
                break

            print(f"Отримано повідомлення: {data}")

            # якщо повідомлення має формат MSG:id
            if data.startswith("MSG:"):
                # витягуємо ID повідомлення
                message_id = data.split(":")[1]

                # імітація обробки повідомлення
                time.sleep(0.5)

                # формуємо підтвердження доставки
                ack = f"ACK:{message_id}"

                # надсилаємо підтвердження серверу
                client_socket.send(ack.encode())
                print(f"Надіслано підтвердження: {ack}")

    except ConnectionResetError:
        print("З’єднання з сервером втрачено")

    finally:
        # закриваємо сокет
        client_socket.close()
        print("Клієнт завершив роботу")


if __name__ == "__main__":
    start_client()


# cd D:\exam
# python client.py