import sqlite3
import tkinter

conn = sqlite3.connect('music.db')

main_window = tkinter.Tk()
main_window.title('Music DB Browser')
main_window.geometry('1024x768')

main_window.columnconfigure(0, weight=2)
main_window.columnconfigure(1, weight=2)
main_window.columnconfigure(2, weight=2)
main_window.columnconfigure(3, weight=1)


main_window.rowconfigure(0,weight=1)
main_window.rowconfigure(1,weight=5)
main_window.rowconfigure(2,weight=5)
main_window.rowconfigure(3,weight=1)

# ===labels===
tkinter.Label(main_window, text="Artists").grid(row=0, column=0)
tkinter.Label(main_window, text="Albums").grid(row=0, column=1)
tkinter.Label(main_window, text="Songs").grid(row=0, column=2)

# === artists listbox ===
artist_list = tkinter.Listbox(main_window)
artist_list.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
artist_list.config(border=2, relief='sunken')
artist_scroll = tkinter.Scrollbar(main_window, orient=tkinter.VERTICAL,
                                  command=artist_list.yview)
artist_scroll.grid(row=1,column=0, sticky='nse', rowspan=2)
artist_list['yscrollcommand'] = artist_scroll.set

# ===albums listbox===
album_LV = tkinter.Variable(main_window)
album_LV.set(("Choose an artist",))
album_list = tkinter.Listbox(main_window, listvariable=album_LV)
album_list.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
album_list.config(border=2, relief='sunken')
album_scroll = tkinter.Scrollbar(main_window, orient=tkinter.VERTICAL,
                                 command=album_list.yview)
album_scroll.grid(row=1,column=1, sticky='nse', rowspan=2)
album_list['yscrollcommand'] = album_scroll.set

# === songs listbox===
song_lv = tkinter.Variable(main_window)
song_lv.set(("Choose an Album",))
song_list = tkinter.Listbox(main_window, listvariable=song_lv)
song_list.grid(row=1, column=2, sticky='nsew', padx=(30, 0))
song_list.config(border=2, relief='sunken')


test_list = range(0, 100)
album_LV.set(tuple(test_list))
main_window.mainloop()
print("closing databse connection")
conn.close()