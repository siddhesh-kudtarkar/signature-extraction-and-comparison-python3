from tkinter import Tk, Button, RAISED, Label, LEFT, filedialog, Toplevel, messagebox, PhotoImage, scrolledtext, HORIZONTAL, INSERT, END
from tkinter.ttk import Progressbar
import extraction, compare, os

src_img_path, ref_img_path = "", ""

#Functions
def open_window(window_name):
    main_window.withdraw()

    if (window_name == "extraction"):
        comparison_window.withdraw()
        extraction_window.deiconify()
        
    elif (window_name == "comparison"):
        extraction_window.withdraw()
        comparison_window.deiconify()

    elif (window_name == "extraction_comparison"):
        extraction_window.deiconify()
        comparison_window.deiconify()

def back(action):
    if (action == "fromComparison"):
        comparison_window.withdraw()
    elif (action == "fromExtraction"):
        extraction_window.withdraw()
    main_window.deiconify()

def exitFunction():
    exitConfirmation = messagebox.askyesno("Confirm Exit", "Do you really want to exit?")
    if (exitConfirmation > 0):
        main_window.destroy()

def file_browser(btn_name, start_directory="./"):
    filename = filedialog.askopenfilename(initialdir=start_directory, title="Select a source image file", filetypes=(("JPG files", "*.jpg*"),
    ("PNG files", "*.png*"),
    ("JPEG files", "*.jpeg*"),
    ("JPE files", "*.jpe*"),
    ("JP2 files", "*.jp2*"),
    ("WEBP files", "*.webp*"),
    ("Windows Bitmap", "*.bmp*"),
    ("Windows Bitmap", "*.dib*"),
    ("PBM files", "*.pbm*"),
    ("PGM files", "*.pgm*"),
    ("PPM files", "*.ppm*"),
    ("PXM files", "*.pxm*"),
    ("PNM files", "*.pnm*"),
    ("PFM files", "*.pfm*"),
    ("SR files", "*.sr*"),
    ("RAS files", "*.ras*"),
    ("TIFF files", "*.tiff*"),
    ("TIF files", "*.tif*"),
    ("EXR files", "*.exr*"),
    ("HDR files", "*.hdr*"),
    ("PIC files", "*.pic*")))

    file_path = filename
    filename = os.path.basename(filename)

    global src_img_path
    global ref_img_path

    if (btn_name == "btn_file_explorer"):
        btn_file_explorer.configure(text="".join(["Selected file: ", filename]))
        src_img_path = file_path
    elif (btn_name == "btn_file_explorer_src_img"):
        btn_file_explorer_src_img.configure(text="".join(["Selected file: ", filename]))
        src_img_path = file_path
    elif (btn_name == "btn_file_explorer_ref_img"):
        btn_file_explorer_ref_img.configure(text="".join(["Selected file: ", filename]))
        ref_img_path = file_path

def start_process(process_name):
    global src_img_path
    global ref_img_path

    if (process_name == "extraction"):
        extraction_log_text.configure(state="normal")
        extraction_log_text.delete('0.0', END)
        extraction_progressbar.start()
        log = extraction.extract(src_img_path)
        extraction_log_text.insert(INSERT, log)
        extraction_progressbar.stop()
        extraction_log_text.configure(state="disabled")

    elif (process_name == "comparison"):
        comparison_log_text.configure(state="normal")
        comparison_log_text.delete('0.0', END)
        comparison_progressbar.start()
        log = compare.compare(src_img_path, ref_img_path)
        comparison_log_text.insert(INSERT, log)
        comparison_progressbar.stop()
        comparison_log_text.configure(state="disabled")

#Main Window
main_window = Tk()

main_window.geometry("500x400+400+200")
main_window.configure(background="lightblue")
main_window.title("Signature Detection, Extraction & Comparison")

main_window_icon = PhotoImage(file="./images/signature_icon.jpg")
main_window.iconphoto(False, main_window_icon)

btn_extraction_only = Button(main_window, background="lightyellow", activebackground="green", activeforeground="white", text="Signature Extraction only", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:open_window("extraction"))
btn_extraction_only.pack(padx=10, pady=15)

btn_comparison_only = Button(main_window, background="lightyellow", activebackground="green", activeforeground="white", text="Signature Comparison only", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:open_window("comparison"))
btn_comparison_only.pack(padx=10, pady=15)

