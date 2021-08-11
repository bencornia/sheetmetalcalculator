import tkinter as tk
from tkinter import Frame, ttk
from itertools import islice



def main():
    # create top level widget
    root = tk.Tk()   

    frm_main = tk.Frame(root)
    frm_main.master.title("Sheet Metal Calculator")
    frm_main.pack(padx=40, pady=10)
    frm_bend = tk.Frame(root)
    frm_bend.pack(padx=40, pady=10)
    frm_flg = tk.Frame(root)
    frm_flg.pack(padx=40, pady=10)
    frm_results = tk.Frame(root)
    frm_results.pack(padx=40, pady=10)

    maths = create_entries(frm_main)
    bend_count = create_combo(frm_main)
    bends = create_bends(frm_bend)
    flanges = create_flanges(frm_flg)
    results = display_results(frm_results)
    update_rows(flanges, bend_count, bends)

    root.mainloop()
    

def create_entries(frm_main):
    fields = ('Material Thickness', 'Bend Radius', 'K Factor')
    maths = {}

    for field in fields:
        row = Frame(frm_main)
        label = tk.Label(row, width=20, anchor='w', text=field)
        entry = tk.Entry(row)
        row.pack(side=tk.TOP, 
                 padx=5, 
                 pady=5)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, '0')
        # store values in dictionary
        maths[field] = entry    

    return maths
    

def create_combo(frm_main):
    row = tk.Frame(frm_main)
    label = tk.Label(row, width=33, anchor='w', text='Number of Bends')
    row.pack(side=tk.TOP, 
                padx=5, 
                pady=5)        
    label.pack(side=tk.LEFT)
    bend_count = ttk.Combobox(row, width=2,
                                values=['1', '2', '3','4'],
                                state='readonly')
    bend_count.current(0)
    bend_count.pack(side=tk.RIGHT)
    label.pack(side=tk.LEFT)

    return bend_count


def create_flanges(frm_flg):
    flange_count = 5
    flanges = {}

    for i in range(flange_count):
        field_name = f'Flange {i+1}'        
        row = tk.Frame(frm_flg)
        label = tk.Label(row, width=20, anchor='w', text=field_name)
        entry = tk.Entry(row)
        row.pack(side=tk.TOP,
                 padx=5,
                 pady=5)  
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, '0')
        # store values in dictionary
        flanges[field_name] = row

    return flanges


def create_bends(frm_bend):
    bend_count = 4
    bends = {}
    for i in range(bend_count):
        field_name = f'Bend Angle {i+1}'        
        row = tk.Frame(frm_bend)
        label = tk.Label(row, width=20, anchor='w', text=field_name)
        entry = tk.Entry(row)
        row.pack(side=tk.TOP,
                 padx=5,
                 pady=5)  
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, '0')
        # store values in dictionary
        bends[field_name] = row

    return bends


def display_results(frm_results):
    labels = ('Flat Length:', 'Bend Centers:')
    results = {}

    for label in labels:
        row = tk.Frame(frm_results)
        label = tk.Label(row, width=20, anchor='w', text=label)
        label_val = tk.Label(row, width=17, anchor='w', text='0')
        row.pack(side=tk.TOP,
                 padx=5,
                 pady=5)  
        label.pack(side=tk.LEFT)
        label_val.pack(side=tk.RIGHT)
        # store values in dictionary
        results[label]=label_val

    return results


def update_rows(flanges, bend_count, bends):


    def update_flanges(event):
        bend_num = int(bend_count.get())
        flange_count = bend_num+1  
        flange_rows = flanges.values()

        # unpack flange rows
        for row in flange_rows:
            row.pack_forget()

        # pack flange rows
        for row in islice(flange_rows, flange_count):
            row.pack(side=tk.TOP,
                    padx=5,
                    pady=5)


    def update_bends(event):
        bend_num = int(bend_count.get())
        bend_rows = bends.values()        

        # unpack bend rows
        for row in bend_rows:
            row.pack_forget()

        # pack bend rows
        for row in islice(bend_rows, bend_num):
            row.pack(side=tk.TOP,
                    padx=5,
                    pady=5)



        

    bend_count.bind('<<ComboboxSelected>>', update_bends)
    bend_count.bind('<<ComboboxSelected>>', update_flanges, add=True)


if __name__ == '__main__':
    main()