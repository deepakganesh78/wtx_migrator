import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from wtx_parser import WTXParser
from code_generator import PythonCodeGenerator

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, radius=10, bg='#0D99FF', fg='white', 
                 hoverbg='#0077FF', padx=20, pady=8, font=None):
        super().__init__(parent, bd=0, highlightthickness=0, background='#252526')
        
        self.command = command
        self.radius = radius
        self.bg = bg
        self.hoverbg = hoverbg
        
        if font is None:
            font = ('SF Pro Display', 10)
            
        # Create temporary label to measure text dimensions
        temp_label = tk.Label(self, text=text, font=font)
        text_width = temp_label.winfo_reqwidth()
        text_height = temp_label.winfo_reqheight()
        temp_label.destroy()
        
        # Calculate button dimensions
        width = text_width + (padx * 2)
        height = text_height + (pady * 2)
        
        self.configure(width=width, height=height)
        
        # Create rounded rectangle
        self.rect = self.create_rounded_rect(2, 2, width-2, height-2, radius, fill=bg)
        self.text = self.create_text(width/2, height/2, text=text, fill=fg, font=font)
        
        # Bind events
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def _on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hoverbg)
        
    def _on_leave(self, e):
        self.itemconfig(self.rect, fill=self.bg)
        
    def _on_click(self, e):
        if self.command:
            self.command()

class WTXMigratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WTX to Python Migrator")
        self.root.geometry("900x700")
        
        # Configure modern Apple-inspired theme colors
        self.root.configure(bg='#1E1E1E')
        self.style = ttk.Style()
        
        # Define font family (SF Pro with fallbacks)
        self.font_family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
        
        # Create title bar frame
        self.title_bar = tk.Frame(self.root, bg='#2C2C2E', height=40)
        self.title_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.title_bar.grid_columnconfigure(1, weight=1)
        
        # Title label
        self.title_label = tk.Label(self.title_bar, 
                                  text="WTX to Python Migration Tool",
                                  bg='#2C2C2E',
                                  fg='#FFFFFF',
                                  font=(self.font_family, 12))
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        # Window control buttons frame
        self.controls_frame = tk.Frame(self.title_bar, bg='#2C2C2E')
        self.controls_frame.grid(row=0, column=2, padx=5, sticky=tk.E)
        
        # Window control buttons
        button_config = {
            'bg': '#2C2C2E',
            'fg': '#FFFFFF',
            'font': (self.font_family, 12),
            'bd': 0,
            'padx': 10,
            'highlightthickness': 0,
            'activebackground': '#3C3C3E',
            'activeforeground': '#FFFFFF'
        }
        
        self.min_button = tk.Button(self.controls_frame,
                                  text="−",
                                  command=self.minimize_window,
                                  **button_config)
        self.min_button.grid(row=0, column=0, padx=2)
        
        self.max_button = tk.Button(self.controls_frame,
                                  text="□",
                                  command=self.maximize_window,
                                  **button_config)
        self.max_button.grid(row=0, column=1, padx=2)
        
        self.close_button = tk.Button(self.controls_frame,
                                    text="×",
                                    command=self.root.destroy,
                                    **button_config)
        self.close_button.grid(row=0, column=2, padx=2)
        
        # Main content frame
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame', padding="20")
        self.main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2, pady=2)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Configure custom styles with rounded corners
        self.style.configure('Main.TFrame', background='#1E1E1E')
        self.style.configure('Custom.TLabelframe', 
                           background='#252526',
                           foreground='#FFFFFF',
                           borderwidth=0)
        self.style.configure('Custom.TLabelframe.Label',
                           background='#252526',
                           foreground='#FFFFFF',
                           font=(self.font_family, 10))
        


        # Radio button style
        self.style.configure('Custom.TRadiobutton',
                           background='#252526',
                           foreground='#FFFFFF',
                           font=(self.font_family, 10))
        


        # Title Label with SF Pro font
        title_label = tk.Label(self.main_frame,
                             text="WTX to Python Migration Tool",
                             font=(self.font_family, 24, 'bold'),
                             fg='#FFFFFF',
                             bg='#1E1E1E')
        title_label.grid(row=0, column=0, pady=(0, 20), sticky='w')
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        
        # File selection with rounded corners
        self.file_frame = ttk.LabelFrame(self.main_frame,
                                       text="Select Input File",
                                       style='Custom.TLabelframe',
                                       padding="15")
        self.file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.file_frame.columnconfigure(0, weight=1)
        
        self.file_path = tk.StringVar()
        # Custom Entry with rounded corners and modern styling
        self.file_entry = tk.Entry(self.file_frame,
                                 textvariable=self.file_path,
                                 font=(self.font_family, 10),
                                 bg='#363842',
                                 fg='#FFFFFF',
                                 insertbackground='#FFFFFF',
                                 relief='flat',
                                 bd=0,
                                 cursor='ibeam')
        self.file_entry.grid(row=0, column=0, padx=(5, 10), sticky=(tk.W, tk.E), ipady=10)
        self.file_entry.configure(highlightthickness=1,
                                highlightbackground='#404040',
                                highlightcolor='#0A84FF')
        
        # Bold browse button with modern styling
        self.browse_button = RoundedButton(
            self.file_frame,
            text="Browse...",
            command=self.browse_file,
            bg='#0D99FF',
            hoverbg='#0077FF',
            font=(self.font_family, 10, 'bold'),
            radius=12,
            padx=25,
            pady=12
        )
        self.browse_button.grid(row=0, column=1, padx=5)
        
        # File type selection
        self.file_type = tk.StringVar(value="map")
        self.type_frame = ttk.LabelFrame(self.main_frame,
                                       text="WTX File Type",
                                       style='Custom.TLabelframe',
                                       padding="15")
        self.type_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        for i, (text, value) in enumerate([("Map", "map"),
                                         ("System", "system"),
                                         ("Type Tree", "typetree")]):
            ttk.Radiobutton(self.type_frame,
                           text=text,
                           value=value,
                           variable=self.file_type,
                           style='Custom.TRadiobutton').grid(row=0,
                                                           column=i,
                                                           padx=20)
        
        # Convert button
        self.convert_button = RoundedButton(
            self.main_frame,
            text="Convert to Python",
            command=self.convert_file,
            bg='#0D99FF',
            hoverbg='#0077FF',
            font=(self.font_family, 11, 'bold'),
            radius=16,  # Increased from 10
            padx=35,    # Increased padding
            pady=14     # Increased padding
        )

        self.convert_button.grid(row=3, column=0, pady=20)
        
        # Output area with rounded corners
        self.output_frame = ttk.LabelFrame(self.main_frame,
                                         text="Generated Python Code",
                                         style='Custom.TLabelframe',
                                         padding="15")
        self.output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)
        
        # Code editor with modern styling
        self.output_text = tk.Text(self.output_frame,
                                 wrap=tk.WORD,
                                 font=('SF Mono, Menlo, Monaco, Consolas', 11),
                                 bg='#2C2C2E',
                                 fg='#FFFFFF',
                                 insertbackground='#FFFFFF',
                                 selectbackground='#0A84FF',
                                 selectforeground='#FFFFFF',
                                 relief='flat',
                                 bd=0,
                                 padx=10,
                                 pady=10)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.output_text.configure(highlightthickness=1,
                                 highlightbackground='#404040',
                                 highlightcolor='#0A84FF')
        
        # Modern scrollbar
        self.scrollbar = ttk.Scrollbar(self.output_frame,
                                     orient=tk.VERTICAL,
                                     command=self.output_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.output_text['yscrollcommand'] = self.scrollbar.set

    def browse_file(self):
        filetypes = [
            ('WTX Files', '*.mmc;*.tts;*.sys'),
            ('All Files', '*.*')
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path.set(filename)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def minimize_window(self):
        self.root.iconify()

    def maximize_window(self):
        if self.root.state() == 'zoomed':
            self.root.state('normal')
        else:
            self.root.state('zoomed')

    def convert_file(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file to convert")
            return
            
        try:
            parser = WTXParser()
            generator = PythonCodeGenerator()
            
            # Parse WTX file
            wtx_content = parser.parse_file(self.file_path.get(), self.file_type.get())
            
            # Generate Python code
            python_code = generator.generate_code(wtx_content)
            
            # Display generated code
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, python_code)
            
            # Save to file
            output_file = self.file_path.get() + ".py"
            with open(output_file, 'w') as f:
                f.write(python_code)
                
            messagebox.showinfo("Success", f"Python code generated and saved to {output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

def main():
    root = tk.Tk()
    app = WTXMigratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()