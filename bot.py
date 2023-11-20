import json
from tkinter import Tk, Label, Entry, Button, Listbox

from discord_webhook import DiscordWebhook

class DiscordWebhookApp:
    def __init__(self, master):
        self.master = master
        master.title("Discord Webhook App")

        # Entry for message content
        self.label = Label(master, text="Message Content:")
        self.label.pack()

        self.content_entry = Entry(master)
        self.content_entry.pack()

        # Entry for webhook URL
        self.label = Label(master, text="Webhook URL:")
        self.label.pack()

        self.webhook_entry = Entry(master)
        self.webhook_entry.pack()

        # Button to send message
        self.send_button = Button(master, text="Send Message", command=self.send_message)
        self.send_button.pack()

        # Listbox to display webhooks
        self.webhook_listbox = Listbox(master)
        self.webhook_listbox.pack()

        # Button to add webhook
        self.add_button = Button(master, text="Add Webhook", command=self.add_webhook)
        self.add_button.pack()

        # Button to remove selected webhook
        self.remove_button = Button(master, text="Remove Webhook", command=self.remove_webhook)
        self.remove_button.pack()

        # Load existing webhooks
        self.load_webhooks()

    def send_message(self):
        content = self.content_entry.get()
        webhook_url = self.webhook_entry.get()
        if content and webhook_url:
            print(f"Sending message: {content} to webhook: {webhook_url}")
            webhook = DiscordWebhook(url=webhook_url, content=content)
            webhook.execute()

    def add_webhook(self):
        webhook_url = self.webhook_entry.get()
        if webhook_url:
            print(f"Adding webhook: {webhook_url}")
            self.webhook_listbox.insert("end", webhook_url)
            self.save_webhooks()

    def remove_webhook(self):
        selected_index = self.webhook_listbox.curselection()
        if selected_index:
            webhook_url = self.webhook_listbox.get(selected_index)
            print(f"Removing webhook: {webhook_url}")
            self.webhook_listbox.delete(selected_index)
            self.save_webhooks()

    def load_webhooks(self):
        try:
            with open('config.json', 'r') as f:
                data = json.load(f)
                webhooks = data.get('webhooks', [])
                for webhook_url in webhooks:
                    print(f"Loading webhook: {webhook_url}")
                    self.webhook_listbox.insert("end", webhook_url)
        except FileNotFoundError:
            print("Config file not found.")

    def save_webhooks(self):
        webhooks = list(self.webhook_listbox.get(0, "end"))
        data = {'webhooks': webhooks}
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved webhooks: {webhooks}")

def main():
    root = Tk()
    app = DiscordWebhookApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
