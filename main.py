import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import ImageTk, Image
import os

# List to store QR code images
qr_images = []


def generate_qr_codes():
    global qr_images
    qr_images = []  # Reset the list for new QR codes

    # Get the comma-separated values from the entry widget
    input_data = entry.get()

    if not input_data:
        messagebox.showwarning("Input Error", "Please enter some values.")
        return

    # Split the input data by commas
    values = input_data.split(',')

    # Create a directory to save QR codes
    qr_dir = "qr_codes"
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)

    # Generate and display QR codes
    for value in values:
        value = value.strip()
        if value:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(value)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img_path = os.path.join(qr_dir, f"{value}.png")
            img.save(img_path)

            # Add the image to the list for later use
            qr_images.append(img_path)

            # Show QR Code in the GUI
            show_qr_code(img_path, value)


def show_qr_code(img_path, value):
    top = tk.Toplevel()
    top.title(f"QR Code for {value}")

    img = Image.open(img_path)
    img = img.resize((200, 200), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
    img = ImageTk.PhotoImage(img)

    label = tk.Label(top, image=img)
    label.image = img  # Keep a reference!
    label.pack()


def save_combined_image():
    global qr_images
    if not qr_images:
        messagebox.showwarning("No QR Codes", "Generate QR codes first.")
        return

    # Load all images
    images = [Image.open(img_path) for img_path in qr_images]

    # Determine the size for the combined image
    width, height = images[0].size
    combined_width = width * len(images)
    combined_image = Image.new('RGB', (combined_width, height), (255, 255, 255))

    # Paste each image into the combined image
    for i, img in enumerate(images):
        combined_image.paste(img, (i * width, 0))

    # Save the combined image
    combined_image_path = "combined_qr_codes.png"
    combined_image.save(combined_image_path)
    messagebox.showinfo("Success", f"Combined QR codes saved as {combined_image_path}")


# Create the main window
root = tk.Tk()
root.title("QR Code Generator")

# Add an entry widget for input
label = tk.Label(root, text="Enter comma-separated values:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Add buttons to trigger QR code generation and saving combined image
generate_button = tk.Button(root, text="Generate QR Codes", command=generate_qr_codes)
generate_button.pack(pady=10)

save_button = tk.Button(root, text="Save Combined Image", command=save_combined_image)
save_button.pack(pady=10)

# Run the application
root.mainloop()
