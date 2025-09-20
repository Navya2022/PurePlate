import mysql.connector
import tkinter as tk
from tkinter import ttk,simpledialog,messagebox,Listbox,Scrollbar
import customtkinter
import csv
import time
from ttkbootstrap.toast import ToastNotification
import os
from datetime import datetime, timedelta
from datetime import date
from PIL import Image, ImageTk

user = ''
mycon = mysql.connector.connect(user="root",host="localhost",database="pureplate",password="determination")
cursor = mycon.cursor()
k = 0
def reset_orders_if_needed(cursor):
    current_date = datetime.now().date()

    cursor.execute("SELECT last_reset_date FROM Reset_Date;")
    result = cursor.fetchone()
    
    if result and result[0]:  # Check if there is a result and it's not None
        last_reset_date = result[0]

        if current_date != last_reset_date:
            cursor.execute("UPDATE delivery SET del_orders_taken = 0;")
            
            # Update the last reset date in the Reset_Date table
            cursor.execute("UPDATE Reset_Date SET last_reset_date = %s;", (current_date,))
            print(type(current_date))
            print("Updated last reset date to:", current_date)
            print('j')
        else:
            print("No reset needed. Last reset date is:", last_reset_date)
    else:
        # No input for Reset_date
        cursor.execute("INSERT INTO Reset_Date (last_reset_date) VALUES (%s);", (current_date,))

reset_orders_if_needed(cursor)
mycon.commit()

s = ''' select count(*) from contributors;'''
cursor.execute(s)
contributor = cursor.fetchall()[0][0]

s = ''' select count(*) from receiver;'''
cursor.execute(s)
receiver = cursor.fetchall()[0][0]+1
today = date.today()

def contributor_signup():
    global contributor  
    
    #window initialization
    root = tk.Toplevel()
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    root.geometry(f'{window_width}x{window_height}')
    
    # Scrollable layout
    main_frame = customtkinter.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)

    image = tk.PhotoImage(file="orange_bg.png")  
    
    canvas = customtkinter.CTkCanvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image = image)
    canvas.image = image                                     

    scrollbar = customtkinter.CTkScrollbar(canvas, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrolled_frame = customtkinter.CTkFrame(canvas,fg_color="#FFFFFF",
        border_color="#FFB6C1",
        border_width=2)
    scrolled_frame.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrolled_frame, anchor="nw")
    
    label = customtkinter.CTkLabel(scrolled_frame, text="Enter Name" )
    label.pack(pady=10)
    my_text = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                       height=37, fg_color="#D3D3D3")
    my_text.pack(pady=10, padx=20)

    label1 = customtkinter.CTkLabel(scrolled_frame, text="Enter Phone No")
    label1.pack(pady=10)
    my_text1 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text1.pack(pady=10, padx=20)

    label2 = customtkinter.CTkLabel(scrolled_frame, text="Enter Contributor's Username")
    label2.pack(pady=10)
    my_text2 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text2.pack(pady=10, padx=20)

    label3 = customtkinter.CTkLabel(scrolled_frame, text="Enter Contributor's Password")
    label3.pack(pady=10)
    my_text3 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text3.pack(pady=10, padx=20)

    label4 = customtkinter.CTkLabel(scrolled_frame, text="Enter City")
    label4.pack(pady=10)
    my_text4 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text4.pack(pady=10, padx=20)

    label5 = customtkinter.CTkLabel(scrolled_frame, text="Enter Locality")
    label5.pack(pady=10)
    my_text5 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text5.pack(pady=10, padx=20)

    def on_next():
        print(contributor)
        j=0
        CID = 'C'+str(contributor)
        text = my_text.get('0.0','end').strip()
        text1 = my_text1.get('0.0','end').strip()
        text2 = my_text2.get('0.0','end').strip()
        text3 = my_text3.get('0.0','end').strip()
        text4 = my_text4.get('0.0','end').strip()
        text5 = my_text5.get('0.0','end').strip()

        if text1.isdigit()==False or len(text1)!=10:
            Toast("Enter valid phno")
            r=2
        
        l =[text,text1,text2,text3,text4,text5]
        for i in l:
            if i =='\n':
                j=1
        if j==1 or j==2:
            root.destroy()
            contributor_signup()
            
        sq = '''INSERT INTO Contributors (CID, CNAME, PHONE_NO, C_username, C_password,C_CITY,C_locality)
                VALUES ('%s', '%s', %s, '%s', '%s','%s','%s')'''%(CID, text, text1, text2, text3,text4,text5) 
        cursor.execute(sq)
        mycon.commit()

        my_text.delete('0.0', 'end')
        my_text1.delete('0.0', 'end')
        my_text2.delete('0.0', 'end')
        my_text3.delete('0.0', 'end')
        my_text4.delete('0.0', 'end')
        my_text5.delete('0.0', 'end')

        root.destroy()

    contributor+= 1                 

    next_button = customtkinter.CTkButton(scrolled_frame,
                                          text="Next", corner_radius=32, fg_color="#FF7F00", 
                hover_color="#D76B30", border_color="#FF9E40", 
                border_width=2, command=on_next)
    next_button.pack(pady=20)

    root.mainloop()

