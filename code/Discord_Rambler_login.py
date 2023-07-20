import email
import imaplib
import quopri
import webbrowser
import tkinter as tk
import tkinter
import pyperclip
import re
import socks
import socket

from bs4 import BeautifulSoup
from tkinter import ttk, messagebox
from imaplib import IMAP4_SSL
from constants import PROXY_URL
from proxy_info import ProxyInfo

def enter_via_proxy(proxy_info: ProxyInfo, server_address: str):
    proxy_info = ProxyInfo.parse_proxy_url(proxy_url=PROXY_URL)
    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, 
        proxy_info.hostname, 
        proxy_info.port, 
        username=proxy_info.username, 
        password=proxy_info.password)
    socket.socket = socks.socksocket
    imap_server = IMAP4_SSL(server_address)
    return imap_server

def link_authorization():

    proxy_info = ProxyInfo.parse_proxy_url(PROXY_URL)

    global link, imap_server
    print("\n TRYING TO GET VERIFICATION LINK...")
    try:        
        imap_server = enter_via_proxy(proxy_info, 'imap.rambler.ru')
        imap_server.login(email_entry.get().strip(), password_entry.get().strip())
        imap_server.select('Inbox')

        # Search for emails with the subject 'Verify Email Address for Discord'
        status, messages = imap_server.search(None, "ALL")

        # Get the IDs of the emails that match the search criteria
        msg_ids = messages[0].split()

        if msg_ids != []:
            for msg_id in msg_ids:
                # Fetch the contents of the email with the matching subject
                status, message = imap_server.fetch(msg_ids[-1], '(RFC822)')
                for response in message:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        for msg in msg.get_payload():
                            body = msg.get_payload()

                            decoded_body = quopri.decodestring(body).decode()

                            # Remove = from the body
                            decoded_body = decoded_body.replace("=\n", '')

                            soup = BeautifulSoup(decoded_body, 'html.parser')
                            
                            verify_link_text = soup.find(text=re.compile(r'Verify Login'))

                            link = verify_link_text.split('Verify Login: ')[1].split()[0]
                                                        
                            print('\n GOT VERIFICATION LINK ✅')

                            # Mark the email for deletion
                            # imap_server.store(msg_id, '+FLAGS', '\\Deleted')

                            # imap_server.close()
                            # imap_server.logout()

                            return link

    except Exception as link_authorization_mail:
        print("\nError in link authorization -", link_authorization_mail)
        messagebox.showerror("Error", "Something went wrong, check terminal!")

    else:
        print("\n No email with the specified subject found.")
        messagebox.showinfo("Error", "No email found, please retry!")


    # Close the mailbox and log out of the email account

def show_popup(link):
    popup_window = tk.Toplevel(window)
    popup_window.title("Login Link")
    popup_window.configure(bg='#333333')
    popup_window.geometry("300x150")
    popup_window.resizable(False, False)

    login_label = tk.Label(popup_window, text="Login Link:" ,bg='#333333', fg="#FF3399")
    login_label.pack()

    login_text = tk.Text(popup_window, width=30, height=3)
    login_text.insert(tk.END, link)
    login_text.configure(state='disabled')
    login_text.pack(pady=10)

    def copy_link():
        pyperclip.copy(link)
        messagebox.showinfo("Link Copied", "The link has been copied to the clipboard.")

    copy_button = tk.Button(popup_window, text="Copy Link", bg="#FF3399", fg="#FFFFFF", font=("Arial", 10),
                            command=copy_link)
    copy_button.pack()

def get_link():
    link = link_authorization()

    if link:
        show_popup(link)

window = tkinter.Tk()
window.title("Discord Get Verification Link by @maked0n1an")
window.geometry('500x500')
window.configure(bg='#333333')
window.resizable(False, False)
frame = tkinter.Frame(bg='#333333')

# Creating widgets
login_label = tkinter.Label(
    frame, text="Discord Bot", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tkinter.Label(
    frame, text="Email", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
email_entry = tkinter.Entry(frame, font=("Arial", 16))
password_entry = tkinter.Entry(frame, font=("Arial", 16))
password_label = tkinter.Label(
    frame, text="Password  ", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tkinter.Button(
    frame, text="  Get link  ", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=get_link)

# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
email_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30,padx=50)

frame.pack()

window.mainloop()
