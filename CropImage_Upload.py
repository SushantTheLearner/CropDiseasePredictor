import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
import os

last_uploaded_file = None

def upload_image():
    global last_uploaded_file
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg")])
    if file_path:
        try:
            # Extract the file extension
            file_extension = os.path.splitext(file_path)[1]
            # Define the target path
            target_path = os.path.join(os.getcwd(), f"newCropImage{file_extension}")
            # Copy the file to the target location
            shutil.copy(file_path, target_path)
            last_uploaded_file = target_path
            messagebox.showinfo("Success", f"Image has been uploaded and saved as 'newCropImage{file_extension}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while uploading the image: {str(e)}")
    else:
        messagebox.showinfo("Info", "No image selected, please try again")

def clear_last_image():
    global last_uploaded_file
    if last_uploaded_file and os.path.exists(last_uploaded_file):
        try:
            os.remove(last_uploaded_file)
            messagebox.showinfo("Success", f"Image '{os.path.basename(last_uploaded_file)}' has been deleted")
            last_uploaded_file = None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the image: {str(e)}")
    else:
        messagebox.showinfo("Info", "No image found in the folder to be deleted")

def on_closing():
    clear_last_image()
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Image Uploader")
root.geometry("400x200")

# Create and pack the instruction label
instruction_label = tk.Label(root, text="Upload your image here")
instruction_label.pack(pady=10)

# Load and resize the file icon
icon_image = Image.open("file_icon.png")
icon_image = icon_image.resize((20, 20), Image.LANCZOS)
file_icon = ImageTk.PhotoImage(icon_image)

# Load and resize the dustbin icon
dustbin_image = Image.open("DustbinIcon.jpg")
dustbin_image = dustbin_image.resize((20, 20), Image.LANCZOS)
dustbin_icon = ImageTk.PhotoImage(dustbin_image)

# Create a frame to hold the buttons and icons
frame = tk.Frame(root)
frame.pack(pady=10)

# Create and pack the upload button with the file icon
upload_button = tk.Button(frame, text="Upload Image", command=upload_image, compound=tk.LEFT, image=file_icon)
upload_button.pack(side=tk.LEFT, padx=10)

# Create a sub-frame to hold the dustbin icon and the clear button together
clear_frame = tk.Frame(frame)
clear_frame.pack(side=tk.LEFT, padx=10)

# Add the dustbin icon to the sub-frame
dustbin_label = tk.Label(clear_frame, image=dustbin_icon)
dustbin_label.pack(side=tk.LEFT)

# Create and pack the clear button
clear_button = tk.Button(clear_frame, text="Clear Last Image", command=clear_last_image)
clear_button.pack(side=tk.LEFT)

# Set the protocol for the window close button
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main loop
root.mainloop()