def receiver_signup():
    global receiver
    j=0
    #window initialization
    root = tk.Toplevel()
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    root.geometry(f'{window_width}x{window_height}')
    
    # Scrollable layout
    main_frame = customtkinter.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)

    image = tk.PhotoImage(file="orange_bg.png")  
    
    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image = image)
    canvas.image = image

    scrollbar = customtkinter.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrolled_frame = customtkinter.CTkFrame(canvas, fg_color="#FFFFFF",
        border_color="#FFB6C1",
        border_width=2.5)
    scrolled_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrolled_frame, anchor="nw")

    label = customtkinter.CTkLabel(scrolled_frame, text="Enter Name" )
    label.pack(pady=10)
    my_text = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                       height=37, fg_color="#D3D3D3")
    my_text.pack(pady=10, padx=20)

    label1 = customtkinter.CTkLabel(scrolled_frame, text="Enter Phone No")
    label1.pack(pady=10)
    my_text1 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text1.pack(pady=10, padx=20)

    label2 = customtkinter.CTkLabel(scrolled_frame, text="Enter Receiver's Username")
    label2.pack(pady=10)
    my_text2 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text2.pack(pady=10, padx=20)

    label3 = customtkinter.CTkLabel(scrolled_frame, text="Enter Receiver's Password")
    label3.pack(pady=10)
    my_text3 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text3.pack(pady=10, padx=20)
    
    label4 = customtkinter.CTkLabel(scrolled_frame, text="Enter Receiver's City")
    label4.pack(pady=10)
    my_text4 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text4.pack(pady=10, padx=20)

    label5 = customtkinter.CTkLabel(scrolled_frame, text="Locality")
    label5.pack(pady=10)
    my_text5 = customtkinter.CTkTextbox(scrolled_frame, width=550,
                                        height=37, fg_color="#D3D3D3")
    my_text5.pack(pady=10, padx=20)

    def on_next():
        j=0
        RID = 'R'+str(receiver)
        text = my_text.get('0.0','end').strip()
        text1 = my_text1.get('0.0','end').strip()
        text2 = my_text2.get('0.0','end').strip()
        text3 = my_text3.get('0.0','end').strip()
        text4 = my_text4.get('0.0','end').strip()
        text5 = my_text5.get('0.0','end').strip()

        if text1.isdigit()==False or len(text1)!=10:
            Toast("Enter valid phno")
            j=2
        
        l1 =[text,text1,text2,text3,text4]
        for i in l1:
            if i =='\n':
                j=1
        if j==1 or j==2:
            root.destroy()
            receiver_signup()
            
        sq = '''INSERT INTO receiver (RID, RNAME, PHONE_NO, R_username,R_password, R_CITY, R_LOCALITY)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s')'''%(RID, text, text1, text2, text3, text4,text5)
        cursor.execute(sq)
        mycon.commit()

        my_text.delete('0.0', 'end')
        my_text1.delete('0.0', 'end')
        my_text2.delete('0.0', 'end')
        my_text3.delete('0.0', 'end')
        my_text4.delete('0.0', 'end')
        my_text5.delete('0.0', 'end')
        root.destroy()                           

    next_button = customtkinter.CTkButton(scrolled_frame,
                                          text="Next",corner_radius=32, fg_color="#FF7F00", 
                hover_color="#FF9E40", border_color="#CC5500", 
                border_width=2, command=on_next)
    next_button.pack(pady=20)    

    root.mainloop()

def choice():
    global r1
    r1 = tk.Toplevel()
    r.destroy
    r1.title("SIGNUP WINDOW")

    window_width = r1.winfo_screenwidth()
    window_height = r1.winfo_screenheight()
    r1.geometry(f'{window_width}x{window_height}')
    image = tk.PhotoImage(file="white_orange_bg.png")  
    canvas = tk.Canvas(r1,width=window_width, height=window_height)
    canvas.pack()
    canvas.create_image(window_width//2, window_height//2,
                        anchor="center", image=image)

    img_one = tk.PhotoImage(file = "ICON donating.png")
    img_two = tk.PhotoImage(file = "ICON receiving.png")
    
    button1 = customtkinter.CTkButton(r1, text="Be A Contributor",
                                font=("Arial", 30, "bold")
                                ,image = img_one, compound = "left",
                                fg_color ="#FF7F00", hover_color = "#D76B30",
                                border_color ="#FF9E40", border_width=2,
                                command=contributor_signup)
    canvas.create_window(window_width//2 - 480 , window_height//2 + 150 ,
                         window=button1)

    button2 = customtkinter.CTkButton(r1, text="Be A Receiver",
                                      font=("Arial", 30, "bold"),
                                      image = img_two , compound = "left",
                                      fg_color="#FF7F00", hover_color="#D76B30",
                                      border_color="#FF9E40", border_width=2,
                                      command=receiver_signup)
    canvas.create_window(window_width//2 - 100, window_height//2 + 150 ,
                         window=button2)
    
    r1.mainloop()

