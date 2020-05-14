import sqlite3
import tkinter

conn = sqlite3.connect('music.db')


class Scrollbox(tkinter.Listbox):
    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)

        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL,
                                           command=self.yview)

    def grid(self, row, column, sticky='nse', rowspan=1, columnspan=1,
             **kwargs):

        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan,
                     columnspan=columnspan, **kwargs)
        self.scrollbar.grid(row=row, column=column, stick='nse',
                            rowspan=rowspan)
        self['yscrollcommand'] = self.scrollbar.set


class DataListBox(Scrollbox):
    def __init__(self, window, connection, table, field, sort_order=(),
                 **kwargs):
        super().__init__(window, **kwargs)

        self.linked_box = None
        self.link_field = None
        self.link_value = None
        self.cursor = connection.cursor()
        self.table = table
        self.field = field
        self.bind('<<ListboxSelect>>', self.on_select)

        self.sql_select = "select " + self.field + ", _id" + " FROM " +  \
                          self.table
        if sort_order:
            self.sql_sort = " ORDER BY " + ','.join(sort_order)
        else:
            self.sql_sort = " Order By " + self.field

    def clear(self):
        self.delete(0, tkinter.END)

    def link(self, widget, link_field):
        self.linked_box = widget
        widget.link_field = link_field

    def requery(self, link_value=None):
        self.link_value = link_value
        if link_value and self.link_field:
            sql = self.sql_select + " WHERE " + self.link_field + "=?" + \
                  self.sql_sort
            print(sql)
            self.cursor.execute(sql, (link_value,))
        else:
            print(self.sql_select + self.sql_sort)
            self.cursor.execute(self.sql_select + self.sql_sort)

        self.clear()
        for value in self.cursor:
            self.insert(tkinter.END, value[0])

    def on_select(self, event):
        if self.linked_box:
            print("self is event.widget")
            index = self.curselection()[0]
            value = self.get(index),

            if self.link_value:
                value = value[0], self.link_value
                sql_where = " WHERE " + self.field + " =? AND " + \
                            self.link_field + "=?"
            else:
                sql_where = " WHERE " + self.field + "=?"
            link_id = self.cursor.execute(self.sql_select + sql_where,
                                          value).fetchone()[1]
            self.linked_box.requery(link_id)


if __name__ == "__main__":
    main_window = tkinter.Tk()
    main_window.title('Music DB Browser')
    main_window.geometry('1024x768')

    main_window.columnconfigure(0, weight=2)
    main_window.columnconfigure(1, weight=2)
    main_window.columnconfigure(2, weight=2)
    main_window.columnconfigure(3, weight=1)
    main_window.rowconfigure(0, weight=1)
    main_window.rowconfigure(1, weight=5)
    main_window.rowconfigure(2, weight=5)
    main_window.rowconfigure(3, weight=1)

    # ===labels===
    tkinter.Label(main_window, text="Artists").grid(row=0, column=0)
    tkinter.Label(main_window, text="Albums").grid(row=0, column=1)
    tkinter.Label(main_window, text="Songs").grid(row=0, column=2)

    # === artists listbox ===
    artist_list = DataListBox(main_window, conn, "artists", "name")
    artist_list.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
    artist_list.config(border=2, relief='sunken')
    artist_list.requery()

    # ===albums listbox===
    album_LV = tkinter.Variable(main_window)
    album_LV.set(("Choose an artist",))
    album_list = DataListBox(main_window, conn, "albums", "name",
                             sort_order=("name",))
    album_list.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
    album_list.config(border=2, relief='sunken')
    artist_list.link(album_list, "artist")

    # === songs listbox===
    song_lv = tkinter.Variable(main_window)
    song_lv.set(("Choose an Album",))
    song_list = DataListBox(main_window, conn, "songs", "title", sort_order=(
        "track", "title"))
    song_list.grid(row=1, column=2, sticky='nsew', padx=(30, 0))
    song_list.config(border=2, relief='sunken')
    album_list.link(song_list, "album")

    main_window.mainloop()
    print("closing database connection")
    conn.close()
