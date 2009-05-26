import threading
import time
import Tkinter

from tibdb import tibiacom
from classes import \
        AsyncWidgetCommand, ListboxContextMenu, WidgetState, ActiveCharacterList, StanceContextMenu
from functions import get_char_guild, update_guild_members, open_char_page
from globals import VERSION, STANCES, char_stances, guild_stances, guild_members

class GuildStanceDialog:
    def __init__(self, parent, callback):
        self.callback = callback
        self.fetch_guild_list = AsyncWidgetCommand(parent, self.__fetch_guild_list)
        self.dialog = Tkinter.Toplevel(parent)
        self.dialog.transient(parent)
        self.dialog.title("Guild Stances")
        self.dialog.grab_set()
        self.button = Tkinter.Button(
                self.dialog,
                text="Fetch Guild List")
        self.fetch_guild_list.add_widget(self.button, True)
        self.button.pack(side=Tkinter.BOTTOM)
        self.scrollbar = Tkinter.Scrollbar(self.dialog)
        self.scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        self.listbox_data = []
        self.listbox = Tkinter.Listbox(
                self.dialog,
                height=20,
                yscrollcommand=self.scrollbar.set)
        self.listbox.bind(
                "<Button-3>",
                StanceContextMenu(
                        self.dialog,
                        self.listbox,
                        self.stance_changed,
                        self.listbox_data,
                        guild_stances)
                    .handler)
        self.listbox.pack(fill=Tkinter.BOTH, expand=Tkinter.YES)
        self.scrollbar.config(command=self.listbox.yview)
        self.refresh_listbox()
    def stance_changed(self):
        self.refresh_listbox()
        self.callback()
    def refresh_listbox(self):
        listbox_offset = self.listbox.yview()[0]
        self.listbox.delete(0, Tkinter.END)
        del self.listbox_data[:]
        # sort by stances first, then by guild name
        items = sorted(guild_stances.items(), key=lambda (k, v): (v, k))
        items += [ (x, None) for x in sorted(guild_members.keys()) if x not in guild_stances.keys() ]
        for guild, stance in items:
            self.listbox.insert(Tkinter.END, guild)
            if stance is not None:
                self.listbox.itemconfig(Tkinter.END, fg=STANCES[stance][1])
            self.listbox_data.append(guild)
        for index in xrange(self.listbox.size()):
            for opt in (("selectforeground", "fg"), ("selectbackground", "bg")):
                self.listbox.itemconfig(
                        index, **dict(((
                                opt[0],
                                self.listbox.itemcget(index, opt[1]) or self.listbox.cget(opt[1]))
                            ,)))
        self.listbox.yview_moveto(listbox_offset)
    def __fetch_guild_list(self, gui):
        guilds = tibiacom.guild_list("Dolera")
        for g in guilds:
            guild_members.setdefault(g, set())
        gui.post(self.refresh_listbox)