btn_extraction_comparison = Button(main_window, background="lightyellow", activebackground="green", activeforeground="white", text="Both Signature Extraction & Comparison", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:open_window("extraction_comparison"))
btn_extraction_comparison.pack(padx=10, pady=15)

btn_exit = Button(main_window, background="lightyellow", activebackground="green", activeforeground="white", text="Exit", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=exitFunction)
btn_exit.pack(padx=10, pady=15)

#Extraction Window
extraction_window = Toplevel(main_window)

extraction_window.geometry("500x550+80+100")
extraction_window.configure(background="lightblue")
extraction_window.title("Signature Extraction")

lbl_extraction_src_img = Label(extraction_window, text="Select a source image file:", background="lightblue", font=("Calibri", 15, "bold"), width=35)
lbl_extraction_src_img.pack(padx=10, pady=15)

btn_file_explorer = Button(extraction_window, background="lightyellow", activebackground="green", activeforeground="white", text="Choose an image file", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:file_browser("btn_file_explorer"))
btn_file_explorer.pack(padx=10, pady=15)

btn_start_extraction = Button(extraction_window, background="lightyellow", activebackground="green", activeforeground="white", text="Start Signature Extraction", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:start_process("extraction"))
btn_start_extraction.pack(padx=10, pady=15)

lbl_extraction_log = Label(extraction_window, text="Progress of process:", font=("Calibri", 15, "bold"), background="lightblue", width=35)
lbl_extraction_log.pack(padx=10, pady=15)

extraction_progressbar = Progressbar(extraction_window, orient=HORIZONTAL, length=350, mode="indeterminate")
extraction_progressbar.pack(padx=10, pady=15, expand=False)

extraction_log_text = scrolledtext.ScrolledText(extraction_window, width=45, height=7, state="disabled")
extraction_log_text.pack(padx=10, pady=15)

btn_extraction_back = Button(extraction_window, background="lightyellow", activebackground="green", activeforeground="white", text="Back", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:back("fromExtraction"))
btn_extraction_back.pack(padx=10, pady=15)

extraction_window.withdraw()

#Comparison Window
comparison_window = Toplevel(main_window)

comparison_window.geometry("500x650+700+50")
comparison_window.configure(background="lightblue")
comparison_window.title("Signature Comparison")

lbl_comparison_src_img = Label(comparison_window, text="Select a source image file:", background="lightblue", font=("Calibri", 15, "bold"), width=35)
lbl_comparison_src_img.pack(padx=10, pady=15)

btn_file_explorer_src_img = Button(comparison_window, background="lightyellow", activebackground="green", activeforeground="white", text="Choose an image file", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:file_browser("btn_file_explorer_src_img"))
btn_file_explorer_src_img.pack(padx=10, pady=15)

lbl_comparison_ref_img = Label(comparison_window, text="Select a reference image file:", background="lightblue", font=("Calibri", 15, "bold"), width=35)
lbl_comparison_ref_img.pack(padx=10, pady=15)

btn_file_explorer_ref_img = Button(comparison_window, background="lightyellow", activebackground="green", activeforeground="white", text="Choose an image file", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:file_browser("btn_file_explorer_ref_img"))
btn_file_explorer_ref_img.pack(padx=10, pady=15)

btn_start_comparison = Button(comparison_window, background="lightyellow", activebackground="green", activeforeground="white", text="Start Signature Comparison", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:start_process("comparison"))
btn_start_comparison.pack(padx=10, pady=15)

lbl_comparison_log = Label(comparison_window, text="Progress of process:", font=("Calibri", 15, "bold"), background="lightblue", width=35)
lbl_comparison_log.pack(padx=10, pady=15)

comparison_progressbar = Progressbar(comparison_window, length=350, orient=HORIZONTAL, mode="indeterminate")
comparison_progressbar.pack(padx=10, pady=15, expand="False")

comparison_log_text = scrolledtext.ScrolledText(comparison_window, width=45, height=7, state="disabled")
comparison_log_text.pack(padx=10, pady=15)

btn_comparison_back = Button(comparison_window, background="lightyellow", activebackground="green", activeforeground="white", text="Back", font=('Calibri', 15, 'bold'), width=35, relief=RAISED, command=lambda:back("fromComparison"))
btn_comparison_back.pack(padx=10, pady=15)

comparison_window.withdraw()

main_window.mainloop()