def login():
    global k
    global user
    l = customtkinter.CTkToplevel()
    l.title("LOGIN WINDOW")
    window_width = l.winfo_screenwidth()
    window_height = l.winfo_screenheight()
    l.geometry(f'{window_width}x{window_height}')
    image = tk.PhotoImage(file="babypink.png")  
    canvas = tk.Canvas(l, width=window_width, height=window_height)
    canvas.pack()
    canvas.create_image(window_width//2, window_height//2, anchor="center", image=image)

    my_text = customtkinter.CTkTextbox(l, width=200, height=20,
                                       fg_color="#FFB6C1")
    username_label = customtkinter.CTkLabel(l, text="Enter Username",
                                            bg_color='#FFFFFF', text_color="#000000",
                                            font=("Arial", 26))

    my_text1 = customtkinter.CTkTextbox(l, width=200, height=20,
                                        fg_color="#FFB6C1")
    password_label = customtkinter.CTkLabel(l, text="Enter Password ",
                                            bg_color='#FFFFFF', text_color="#000000",
                                            font=("Arial", 26))

    # Placing widgets on the canvas
    canvas.create_window(window_width//2 +120,window_height//2,
                         window=username_label)
    canvas.create_window(window_width//2 + 350, window_height//2,
                         window=my_text)  
    canvas.create_window(window_width//2 +120, window_height//2 + 40,
                         window=password_label)  
    canvas.create_window(window_width//2+ 350, window_height//2 + 40,
                         window=my_text1)  

    def on_next():
      
        global user
        global receiver_match
        global drvy_details
        
        username = my_text.get('0.0', 'end').strip()
        password = my_text1.get('0.0', 'end').strip()   
        
        # Check if username and password match either table
        cursor.execute("SELECT * FROM Contributors WHERE C_username = %s AND C_password = %s", (username, password))
        contributor_match = cursor.fetchone()        

        cursor.execute("SELECT * FROM receiver WHERE R_username = %s AND R_password = %s", (username, password))
        receiver_match = cursor.fetchone()
        if receiver_match is None:
            pass
        else:
            check = receiver_match[5]  # Get the city from receiver_match
            cursor.execute("SELECT * FROM delivery WHERE CITY = %s", (check,))
            drvy_details = cursor.fetchall()  # Fetch all delivery persons for that city

        if contributor_match :
            k = 1
            cursor.execute('''Select CID from contributors where C_username = %s;''',(username, ))
            user = cursor.fetchall()[0][0]
            l.destroy()  # Close the login window
            dashboardc()  # Proceed to the dashboard
        elif receiver_match:
            global x
            x=1

            cursor.execute('''Select RID from receiver where R_Username = %s;''',(username, ))
            user = cursor.fetchall()[0][0]
            print (user)
            l.destroy()  # Close the login window
            dashboardr()  # Proceed to the dashboard            
            
        else:
            Toast("Invalid username or password. Please try again.")
            login()
            l.destroy()

    next_button = customtkinter.CTkButton(l, text="next",
                                          corner_radius=32, fg_color="#FF7F00", 
                hover_color="#FF9E40", border_color="#CC5500", 
                border_width=2, command=on_next)

    canvas.create_window(window_width//2 + 250 , window_height//2 + 260,
                         window=next_button)
    l.mainloop()

def Toast(text):
    toast = ToastNotification (title = "Error",message=text,duration=5000,
                               alert=True,position=(),)
    toast.show_toast()

def dashboardc():
    d = tk.Toplevel()
    window_width = d.winfo_screenwidth()
    window_height = d.winfo_screenheight()
    d.geometry(f'{window_width}x{window_height}')

    image = tk.PhotoImage(file="dpo.png")  
    
    canvas = tk.Canvas(d, width=window_width, height=window_height)
    canvas.pack()
    canvas.create_image(window_width//2, window_height//2,
                                                     anchor="center", image=image)

    img_d = tk.PhotoImage( file = "ICON donation.png")
    img_o = tk.PhotoImage( file = "ICON order.png")
    img_p = tk.PhotoImage( file = "ICON profile.png")

    donation_button = customtkinter.CTkButton(d, text="Donation", 
                         font=("Arial", 30, "bold"),
                         image = img_d , compound = "left",
                         fg_color="#FF7F00", hover_color="#FF9E40",
                         border_color="#CC5500", border_width=2,
                         command=donation)

    order1_button = customtkinter.CTkButton(d, text="Order Details", 
                         font=("Arial", 30, "bold"),
                         image = img_o , compound = "left",
                         fg_color="#FF7F00", hover_color="#FF9E40",
                         border_color="#CC5500", border_width=2,
                         command=order1)
    
    profile_button = customtkinter.CTkButton(d, text="Profile", 
                         font=("Arial", 30, "bold"),
                         image = img_p , compound = "left",
                         fg_color="#FF7F00", hover_color="#FF9E40",
                         border_color="#CC5500", border_width=2,
                         command=profile)

    canvas.create_window(window_width//2 - 160 , window_height//2 - 100,
                         window=donation_button)
    canvas.create_window(window_width//2 - 160,window_height//2,
                         window=order1_button)
    canvas.create_window(window_width//2 - 160, window_height//2 + 100,
                         window=profile_button)  

    d.update()
    d.after(500000, d.destroy)
    d.mainloop()

def donation():
    global user
    
    d = tk.Toplevel()
    d.title("DONATION WINDOW")
    window_width = d.winfo_screenwidth()
    window_height = d.winfo_screenheight()
    d.geometry(f'{window_width}x{window_height}')

    main_frame = customtkinter.CTkFrame(d)
    main_frame.pack(fill="both", expand=True)

    image = tk.PhotoImage(file="homepage donation.png")  
    
    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image = image)
    canvas.image = image 

    scrollbar = customtkinter.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrolled_frame = customtkinter.CTkFrame(canvas)
    scrolled_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrolled_frame, anchor="nw")

    label7 = customtkinter.CTkLabel(scrolled_frame, text="Enter Food Item *")
    label7.pack(pady=10)
    my_text7 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text7.pack(pady=10, padx=20)

    label8 = customtkinter.CTkLabel(scrolled_frame, text="Serving *")
    label8.pack(pady=10)
    my_text8 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text8.pack(pady=10, padx=20)

    label9 = customtkinter.CTkLabel(scrolled_frame, text="Enter Date of Donation ( YYYY-MM-DD)*")
    label9.pack(pady=10)
    my_text9 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text9.pack(pady=10, padx=20)

    label10 = customtkinter.CTkLabel(scrolled_frame, text="Enter Shelf Life of Food (In days)*")
    label10.pack(pady=10)
    my_text10 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text10.pack(pady=10, padx=20)

    label11 = customtkinter.CTkLabel(scrolled_frame, text="Enter Donation")
    label11.pack(pady=10)
    my_text11 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text11.pack(pady=10, padx=20)

    def on_next():
        global user
        r=0
        text = user
        text1 = my_text7.get('0.0','end').strip()
        text2 = my_text8.get('0.0','end').strip()
        text3 = my_text9.get('0.0','end').strip()
        text4 = my_text10.get('0.0','end').strip()
        text5 = my_text11.get('0.0','end').strip()
        
        if text3!=str(today):
            Toast("only orders for today will be accepted")
            r=2
        l1 =[text,text1,text2,text3,text4,text5]
        for i in l1:
            if i =='\n'and i != text5:
                r=1
        if r==1:
            toast("all entries are mandatory")
        if r==1 or r==2:
            d.destroy()
            donation()
        
        f = open('donation.csv', 'a',newline='')
        csv_w = csv.writer(f)
        csv_w.writerow(l1)
        f.close()
        d.destroy()
        dashboardc()
        k=1

    next_button = customtkinter.CTkButton(scrolled_frame, text="Next",
                                          corner_radius=32, fg_color="#FF7F00", 
                                hover_color="#D76B30", border_color="#FF9E40", 
                                border_width=2, command=on_next)
    next_button.pack(pady=20)
    
    d.mainloop()   


