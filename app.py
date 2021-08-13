import tkinter as tk
from tkinter import Frame, ttk
from itertools import islice
import math
from sheet_metal_calc import calc_bend_deduct, calc_bend_centers


def main():
    # create top level widget
    root = tk.Tk()   

    # create frames
    frm_main = tk.Frame(root)
    frm_main.master.title("Sheet Metal Calculator")
    frm_main.pack(padx=40, pady=10)
    frm_bend = tk.Frame(root)
    frm_bend.pack(padx=40, pady=10)
    frm_flg = tk.Frame(root)
    frm_flg.pack(padx=40, pady=10)
    frm_results = tk.Frame(root)
    frm_results.pack(padx=40, pady=10)

    # return values as dictionaries
    bend_properties = create_entries(frm_main)
    bend_count = create_combo(frm_main)
    bends = create_bends(frm_bend)
    flanges = create_flanges(frm_flg)
    results = display_results(frm_results)
    update_rows(flanges, bend_count, bends)
    
    return_results(bend_properties, bend_count, bends, flanges, results)

    root.mainloop()


def return_results(bend_properties, bend_count, bends, flanges, results):
    

    def calc(event):

        # calculate bend deduction
        mt = float(bend_properties['Material Thickness'].get())
        ir = float(bend_properties['Bend Radius'].get())
        k = float(bend_properties['K Factor'].get())
        bc = int(bend_count.get())

        bend_deduct_list = []
        for i in range(1, bc+1):
            ba = float(bends[f'Bend Angle {i}'].children['!entry'].get())
            ba = 180 - ba
            bd = 2 * (math.tan(math.radians(ba/2)) * (ir + mt))- math.pi/180 * ba * (ir + k * mt)
            bend_deduct_list.append(bd)

        bend_deduction = sum(bend_deduct_list)

        # calculate flat length
        flange_list = []
        for i in range(1, 6):
            flange = float(flanges[f'Flange {i}'].children['!entry'].get())
            flange_list.append(flange)

        total_length = sum(flange_list) 
        flat_length = total_length - bend_deduction

        # calculate bend_centers
        length = 0
        previous_deduct = 0
        centers = ''
        for i in range(bc):
            deduct = bend_deduct_list[i]/2
            flange = flange_list[i]        
            bend_center = str(round(flange - deduct - previous_deduct + length, 2))
            length = flange - deduct - previous_deduct + length
            previous_deduct = deduct

            centers += bend_center + '   '
            


        # display results
        results['Flat Length:'].configure(text=f'{flat_length:.2f}')
        results['Bend Centers:'].configure(text=f'{centers}')


        

    # bind entry objects to key release event
    flanges['Flange 1'].children['!entry'].bind('<KeyRelease>', calc)
    flanges['Flange 2'].children['!entry'].bind('<KeyRelease>', calc)
    flanges['Flange 3'].children['!entry'].bind('<KeyRelease>', calc)
    flanges['Flange 4'].children['!entry'].bind('<KeyRelease>', calc)
    flanges['Flange 5'].children['!entry'].bind('<KeyRelease>', calc)

    bends[f'Bend Angle 1'].children['!entry'].bind('<KeyRelease>', calc)
    bends[f'Bend Angle 2'].children['!entry'].bind('<KeyRelease>', calc)
    bends[f'Bend Angle 3'].children['!entry'].bind('<KeyRelease>', calc)
    bends[f'Bend Angle 4'].children['!entry'].bind('<KeyRelease>', calc)

    bend_properties['Material Thickness'].bind('<KeyRelease>', calc)
    bend_properties['Bend Radius'].bind('<KeyRelease>', calc)
    bend_properties['K Factor'].bind('<KeyRelease>', calc)
    

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

    for labelname in labels:
        row = tk.Frame(frm_results)
        label = tk.Label(row, width=20, anchor='w', text=labelname)
        label_val = tk.Label(row, width=17, anchor='w', text='0')
        row.pack(side=tk.TOP,
                 padx=5,
                 pady=5)  
        label.pack(side=tk.LEFT)
        label_val.pack(side=tk.RIGHT)
        # store values in dictionary
        results[labelname]=label_val

    return results


def update_rows(flanges, bend_count, bends): 


    def update_flanges(event):
        bend_num = int(bend_count.get())
        flange_count = bend_num+1  
        flange_rows = flanges.values()

        # unpack flange rows
        for row in flange_rows:
            row.pack_forget()
            entry = row.children['!entry']
            entry.delete(0, 'end')
            entry.insert(0, '0')

        # pack flange rows
        for row in islice(flange_rows, flange_count):
            row.pack(side=tk.TOP,
                    padx=5,
                    pady=5)
            entry = row.children['!entry']
            entry.delete(0, 'end')
            entry.insert(0, '0')


    def update_bends(event):
        bend_num = int(bend_count.get())
        bend_rows = bends.values()        

        # unpack bend rows
        for row in bend_rows:
            row.pack_forget()
            entry = row.children['!entry']
            entry.delete(0, 'end')
            entry.insert(0, '0')

        # pack bend rows
        for row in islice(bend_rows, bend_num):
            row.pack(side=tk.TOP,
                    padx=5,
                    pady=5)  
            entry = row.children['!entry']
            entry.delete(0, 'end')
            entry.insert(0, '0')


    bend_count.bind('<Visibility>', update_bends)
    bend_count.bind('<Visibility>', update_flanges, add=True)
    bend_count.bind('<<ComboboxSelected>>', update_bends, add=True)
    bend_count.bind('<<ComboboxSelected>>', update_flanges, add=True)


if __name__ == '__main__':
    main()