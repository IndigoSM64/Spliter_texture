import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from PIL import Image

def divide_image(input_image, output_folder):
    img = Image.open(input_image)
    width, height = img.size
    tile_size = 32

    if width % tile_size != 0 or height % tile_size != 0:
        raise ValueError("La taille de l'image doit être un multiple de 32.")

    texture_defs = []
    texture_list = []

    for i in range(0, width, tile_size):
        for j in range(0, height, tile_size):
            box = (i, j, i + tile_size, j + tile_size)
            cropped_img = img.crop(box)
            filename = f"fragment_{i}_{j}.png"
            filepath = os.path.join(output_folder, filename)
            cropped_img.save(filepath)

            texture_name = f"test_{i // tile_size}_{j // tile_size}"
            texture_defs.append(f'ALIGNED8 static const Texture {texture_name}[] = {{\n#include "{filepath}"\n}};')
            texture_list.append(texture_name)

    texture_file_content = '\n'.join(texture_defs) + '\n\nconst Texture *const test[] = {\n' + ', '.join(texture_list) + '\n};'
    
    with open(os.path.join(output_folder, "textures.txt"), "w") as texture_file:
        texture_file.write(texture_file_content)

def browse_input_image():
    global input_image_path
    input_image_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.png")]))
    input_label.config(text=f"Image source : {input_image_path.get()}")

def browse_output_folder():
    global output_folder_path
    output_folder_path.set(filedialog.askdirectory())
    output_label.config(text=f"Dossier de sortie : {output_folder_path.get()}")

def process_image():
    try:
        divide_image(input_image_path.get(), output_folder_path.get())
        messagebox.showinfo("Succès", "L'image a été divisée et le fichier texte a été créé avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

root = Tk()
root.title("Diviseur d'image")

input_image_path = StringVar()
output_folder_path = StringVar()

browse_input_button = Button(root, text="Sélectionner l'image source", command=browse_input_image)
browse_input_button.pack(pady=10)
input_label = Label(root, text="")
input_label.pack()

browse_output_button = Button(root, text="Sélectionner le dossier de sortie", command=browse_output_folder)
browse_output_button.pack(pady=10)
output_label = Label(root, text="")
output_label.pack()

process_button = Button(root, text="Diviser l'image", command=process_image)
process_button.pack(pady=10)

root.mainloop()