# Global dictionary to hold image references
image_refs = {}

def order1():
    global user, image_refs

    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Order List")

    try:
        # Load and resize images
        edit_icon_image = Image.open("edit_icon.png").resize((10, 10))
        delete_icon_image = Image.open("delete_icon.png").resize((10, 10))

        # Convert to PhotoImage
        edit_icon = ImageTk.PhotoImage(edit_icon_image, master=root)
        delete_icon = ImageTk.PhotoImage(delete_icon_image, master=root)

        # Store references in the dictionary
        image_refs['edit_icon'] = edit_icon
        image_refs['delete_icon'] = delete_icon
    except Exception as e:
        print(f"Error loading images: {e}")
        return

    # Create the Treeview
    tree = ttk.Treeview(root)
    tree['columns'] = ('Customer ID', 'Food Item', 'Serving', 'Date of Donation', 'Shelf Life of Food', 'Donation', 'Actions')
    tree.column('#0', width=0, stretch=tk.NO)
    for col in tree['columns']:
        tree.column(col, anchor=tk.W, width=120)
        tree.heading(col, text=col, anchor=tk.W)

    # Load data from CSV and populate Treeview
    try:
        with open('donation.csv', 'r', newline='') as f:
            csv_r = csv.reader(f)
            next(csv_r)  # Skip header
            for row in csv_r:
                if row[0] == user:
                    tree.insert('', tk.END, values=row + [''])
    except FileNotFoundError:
        print("CSV file not found.")

    tree.pack(expand=True, fill='both')

    # Dictionary to store references to action buttons
    action_buttons = {}

    def create_action_buttons():
        """Create buttons for the 'Actions' column in the Treeview."""
        for item_id in action_buttons.keys():
            action_buttons[item_id]['edit'].destroy()
            action_buttons[item_id]['delete'].destroy()

        action_buttons.clear()

        for item_id in tree.get_children():
            x, y, width, height = tree.bbox(item_id, 'Actions')
            if width > 0 and height > 0:
                # Create Edit and Delete buttons using standard Tkinter Button
                edit_btn = tk.Button(
                    root, 
                    image=image_refs['edit_icon'], 
                    command=lambda i=item_id: edit_record(i, tree.item(i, 'values')),
                    width=20,                # Slightly increased width
                    height=20,               # Increased height to give a good space
                    relief="solid",          # Adds a border to the button
                    bd=2,                    # Border thickness
                    fg="white",              # White text color (if text is displayed)
                    bg="#28a745",            # Green color for edit
                    activebackground="#218838", # Darker green when button is clicked
                    font=("Arial", 10, "bold"), # Font styling
                    padx=5,                  # Adds padding inside the button horizontally
                    pady=5                   # Adds padding inside the button vertically
                )
                delete_btn = tk.Button(
                    root, 
                    image=image_refs['delete_icon'], 
                    command=lambda i=item_id: delete_record(i, tree.item(i, 'values')),
                    width=20,                # Slightly increased width
                    height=20,               # Increased height to give a good space
                    relief="solid",          # Adds a border to the button
                    bd=2,                    # Border thickness
                    fg="white",              # White text color (if text is displayed)
                    bg="#dc3545",            # Red color for delete
                    activebackground="#c82333", # Darker red when button is clicked
                    font=("Arial", 10, "bold"), # Font styling
                    padx=5,                  # Adds padding inside the button horizontally
                    pady=5                   # Adds padding inside the button vertically
                )

                # Place the buttons in the appropriate position
                edit_btn.place(x=x + 20, y=y)
                delete_btn.place(x=x + 70, y=y)

                # Store references to prevent garbage collection
                action_buttons[item_id] = {'edit': edit_btn, 'delete': delete_btn}

    def edit_record(item_id, record):
        """ Function to edit the selected record with a popup form """
        popup = tk.Toplevel(root)
        popup.title("Edit Record")

        # Set the size of the popup window
        popup.geometry("350x400")

        # Center the popup window relative to the main window
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        x = root_x + (root_width // 2) - 175  # Centered horizontally (popup width is 350)
        y = root_y + (root_height // 2) - 200  # Centered vertically (popup height is 400)
        popup.geometry(f"+{x}+{y}")

        # Disable editing of Customer ID
        fields = ['Customer ID', 'Food Item', 'Serving', 'Date of Donation', 'Shelf Life of Food', 'Donation']
        entries = {}

        # Display "Customer ID" as a label (non-editable)
        tk.Label(popup, text="Customer ID", font=("Arial", 10)).pack(pady=5)
        tk.Label(popup, text=record[0], font=("Arial", 10, "bold")).pack(pady=5)

        # Create input fields for other fields
        for i, field in enumerate(fields[1:], start=1):
            frame = tk.Frame(popup)
            frame.pack(pady=5, padx=10, fill='x')

            tk.Label(frame, text=field, font=("Arial", 10)).pack(side="left")
            entry = tk.Entry(frame, width=25)
            entry.insert(0, record[i])
            entry.pack(side="right", padx=10)
            entries[field] = entry

        # Function to handle submit action
        def submit_changes():
            new_values = [record[0]]  # Keep Customer ID unchanged

            # Collect new values from entry fields
            for field in fields[1:]:
                new_values.append(entries[field].get())

            # Update Treeview item
            tree.item(item_id, values=new_values + [''])

            # Update the CSV file
            update_csv_after_edit(record, new_values)

            # Close the popup
            popup.destroy()
            messagebox.showinfo("Success", "Record updated successfully")

        # Submit Button
        submit_btn = tk.Button(
            popup, 
            text="Submit", 
            command=submit_changes, 
            bg="#007BFF",  # Blue color for the button
            fg="white",    # White text color for better visibility
            activebackground="#0056b3",  # Darker blue when clicked
            activeforeground="white",  # Active text color
            font=("Arial", 10, "bold"), # Bold font for better visibility
            width=15,      # Width of the button
            height=2       # Height of the button
        )
        submit_btn.pack(pady=20)

        # Make sure the popup window is on top
        popup.grab_set()
        popup.focus()
        popup.lift()

    def update_csv_after_edit(old_record, new_record):
        print(old_record, new_record,"entered update")
        # Read all rows from the CSV file
        with open('donation.csv', 'r', newline='') as f:
            rows = list(csv.reader(f))

    # Update the specific row
        updated = False  # Flag to track if an update has been made
        for i, row in enumerate(rows):
            if row[:6] == list(old_record[:6]):# Compare the first 6 fields
                
                rows[i] = new_record  # Replace old record with new record
                updated = True
                break

        if updated:
        # Write the modified rows back to the CSV file
            with open('donation.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
        else:
            print("No matching record found to update.")

    def delete_record(item_id, record):
        tree.delete(item_id)
        remove_action_buttons(item_id)
        update_csv_after_deletion(record)

    def remove_action_buttons(item_id):
        """Remove the action buttons for the deleted record."""
        if item_id in action_buttons:
            action_buttons[item_id]['edit'].destroy()
            action_buttons[item_id]['delete'].destroy()
            del action_buttons[item_id]

    def update_csv_after_deletion(record_to_delete):
        f=open('donation.csv', 'r', newline='')
        rows = list(csv.reader(f))
        f.close()

        f=open('donation.csv', 'w', newline='') 
        writer = csv.writer(f)
        for row in rows:
            if row != list(record_to_delete)[:6]:
                writer.writerow(row)
        f.close()

    # Update buttons after click event
    def on_tree_click(event):
        root.after(100, create_action_buttons)

     # tree.bind('<Button-1>', on_tree_click)

     # root.bind('<Configure>', lambda event: create_action_buttons())  # Update on window resize

    # Create action buttons initially
    root.after(200, create_action_buttons)

    root.mainloop()

def profile():
    global user
    sq = '''Select * from Contributors where cid = '%s';'''%(user,)
    cursor.execute(sq)
    data = cursor.fetchall()

    root = tk.Tk()
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    root.geometry(f'{window_width}x{window_height}')
    tree = ttk.Treeview(root)

    tree['columns'] = ('Column 1', 'Column 2', 'Column 3','Column 4','Column 5','Column 6','Column 7')
    tree.column('#0', width=0, stretch=tk.NO)  
    tree.column('Column 1', anchor=tk.W, width=200)
    tree.column('Column 2', anchor=tk.W, width=200)
    tree.column('Column 3', anchor=tk.W, width=200)
    tree.column('Column 4', anchor=tk.W, width=200)
    tree.column('Column 5', anchor=tk.W, width=200)
    tree.column('Column 6', anchor=tk.W, width=200)
    tree.column('Column 7', anchor=tk.W, width=200)

    tree.heading('#0', text='', anchor=tk.W)
    tree.heading('Column 1', text='ID', anchor=tk.W)
    tree.heading('Column 2', text='Name', anchor=tk.W)
    tree.heading('Column 3', text='Phone_no', anchor=tk.W)
    tree.heading('Column 4', text='Username', anchor=tk.W)
    tree.heading('Column 5', text='password', anchor=tk.W)
    tree.heading('Column 6', text='city', anchor=tk.W)
    tree.heading('Column 7', text='locality', anchor=tk.W)

    for row in data:
            tree.insert('', tk.END, values=row)
        
    tree.pack(expand=True, fill='both')
    
    edit = customtkinter.CTkButton(root, text="Edit",
                                   corner_radius=32, fg_color="#FF7F00", 
                                hover_color="#D76B30", border_color="#FF9E40", 
                                border_width=2, command=edit2)
    edit.pack(pady=20)
    
    root.mainloop()

def edit2():
    global user
    root = customtkinter.CTk()
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    root.geometry(f'{window_width}x{window_height}')
    
    # Scrollable layout
    main_frame = customtkinter.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg='#2b2b2b')
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = customtkinter.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrolled_frame = customtkinter.CTkFrame(canvas)
    scrolled_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrolled_frame, anchor="nw")
    
    label = customtkinter.CTkLabel(scrolled_frame, text="Enter Name" )
    label.pack(pady=10)
    my_text = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text.pack(pady=10, padx=20)

    label1 = customtkinter.CTkLabel(scrolled_frame, text="Enter Phone No")
    label1.pack(pady=10)
    my_text1 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text1.pack(pady=10, padx=20)

    label2 = customtkinter.CTkLabel(scrolled_frame, text="Enter Contributor's Username")
    label2.pack(pady=10)
    my_text2 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text2.pack(pady=10, padx=20)

    label3 = customtkinter.CTkLabel(scrolled_frame, text="Enter Contributor's Password")
    label3.pack(pady=10)
    my_text3 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text3.pack(pady=10, padx=20)

    label4 = customtkinter.CTkLabel(scrolled_frame, text="Enter City")
    label4.pack(pady=10)
    my_text4 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text4.pack(pady=10, padx=20)

    label5 = customtkinter.CTkLabel(scrolled_frame, text="Enter Locality")
    label5.pack(pady=10)
    my_text5 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text5.pack(pady=10, padx=20)

    def on_next():
        r=0
        text = my_text.get('0.0','end').strip()
        text1 = my_text1.get('0.0','end').strip()
        text2 = my_text2.get('0.0','end').strip()
        text3 = my_text3.get('0.0','end').strip()
        text4 = my_text4.get('0.0','end').strip()
        text5 = my_text5.get('0.0','end').strip()

        if text1.isdigit()==False or len(text1)!=10:
            Toast("Enter valid phno")
            r=2
        
        l =[text,text1,text2,text3,text4,text5]
        for i in l:
            if i =='\n':
                r=1
        if r==1 or r==2:
            root.destroy()
            contributor_signup()
            
        sq = '''Update contributors set CNAME= '%s',PHONE_NO= '%s', C_Username='%s', C_Password='%s',C_CITY ='%s',C_Locality='%s'Where CID = '%s' ;'''%(text, text1, text2, text3,text4,text5,user)
        cursor.execute(sq)
        mycon.commit()

        my_text.delete('0.0', 'end')
        my_text1.delete('0.0', 'end')
        my_text2.delete('0.0', 'end')
        my_text3.delete('0.0', 'end')
        my_text4.delete('0.0', 'end')
        my_text5.delete('0.0', 'end')

        root.destroy()

    next_button = customtkinter.CTkButton(scrolled_frame, text="Next",
                                          corner_radius=32, fg_color="#FF7F00", 
                                hover_color="#D76B30", border_color="#FF9E40", 
                                border_width=2, command=on_next)
    next_button.pack(pady=20)                

    root.mainloop()

''' Receiver screens start from here'''
def dashboardr():
    d = tk.Toplevel()
    window_width = d.winfo_screenwidth()
    window_height = d.winfo_screenheight()
    d.geometry(f'{window_width}x{window_height}')

    image = tk.PhotoImage(file="dpo.png")  
    
    canvas = tk.Canvas(d, width=window_width, height=window_height)
    canvas.pack()
    canvas.create_image(window_width//2, window_height//2,
                                                     anchor="center", image=image)

    img_p = tk.PhotoImage(file = "ICON profile.png")
    img_m = tk.PhotoImage(file = "ICON menu.png")
    img_o = tk.PhotoImage(file = "ICON order.png")

    profile_button = customtkinter.CTkButton(d,text="Profile",
                         font=("Arial", 30, "bold"), text_color = "white",
                         image = img_p, compound = "left",
                         fg_color="#FF7F00", hover_color="#FF9E40",
                         border_color="#CC5500", border_width=2, 
                         command=profiler)

    menu_button = customtkinter.CTkButton(d, text="Menu", 
                         font=("Arial", 30, "bold"), text_color = "white",
                         image = img_m , compound = "left",
                         fg_color="#FF7F00", border_color="#FF9E40",
                         border_width=2, hover_color="#D76B30",
                         command=menu)
    
    order_button = customtkinter.CTkButton(d, text="Order Details", 
                         font=("Arial", 30, "bold"), text_color = "white",
                         image = img_o , compound = "left",
                         fg_color="#FF7F00", border_color="#FF9E40",
                         border_width=2, hover_color="#D76B30",
                         command=Order_details)

    canvas.create_window(window_width//2 - 160 , window_height//2 - 100,
                         window=profile_button)
    canvas.create_window(window_width//2 - 160,window_height//2,
                         window=menu_button)
    canvas.create_window(window_width//2 - 160, window_height//2 + 100,
                         window=order_button)  

    d.mainloop()

def profiler():
    global user
    sq = '''Select * from receiver where rid = '%s';'''%(user,)
    cursor.execute(sq)
    data = cursor.fetchall()
    print (data)

    root = tk.Tk()
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    root.geometry(f'{window_width}x{window_height}')
    tree = ttk.Treeview(root)

    tree['columns'] = ('Column 1', 'Column 2', 'Column 3','Column 4','Column 5','Column 6','Column 7')
    tree.column('#0', width=0, stretch=tk.NO)  
    tree.column('Column 1', anchor=tk.W, width=200)
    tree.column('Column 2', anchor=tk.W, width=200)
    tree.column('Column 3', anchor=tk.W, width=200)
    tree.column('Column 4', anchor=tk.W, width=200)
    tree.column('Column 5', anchor=tk.W, width=200)
    tree.column('Column 6', anchor=tk.W, width=200)
    tree.column('Column 7', anchor=tk.W, width=200)

    tree.heading('#0', text='', anchor=tk.W)
    tree.heading('Column 1', text='ID', anchor=tk.W)
    tree.heading('Column 2', text='Name', anchor=tk.W)
    tree.heading('Column 3', text='Phone_no', anchor=tk.W)
    tree.heading('Column 4', text='Username', anchor=tk.W)
    tree.heading('Column 5', text='password', anchor=tk.W)
    tree.heading('Column 6', text='city', anchor=tk.W)
    tree.heading('Column 7', text='locality', anchor=tk.W)

    for row in data:
            tree.insert('', tk.END, values=row)
        
    tree.pack(expand=True, fill='both')
    
    edit = customtkinter.CTkButton(root, text="Edit",
                                   corner_radius=32, fg_color="#FF7F00", 
                                hover_color="#D76B30", border_color="#FF9E40", 
                                border_width=2, command=editr)
    edit.pack(pady=20)
    
    root.mainloop()
    
def editr():
    root = customtkinter.CTk()
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    root.geometry(f'{window_width}x{window_height}')
    
    # Scrollable layout
    main_frame = customtkinter.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg='#2b2b2b')
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = customtkinter.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrolled_frame = customtkinter.CTkFrame(canvas)
    scrolled_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrolled_frame, anchor="nw")
    
    label = customtkinter.CTkLabel(scrolled_frame, text="Enter Name" )
    label.pack(pady=10)
    my_text = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text.pack(pady=10, padx=20)

    label1 = customtkinter.CTkLabel(scrolled_frame, text="Enter Phone No")
    label1.pack(pady=10)
    my_text1 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text1.pack(pady=10, padx=20)

    label2 = customtkinter.CTkLabel(scrolled_frame, text="Enter Contributor's Username")
    label2.pack(pady=10)
    my_text2 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text2.pack(pady=10, padx=20)

    label3 = customtkinter.CTkLabel(scrolled_frame, text="Enter Contributor's Password")
    label3.pack(pady=10)
    my_text3 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text3.pack(pady=10, padx=20)

    label4 = customtkinter.CTkLabel(scrolled_frame, text="Enter City")
    label4.pack(pady=10)
    my_text4 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text4.pack(pady=10, padx=20)

    label5 = customtkinter.CTkLabel(scrolled_frame, text="Enter Locality")
    label5.pack(pady=10)
    my_text5 = customtkinter.CTkTextbox(scrolled_frame, width=200, height=20)
    my_text5.pack(pady=10, padx=20)  


    def on_next():
        r=0
        text = my_text.get('0.0','end').strip()
        text1 = my_text1.get('0.0','end').strip()
        text2 = my_text2.get('0.0','end').strip()
        text3 = my_text3.get('0.0','end').strip()
        text4 = my_text4.get('0.0','end').strip()
        text5 = my_text5.get('0.0','end').strip()

        if text1.isdigit()==False or len(text1)!=10:
            Toast("Enter valid phno")
            r=2
        
        l =[text,text1,text2,text3,text4,text5]
        for i in l:
            if i =='\n':
                r=1
        if r==1 or r==2:
            root.destroy()
            contributor_signup()
        sq = '''Update receiver set RNAME= '%s',PHONE_NO= '%s', R_Username='%s', R_Password='%s',R_CITY ='%s',R_Locality='%s'Where RID='%s'; '''%(text, text1, text2, text3,text4,text5,user)
        cursor.execute(sq)
        mycon.commit()

        my_text.delete('0.0', 'end')
        my_text1.delete('0.0', 'end')
        my_text2.delete('0.0', 'end')
        my_text3.delete('0.0', 'end')
        my_text4.delete('0.0', 'end')
        my_text5.delete('0.0', 'end')

        root.destroy()

    next_button = customtkinter.CTkButton(scrolled_frame, text="Next",
                                          corner_radius=32, fg_color="#FF7F00", 
                                hover_color="#D76B30", border_color="#FF9E40", 
                                border_width=2, command=on_next)
    next_button.pack(pady=20)

    root.mainloop()