class MainDialog:
    def __update_pzlocks(self, gui):
        assert threading.current_thread().name != "MainThread"
        self.char_data.parse_potential_recent_deaths(
                lambda: gui.post(self.refresh_listbox))
        print "done updating pzlocks."

    def __update_from_online_list(self, gui):
        assert threading.current_thread().name != "MainThread"
        update_started = time.time()
        update_delay = 60000
        self.next_update = None
        gui.post(self.refresh_statusbar, daemonic=False)
        #self.dialog.update_idletasks()
        try:
            stamp, changed = self.char_data.update_from_online_list()
            if self.first_update is None: self.first_update = stamp
            self.last_update = stamp
            if changed: update_delay = 290000
            gui.post(self.refresh_listbox)
        finally:
            # take into account the time taken to perform this update,
            # negative delays will just trigger an immediate update.
            mark = time.time()
            update_delay -= int((mark - update_started) * 1000)
            self.next_update = mark + update_delay / 1000
            print "next update in", update_delay, "ms"
            return update_delay,

    def __update_guild_members(self, gui):
        assert threading.current_thread().name != "MainThread"
        update_guild_members()
        gui.post(self.refresh_listbox)

    def __init__(self, root, listbox_font):
        self.dialog = root
        self.dialog.title("Prolepsis " + VERSION)

        self.update_pzlocks = AsyncWidgetCommand(root, self.__update_pzlocks)
        self.update_online_list = AsyncWidgetCommand(root, self.__update_from_online_list)
        self.update_guild_members = AsyncWidgetCommand(root, self.__update_guild_members)

        self.statusbar = Tkinter.Label(
                self.dialog,
                text="Error!",
                anchor=Tkinter.W,
                justify=Tkinter.LEFT,
                relief=Tkinter.SUNKEN,
                borderwidth=1)
        self.statusbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)

        self.pzlock_button = Tkinter.Button(self.dialog, text="Update PZ locks")
        self.update_pzlocks.add_widget(self.pzlock_button, True)
        self.pzlock_button.pack(side=Tkinter.BOTTOM)

        # can't seem to flatten the scrollbar on windows
        self.scrollbar = Tkinter.Scrollbar(self.dialog)
        self.scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

        self.listbox_data = []

        self.listbox = Tkinter.Listbox(
                self.dialog,
                yscrollcommand=self.scrollbar.set,
                font=listbox_font,
                bg="light yellow",
                selectmode=Tkinter.SINGLE,
                height=30,
                width=40,
                relief=Tkinter.FLAT,
            )
        self.listbox.config(
                selectbackground=self.listbox["bg"],
                selectforeground=self.listbox["fg"])
        self.listbox.bind(
                "<Double-Button-1>",
                lambda event: open_char_page(event, self.listbox_data))
        self.listbox.bind(
                "<Button-3>",
                ListboxContextMenu(
                        root, self.listbox, self.refresh_listbox,
                        self.listbox_data, char_stances, guild_stances)
                    .handler)
        self.listbox.pack(fill=Tkinter.BOTH, expand=Tkinter.YES)

        self.scrollbar.config(command=self.listbox.yview)

        self.menubar = Tkinter.Menu(root)

        self.list_sort_mode = Tkinter.StringVar(value='level')

        self.list_menu = Tkinter.Menu(self.menubar, tearoff=False)

        self.sortby_menu = Tkinter.Menu(self.dialog, tearoff=False)
        for s in ("level", "stance", "vocation", "guild"):
            self.sortby_menu.add_radiobutton(
                    label=s.capitalize(),
                    variable=self.list_sort_mode,
                    command=self.refresh_listbox,
                    value=s)

        self.list_menu.add_cascade(label="Sort by", menu=self.sortby_menu)

        self.list_show_guild = Tkinter.BooleanVar(value=True)
        self.list_show_unguilded = Tkinter.BooleanVar(value=True)

        self.list_menu.add_checkbutton(
                label="Show character's guild",
                variable=self.list_show_guild,
                command=self.refresh_listbox)
        self.list_menu.add_checkbutton(
                label="Show unguilded characters",
                variable=self.list_show_unguilded,
                command=self.refresh_listbox)

        self.menubar.add_cascade(label="List", menu=self.list_menu)

        self.guild_menu = Tkinter.Menu(self.menubar, tearoff=False)
        self.guild_menu.add_command(label="Update members")
        self.update_guild_members.add_widget(
                WidgetState(self.guild_menu, get="entrycget", set="entryconfig", index=0),
                True)
        self.guild_menu.add_command(
                label="Modify stances",
                command=lambda: GuildStanceDialog(self.dialog, self.refresh_listbox))

        self.menubar.add_cascade(label="Guilds", menu=self.guild_menu)

        self.always_on_top = Tkinter.BooleanVar(value=False)

        self.window_menu = Tkinter.Menu(self.menubar, tearoff=False)
        self.window_menu.add_checkbutton(
                label="Always on top",
                variable=self.always_on_top,
                command=self.always_on_top_command)

        self.menubar.add_cascade(label="Window", menu=self.window_menu)

        self.help_menu = Tkinter.Menu(self.menubar, tearoff=False)
        self.help_menu.add_command(
                label="Wiki Howto",
                command=lambda: webbrowser.open("http://code.google.com/p/anacrolix/wiki/Prolepsis"))
        self.help_menu.add_command(
                label="Report issue",
                command=lambda: webbrowser.open("http://code.google.com/p/anacrolix/issues/list"))
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", state=Tkinter.DISABLED)

        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        self.dialog.config(menu=self.menubar)

        self.first_update = None
        self.last_update = None
        self.next_update = None
        self.char_data = ActiveCharacterList("Dolera")

        self.dialog.after_idle(self.refresh_statusbar, True)
        self.dialog.after_idle(self.refresh_listbox, True)
        self.dialog.after_idle(self.update_online_list)

    def always_on_top_command(self):
        self.dialog.wm_attributes("-topmost", self.always_on_top.get())

    def refresh_statusbar(self, daemonic=False):
        try:
            if self.last_update is None:
                last = "never"
            else:
                last = "%ds ago" % (round(time.time() - self.last_update),)
            if self.next_update is None:
                next = "now"
            else:
                next = "in %ds" % (round(self.next_update - time.time()),)
            text = \
                ("World: Dolera (%d players online)\n" + \
                "Last update: %s. Next update: %s") \
                % (self.char_data.online_count(), last, next,)
            self.statusbar.config(text=text)
            self.statusbar.pack()
        except:
            self.statusbar.config(text="Fucking Error!")
            raise
        finally:
            if daemonic:
                self.dialog.after(1000, self.refresh_statusbar, True)
            #else:
                # considering an idle update here to push statusbar changes

    def refresh_listbox(self, daemonic=False):
        try:
            player_kills = self.char_data.get_player_killers()
            items = []
            for name, info in self.char_data.chars.copy().iteritems():
                death = False
                if hasattr(info, "deaths"):
                    for d in info.deaths:
                        if tibiacom.tibia_time_to_unix(d[0]) > time.time() - 1200:
                            death = True
                            break
                # get guild
                guild = get_char_guild(name)
                # get stance
                try: stance = char_stances[name]
                except KeyError:
                    try: stance = guild_stances[guild]
                    except KeyError: stance = None
                # background
                #assert info.last_offline != info.last_online
                background = None
                if info.is_online():
                    assert self.first_update is not None
                    if time.time() - info.last_offline() < 300 and info.last_offline() != self.first_update:
                        background = "white"
                else:
                    if time.time() - info.last_online() < 300:
                        background = "light grey"
                    else:
                        if not death: continue
                pzlocked = False
                if player_kills.has_key(name):
                    for kill in player_kills[name]:
                        print name, kill,
                        if kill.is_pzlocked(info):
                            pzlocked = True
                            break
                if not death and not pzlocked and (info.vocation == "N" or stance is None and (info.level < 45 or not self.list_show_unguilded.get())):
                    continue
                items.append((name, info.level, info.vocation, background, stance, guild, death, pzlocked))

            STANCE_KEY = dict(zip((2, 0, 1, None), range(4)))
            level_sort = lambda x: -x[1]
            stance_sort = lambda x: STANCE_KEY[x[4]]
            vocation_sort = lambda x: dict(
                    zip(("MS", "ED", "RP", "EK", "S", "D", "P", "K", "N"), range(9)))[x[2]]

            def guild_sort(item):
                guild = item[5]
                try: guild_stance = guild_stances[item[5]]
                except KeyError: guild_stance = None
                return (STANCE_KEY[guild_stance], guild)

            items.sort(key=lambda x: tuple([y(x) for y in {
                    'level': (level_sort,),
                    'stance': (stance_sort, level_sort,),
                    'vocation': (vocation_sort, stance_sort, level_sort,),
                    'guild': (guild_sort, level_sort,),
                }[self.list_sort_mode.get()]]))

            listbox_offset = self.listbox.yview()[0]
            listbox_size = self.listbox.size()
            for name, level, vocation, background, stance, guild, death, pzlocked in items:
                fmt = "%3i%3s %-20s"
                vals = [level, vocation, name]
                if guild is not None and self.list_show_guild.get():
                    fmt += " (%s)"
                    vals.append(guild)
                text = fmt % tuple(vals)
                self.listbox.insert(Tkinter.END, text)
                fg = None
                if stance is not None:
                    fg = STANCES[stance][1]
                if death: fg = "magenta"
                if not fg is None:
                    self.listbox.itemconfig(Tkinter.END, fg=fg, selectforeground=fg)
                if not background is None:
                    self.listbox.itemconfig(Tkinter.END, bg=background, selectbackground=background)
                if pzlocked:
                    for opt in ("background", "selectbackground"):
                        #clrstr = self.listbox.itemcget(Tkinter.END, opt) or self.listbox.cget(opt)
                        #fliprgb = tuple([255 - (x >> 8) for x in self.listbox.winfo_rgb(clrstr)])
                        #clrstr = "#" + 3 * "%02x" % fliprgb
                        self.listbox.itemconfig(Tkinter.END, **dict(((opt, "black"),)))
                    for opt in ("foreground", "selectforeground"):
                        clrstr = self.listbox.itemcget(Tkinter.END, opt)
                        if not clrstr: # ie the default color is in use
                            self.listbox.itemconfig(Tkinter.END, **dict(((opt, "white"),)))
            self.listbox_data += [x[0] for x in items]
            self.listbox.delete(0, listbox_size - 1)
            del self.listbox_data[:listbox_size]
            self.listbox.yview_moveto(listbox_offset)
            print "refreshed listbox" + (" (daemon)" if daemonic else ""), time.ctime()
        finally:
            if daemonic:
                self.dialog.after(30000, self.refresh_listbox, True)
