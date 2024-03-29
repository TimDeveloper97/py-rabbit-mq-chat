# import tkinter as tk
# import pika
# import threading


# class ChatApplication(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Chat Application")
#         self.geometry("600x400")

#         # GUI components
#         self.username_label = tk.Label(self, text="Username:")
#         self.username_entry = tk.Entry(self)
#         self.room_label = tk.Label(self, text="Room:")
#         self.room_entry = tk.Entry(self)
#         self.message_label = tk.Label(self, text="Message:")
#         self.message_entry = tk.Entry(self)
#         self.send_button = tk.Button(self, text="Send", command=self.send_message)
#         self.stop_button = tk.Button(self, text="Disconnect", command=self.stop_chat)
#         self.message_display = tk.Text(self, height=20, width=50)

#         # Grid layout
#         self.username_label.grid(row=0, column=0)
#         self.username_entry.grid(row=0, column=1)
#         self.room_label.grid(row=1, column=0)
#         self.room_entry.grid(row=1, column=1)
#         self.message_label.grid(row=2, column=0)
#         self.message_entry.grid(row=2, column=1)
#         self.send_button.grid(row=2, column=2)
#         self.stop_button.grid(row=2, column=3)
#         self.message_display.grid(row=3, column=0, columnspan=4)

#         # RabbitMQ connection
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host="localhost")
#         )
#         self.channel = self.connection.channel()
#         self.channel.exchange_declare(exchange="room", exchange_type="topic")

#         # Start receiving messages in a separate thread
#         receive_thread = threading.Thread(target=self.receive_messages)
#         receive_thread.daemon = True
#         receive_thread.start()

#         # Bind enter key press event to message entry
#         self.message_entry.bind("<Return>", lambda event: self.send_message())

#     def send_message(self):
#         username = self.username_entry.get()
#         room = self.room_entry.get()
#         message = self.message_entry.get()
#         if username.strip() and room.strip() and message.strip():
#             message_body = f"{username}: {message}"
#             self.channel.basic_publish(
#                 exchange="room", routing_key=room, body=message_body
#             )
#             self.message_display.insert(tk.END, f"{message_body}\n")
#             self.message_display.see(tk.END)  # Scroll to the end
#             self.message_entry.delete(0, tk.END)

#     def stop_chat(self):
#         self.connection.close()

#     def receive_messages(self):
#         result = self.channel.queue_declare(queue="", exclusive=True)
#         queue_name = result.method.queue
#         self.channel.queue_bind(exchange="room", queue=queue_name, routing_key="#")

#         def callback(ch, method, properties, body):
#             room = method.routing_key
#             message = body.decode()
#             sender, message_content = message.split(": ", 1)
#             if sender != self.username_entry.get() and room == self.room_entry.get():
#                 # Print message to console
#                 print(f"{sender}: {message_content}")

#                 # Insert message to message display
#                 self.message_display.insert(tk.END, f"{message}\n")
#                 self.message_display.see(tk.END)  # Scroll to the end

#         self.channel.basic_consume(
#             queue=queue_name, on_message_callback=callback, auto_ack=True
#         )
#         self.channel.start_consuming()

#     def on_closing(self):
#         if self.connection.is_open:
#             self.connection.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = ChatApplication()
#     app.protocol("WM_DELETE_WINDOW", app.on_closing)
#     app.mainloop()

import tkinter as tk
import pika
import threading

class ChatApplication(tk.Tk):
    def __init__(self, root, username, room):
        super().__init__()
        self.title("Chat Application")
        self.geometry("600x400")

        self.login = root
        # GUI components
        self.username_label = tk.Label(self, text="Username:")
        self.username_entry = tk.Entry(self)
        self.room_label = tk.Label(self, text="Room:")
        self.room_entry = tk.Entry(self)
        self.message_label = tk.Label(self, text="Message:")
        self.message_entry = tk.Entry(self)
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.message_display = tk.Text(self, height=20, width=50)
        self.disconnect_button = tk.Button(self, text="Disconnect", command=self.disconnect)

        # Grid layout
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.room_label.grid(row=1, column=0)
        self.room_entry.grid(row=1, column=1)
        self.message_label.grid(row=2, column=0)
        self.message_entry.grid(row=2, column=1)
        self.send_button.grid(row=2, column=2)
        self.disconnect_button.grid(row=2, column=3)
        self.message_display.grid(row=3, column=0, columnspan=3)

        # Set value
        self.username_entry.insert(0, username)
        self.room_entry.insert(0, room)

        # RabbitMQ connection
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="room", exchange_type="topic")

        # Start receiving messages in a separate thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        # Bind enter key press event to message entry
        self.message_entry.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        username = self.username_entry.get()
        room = self.room_entry.get()
        message = self.message_entry.get()
        if username.strip() and room.strip() and message.strip():
            message_body = f"{username}: {message}"
            self.channel.basic_publish(
                exchange="room", routing_key=room, body=message_body
            )
            self.message_display.insert(tk.END, f"{message_body}\n")
            self.message_display.see(tk.END)  # Scroll to the end
            self.message_entry.delete(0, tk.END)
    
    def disconnect(self):
        self.connection.close()
        self.destroy()

    def receive_messages(self):
        result = self.channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange="room", queue=queue_name, routing_key="#")

        def callback(ch, method, properties, body):
            room = method.routing_key
            message = body.decode()
            sender, message_content = message.split(": ", 1)
            if sender != self.username_entry.get() and room == self.room_entry.get():
                # Print message to console
                print(f"{sender}: {message_content}")

                # Insert message to message display
                self.message_display.insert(tk.END, f"{message}\n")
                self.message_display.see(tk.END)  # Scroll to the end

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

    def on_closing(self):
        self.connection.close()
        self.destroy()


if __name__ == "__main__":
    app = ChatApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