def menu():
    
    m = customtkinter.CTk()
    m.title("Menu")

    # Create a heading label
    heading_label = customtkinter.CTkLabel(m, text="Food Donation Menu", font=("Helvetica", 16, "bold"))
    heading_label.pack(pady=(10, 5))

    # Create a label for column headings
    tree = ttk.Treeview(m)
    tree['columns'] = ('Food Item', 'Serving', 'Date of Donation', 'Shelf Life of Food', 'Donation')
    tree.column('#0', width=0, stretch=tk.NO)
    for col in tree['columns']:
        tree.column(col, anchor=tk.W, width=120)
        tree.heading(col, text=col, anchor=tk.W)

    # Load data from CSV and populate Treeview
    try:
        with open('donation.csv', 'r', newline='') as f:
            csv_r = csv.reader(f)
            next(csv_r)  # Skip header
            for row in csv_r:
                tree.insert('', tk.END, values=row[1:])
    except FileNotFoundError:
        print("CSV file not found.")

    tree.pack(expand=True, fill='both')

    food_items = []
    try:
        with open('donation.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food_items.append(row)  # Store the row for ordering
    except FileNotFoundError:
        error_label = customtkinter.CTkLabel(m, text="CSV file not found. Please check the file path.", text_color="red")
        error_label.pack(pady=(10, 5))
        return
    except Exception as e:
        error_label = customtkinter.CTkLabel(m, text=f"An error occurred: {e}", text_color="red")
        error_label.pack(pady=(10, 5))
        return

    order_button = customtkinter.CTkButton(m, text="Order",
                                           corner_radius=32, fg_color="#FF7F00", 
                                hover_color="#D76B30", border_color="#FF9E40", 
                                border_width=2, command=lambda: order(food_items, m))
    order_button.pack(pady=(10, 5))
 
    m.mainloop()

order_placed = False
   
def display_order_summary(order_summary):
    # Create a new top-level window for the order summary
    summary_window = tk.Toplevel()
    summary_window.title("Order Confirmed")

    # Set a fixed size for the summary window
    width = 300
    height = 150

    # Center the window on the screen
    screen_width = summary_window.winfo_screenwidth()
    screen_height = summary_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the geometry of the window
    summary_window.geometry(f"{width}x{height}+{x}+{y}")

    # Create a label to display the order summary
    summary_label = tk.Label(summary_window, text=f"You have ordered:\n{order_summary}", padx=10, pady=10)
    summary_label.pack()

    # Add a close button to the summary window
    close_button = tk.Button(summary_window, text="Close", command=summary_window.destroy)
    close_button.pack(pady=10)

def order(food_items, m):
    '''Code where receiver can order food items'''
    global order_placed  
    order_placed = False 
    
    ow = customtkinter.CTk()
    ow.title("Select Food Items to Order")

    frame = tk.Frame(ow)
    frame.pack(pady=10)

    heading_food = tk.Label(frame, text="Food Items", font=("Helvetica", 14, "bold"))
    heading_food.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    heading_quantity = tk.Label(frame, text="Serving", font=("Helvetica", 14, "bold"))
    heading_quantity.grid(row=0, column=1, padx=10, pady=5, sticky='w')

    quantity_entries = []

    for i, item in enumerate(food_items):
        food_label = tk.Label(frame, text=item['Food item'])
        food_label.grid(row=i + 1, column=0, padx=10, pady=5, sticky='w')  

        quantity_entry = tk.Entry(frame, width=10)  
        quantity_entry.grid(row=i + 1, column=1, padx=10, pady=5)  
        quantity_entries.append(quantity_entry)

    confirm_button = customtkinter.CTkButton(ow, text="Confirm Order",
                                             corner_radius=32, fg_color="#FF7F00", 
                                             hover_color="#D76B30", border_color="#FF9E40", 
                                             border_width=2,
                                             command=lambda: handle_order(quantity_entries, food_items, ow, m))
    confirm_button.pack(pady=(10, 5))

    close_button = customtkinter.CTkButton(ow, text="Close",
                                           corner_radius=32, fg_color="#FF7F00", 
                                           hover_color="#D76B30", border_color="#FF9E40", 
                                           border_width=2, command=ow.destroy)
    close_button.pack(pady=(5, 5))
    ow.mainloop()

def handle_order(quantity_entries, food_items, ow, m):
    global order_placed
    ordered_items = []
    quantities = []

    for i, entry in enumerate(quantity_entries):
        food_item = food_items[i]
        food_name = food_item['Food item']
        serving_limit = int(food_item['Serving'])  # Get the serving limit for each food item
        quantity_str = entry.get()

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
            if quantity > serving_limit:  # Check if the quantity exceeds the serving limit from the CSV
                raise ValueError(f"Quantity for {food_name} cannot exceed {serving_limit} servings.")
        except ValueError as e:
            # Display a warning if the quantity is invalid or exceeds the limit
            if str(e).startswith(f"Quantity for {food_name}"):
                messagebox.showwarning("Invalid Quantity")
            continue  # Skip invalid quantities and move to the next item
        f = open('donation.csv','r+',newline='')
        csv_r = csv.reader(f)
        l=[]
        n = next(csv_r)
        l.append(n)
        for rec in csv_r:
            if rec[1]== food_name:
                rec[2]=int(rec[2])-quantity
            l.append(rec)
        csv_w=csv.writer(f)
        f.seek(0)
        for i in l:
            csv_w.writerow(i)
        
        f.close()

        ordered_items.append(food_item)
        quantities.append(quantity)

    if ordered_items:
        global d_city
        # Generate order summary with quantities
        order_summary = ""
        for i in range(len(ordered_items)):
            item = ordered_items[i]
            order_summary += f"{item['Food item']} (Quantity: {quantities[i]})\n"

        order_summary = order_summary.strip()

        d_city = None

        for drvy in drvy_details:
            del_orders_taken = drvy[6]

            if del_orders_taken < 2:  
                d_city = drvy  
                new_orders_taken = del_orders_taken + 1
                cursor.execute("UPDATE delivery SET del_orders_taken = %s WHERE DNo = %s", (new_orders_taken, drvy[0]))
                mycon.commit()  # Commit the changes to the database
                break  # Exit the loop after updating

        # Display the order summary in a new dialog window
        display_order_summary(order_summary)

        # Save the order to a text file, including quantities
        save_details(ordered_items, quantities, receiver_match, d_city)

        order_placed = True 

        # Close the main menu window
        m.destroy()
    else:
        messagebox.showwarning("No Selection", "You must enter a quantity for at least one food item.")

    ow.destroy()

def Order_details():
    if not order_placed:
        toast("You must place an order first to view details.")
        return

    ow = customtkinter.CTk()
    ow.title("Order Details")

    window_width = 600
    window_height = 400
    ow.geometry(f'{window_width}x{window_height}')
    
    text_box = customtkinter.CTkTextbox(ow, width=580, height=350)
    text_box.pack(pady=20, padx=20)

    receiver_name = receiver_match[1]  # Ensure receiver_match is properly set

    with open('orders.txt', mode='r', encoding='utf-8') as file:
        order_contents = file.readlines()
        last_order_details = []  # To store the last match details
        current_order_details = []  # To store details of the current order being processed

        for line in order_contents:
            if f"Name: {receiver_name}" in line:
                if current_order_details:  # If we already have a current order, save it as the last order
                    last_order_details = current_order_details
                current_order_details = [line]  # Start a new order with the matching line
            
            elif current_order_details:
                # Check for a blank line to finalize the current order
                if line.strip() == "":
                    continue  # If we encounter a blank line, continue to the next line
                current_order_details.append(line)  # Store order details for the current order

        # Finalize the last order if current order details exist
        if current_order_details:
            last_order_details = current_order_details

        # Display the last matching order details if any
        if last_order_details:
            text_box.insert('end', ''.join(last_order_details))
            
    close_button = customtkinter.CTkButton(ow, text="Close",
                                           corner_radius=32, fg_color="#FF7F00", 
                                hover_color="#D76B30", border_color="#FF9E40", 
                                border_width=2, command=ow.destroy)
    close_button.pack(pady=10)

    # Start the main loop for this window
    ow.mainloop()

def save_details(ordered_items, quantities, receiver_match, d_city):
  
    
    with open('orders.txt', mode='a', encoding='utf-8') as file:
        # receiver details
        file.write(f"Name: {receiver_match[1]}, Phone number: {receiver_match[2]}\n")

       
        # Save order details
        file.write("Order Details:\n")
        s=0
        for i in range(len(ordered_items)):
            item = ordered_items[i]
            quantity = quantities[i]
            file.write(f"Food item: {item['Food item']}, Quantity: {quantity}\n")

            
        #delivery boys name
        if d_city is not None:
            file.write(f"Delivery boy assigned: {d_city[1]}\n")
            delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            file.write(f"Delivery Date: {delivery_date}\n")
            file.write("\n")  # Add a newline for separation
        else:
            file.write("No delivery boy assigned for the given city.\n")
            file.write("Order Cancelled\n")
            file.write("\n")

##MAIN LOOP
r=customtkinter.CTk()
window_width = r.winfo_screenwidth()
window_height = r.winfo_screenheight()
r.geometry(f'{window_width}x{window_height}')
image = tk.PhotoImage(file="starting.png")
canvas = tk.Canvas(r, width=window_width, height=window_height)
canvas.pack()
canvas.create_image(window_width//2, window_height//2,
                                                     anchor="center", image=image)

signup = customtkinter.CTkButton(r, text="SIGNUP",
                                  font=("Arial", 30, "bold"),
                                  text_color = "#FF9E40",
                                  fg_color="#FFFFFF", 
                                  hover_color="#FED8B1", border_color="#F4C2C2", 
                                  border_width=2, command=choice)
signup.place(relx=0.4, rely=0.4, anchor="ne")

# to open login screen
login = customtkinter.CTkButton(r, text="LOGIN",
                                font=("Arial", 30, "bold"),
                                text_color = "#FF9E40",
                                fg_color="#FFFFFF", 
                                hover_color="#FED8B1", border_color="#F4C2C2", 
                                border_width=2, command=login)
login.place(relx=0.7, rely=0.4, anchor="ne")

r.mainloop()
