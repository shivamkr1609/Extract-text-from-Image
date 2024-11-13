import cv2
import pytesseract
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, RIGHT, LEFT, Y, BOTH, Frame, Canvas, END

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path if necessary


class TextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Extractor")

        # Create a frame to hold the image and scrollable text side-by-side
        self.frame = Frame(root)
        self.frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Create a canvas to enable image scrolling if necessary
        self.canvas = Canvas(self.frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Create a label to show the image inside the canvas
        self.image_label = Label(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_label, anchor="nw")

        # Add scrollbars to the canvas for large images
        self.canvas_scrollbar_y = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas_scrollbar_y.pack(side=RIGHT, fill="y")
        self.canvas_scrollbar_x = Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.canvas_scrollbar_x.pack(side="bottom", fill="x")

        self.canvas.configure(yscrollcommand=self.canvas_scrollbar_y.set, xscrollcommand=self.canvas_scrollbar_x.set)

        # Create a button to open the file dialog
        self.open_button = Button(root, text="Open Image", command=self.open_image)
        self.open_button.pack(pady=10)

        # Create a button to extract text
        self.extract_button = Button(root, text="Extract Text", command=self.extract_text)
        self.extract_button.pack(pady=10)

        # Create a scrollable text widget to show extracted text
        self.text_output = Text(root, wrap='word', height=10, width=50)
        self.text_output.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Add a scrollbar to the text widget
        self.text_scrollbar = Scrollbar(root, command=self.text_output.yview)
        self.text_scrollbar.pack(side=RIGHT, fill=Y)
        self.text_output.config(yscrollcommand=self.text_scrollbar.set)

        self.image_path = None
        self.image = None

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.image_path = file_path
            # Load and resize image
            self.image = cv2.imread(file_path)
            self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.pil_image = Image.fromarray(self.image_rgb)

            # Resize large images for display
            max_width, max_height = 600, 400
            self.pil_image.thumbnail((max_width, max_height), Image.LANCZOS)


            # Convert image to Tkinter format and display
            self.tk_image = ImageTk.PhotoImage(self.pil_image)
            self.image_label.config(image=self.tk_image)
            self.image_label.image = self.tk_image

            # Configure scroll region for large images
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def extract_text(self):
        if self.image_path:
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(self.image)
            # Display the extracted text in the text widget
            self.text_output.delete(1.0, END)  # Clear previous text
            self.text_output.insert(END, text)
        else:
            self.text_output.delete(1.0, END)
            self.text_output.insert(END, "No image selected")


if __name__ == "__main__":
    root = Tk()
    app = TextExtractorApp(root)
    root.mainloop()















