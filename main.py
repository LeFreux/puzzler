from PIL import Image, ImageTk
from tkinter import Canvas
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

        # Bind mouse events
        self.puzzle_canvas.bind("<ButtonPress-1>", self.on_press)
        self.puzzle_canvas.bind("<B1-Motion>", self.on_drag)
        self.puzzle_canvas.bind("<ButtonRelease-1>", self.on_release)

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
        puzzle_frame.grid(sticky='nsew')

        self.puzzle_canvas = Canvas(master=master, bg='red', width=self.original_image.width, height=self.original_image.height)
        self.puzzle_grid_coordinates = []

        # Display images
        for x in range(rows):
            for y in range(cols):
                piece = self.puzzle_pieces[x * cols + y]
                x0 = y * self.square_width
                y0 = x * self.square_height
                self.puzzle_canvas.create_image(x0, y0, anchor='nw', image=piece)
                piece_grid_coordinates = [x0, y0, x0 + self.square_width, y0 + self.square_height]
                self.puzzle_grid_coordinates.append(piece_grid_coordinates)
        print(self.puzzle_grid_coordinates)
        self.puzzle_canvas.grid(row=0, column=0, sticky='nsew')


    def on_press(self, event):
        # Look for the closest canvas item
        piece_id = self.puzzle_canvas.find_closest(event.x, event.y)

        self.original_piece_location = self.puzzle_canvas.coords(piece_id)
        print("coordinates :", self.original_piece_location)

        if piece_id:
            self.selected_piece = piece_id[0]

            # Store the initial mouse click position
            self.start_x = event.x
            self.start_y = event.y

            print(f'start : {self.start_x}, {self.start_y}  {self.puzzle_canvas.coords(self.selected_piece)}')

    def on_drag(self, event):
        if self.selected_piece:
            # Calculate the distance moved since the initial click
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y

            # Update the coordinates of the selected piece to reflect the drag
            self.puzzle_canvas.move(self.selected_piece, delta_x, delta_y)

            # Update the initial mouse click position for the next drag event
            self.start_x = event.x
            self.start_y = event.y

            print(f'drag : {self.start_x}, {self.start_y}')

    def on_release(self, event):
        if self.selected_piece:
            # Calculate the closest grid location for the release position
            new_x = event.x
            new_y = event.y
            print(f'release : {self.start_x}, {self.start_y} | {new_x}, {new_y}')

            for coord in self.puzzle_grid_coordinates:
                if new_x > coord[0] and new_x < coord[2] and new_y > coord[1] and new_y < coord[3]:
                    grid_x, grid_y = coord[0], coord[1]

            if grid_x == None or grid_y == None : print('ERROR')

            overlapping_item = self.puzzle_canvas.find_overlapping(grid_x, grid_y, grid_x+1, grid_y+1)
            print(overlapping_item)




            # Snap the piece to the final grid location
            self.puzzle_canvas.coords(self.selected_piece, int(grid_x), int(grid_y))
            print(self.puzzle_canvas.coords(self.selected_piece))
            # If there is a piece in the location, move it to the actual moved piece location
            self.puzzle_canvas.coords(overlapping_item[0], int(self.original_piece_location[0]), int(self.original_piece_location[1]))

            self.selected_piece = None
            self.original_piece_location = None

    def get_item_at_coordinates(self, x, y):
        # Get the IDs of all items that overlap with the specified coordinates
        overlapping_items = self.puzzle_canvas.find_overlapping(x, y, x, y)

        if overlapping_items:
            # If there are overlapping items, return the ID of the first one (topmost)
            return overlapping_items[0]
        else:
            # No overlapping items found
            return None


if __name__ == "__main__":
    root = CTk.CTk()
    app = PuzzleGame(root, rows=8, cols=8)
    root.mainloop()
