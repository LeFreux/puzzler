from PIL import Image, ImageTk
import customtkinter as CTk
import random

class PuzzleGame:
    def __init__(self, master, rows, cols):
        # Load the original image
        self.original_image = Image.open("image.bmp")

        # Initialize photo_references as an empty list
        self.photo_references = []

        # Cut the image into pieces
        self.puzzle_pieces = self.cut_image_in_square(rows, cols)

        # Set up the GUI
        self.create_gui(master, rows, cols)

        # Additional attributes for drag-and-drop
        self.selected_piece = None
        self.offset_x = 0
        self.offset_y = 0

        # Bind mouse events
        self.puzzle_canvas.bind("<ButtonPress-1>", self.on_press)
        self.puzzle_canvas.bind("<B1-Motion>", self.on_drag)
        self.puzzle_canvas.bind("<ButtonRelease-1>", self.on_release)
        self.puzzle_pieces_coordinates = []

    def cut_image_in_square(self, rows, cols):
        self.square_width = self.original_image.width // cols
        self.square_height = self.original_image.height // rows
        pieces = []

        for x in range(rows):
            for y in range(cols):
                piece = self.original_image.crop(box=(y * self.square_width,
                                                      x * self.square_height,
                                                      (y + 1) * self.square_width,
                                                      (x + 1) * self.square_height))
                piece.save(f'image{x}{y}.bmp')
                photo_piece = ImageTk.PhotoImage(piece)
                self.photo_references.append(photo_piece)
                pieces.append(photo_piece)
        return pieces

    def create_gui(self, master, rows, cols):
        puzzle_frame = CTk.CTkFrame(master=master)

        rows_index = tuple(range(rows))
        cols_index = tuple(range(cols))
        puzzle_frame.columnconfigure(cols_index, weight=1)
        puzzle_frame.rowconfigure(rows_index, weight=1)
        puzzle_frame.grid(sticky='nsew')

        self.puzzle_canvas = CTk.CTkCanvas(master=master, bg='red', width=self.original_image.width, height=self.original_image.height)

        #display the images
        for x in range(rows):
            for y in range(cols):
                piece = self.puzzle_pieces[x * cols + y]
                x0 = y * self.square_width
                y0 = x * self.square_height
                self.puzzle_canvas.create_image(x0, y0, anchor='nw', image=piece)

        self.puzzle_canvas.grid(row=0, column=0, sticky='nsew')

    def on_press(self, event):
        # Look for the closest canvas item
        piece_id = self.puzzle_canvas.find_closest(event.x, event.y)

        if piece_id:
            self.selected_piece = piece_id[0]
            self.offset_x = event.x - self.puzzle_canvas.coords(self.selected_piece)[0]
            self.offset_y = event.y - self.puzzle_canvas.coords(self.selected_piece)[1]

    def on_drag(self, event):
        if self.selected_piece:
            new_x = event.x - self.offset_x
            new_y = event.y - self.offset_y
            self.puzzle_canvas.coords(self.selected_piece, new_x -(self.square_width/2), new_y -(self.square_height/2))

    def on_release(self, event):
        if self.selected_piece:
            self.selected_piece = None
            self.offset_x = 0
            self.offset_y = 0

if __name__ == "__main__":
    root = CTk.CTk()
    app = PuzzleGame(root, rows=3, cols=3)
    root.mainloop()
