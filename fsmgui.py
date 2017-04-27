import tkinter as tk

class Window(tk.Tk):
	def __init__(self, callback):
		super().__init__()
		self.title('6) REPEAT <оператор присваивания> UNTIL <условие>;')
		self.input = tk.Text(self)
		self.input.grid(row = 0, column = 0, rowspan = 3, sticky='nswe')
		self.input.tag_config("err", background="red", foreground="white")
		# self.input.bind("<Button-1>",  lambda x: self.setError(-1))
		self.input.bind("<KeyRelease>",  lambda x: callback(self.text()))
		# self.button = tk.Button(self, text = 'Validate', command = lambda: callback(self.text()))
		# self.button.grid(row = 0, column = 1, sticky='nswe')
		self.status = tk.StringVar()
		self.status.set('Status:')
		self.statusw = tk.Label(self, textvariable=self.status, justify=tk.LEFT)
		self.statusw.grid(row = 0, column = 1, sticky='nw')
		self.textview = tk.Text(self, state=tk.DISABLED, width = 20)
		self.textview.grid(row = 1, column = 1, sticky='nswe')
		tk.Grid.columnconfigure(self, 0, weight=30)
		tk.Grid.columnconfigure(self, 1, weight=1)
		tk.Grid.rowconfigure(self, 0, weight=1)
		# tk.Grid.rowconfigure(self, 1, weight=1)
		tk.Grid.rowconfigure(self, 1, weight=30)
	def text(self):
		result = self.input.get(1.0, tk.END)
		result = result[0:len(result)-1]
		return result
	def set_status(self, status):
		self.status.set(status)
	def set_semantics(self, semantics):
		self.textview['state'] = tk.NORMAL
		self.textview.delete(1.0, tk.END)
		self.textview.insert(tk.END, semantics)
		self.textview['state'] = tk.DISABLED
	def set_error(self, pos, end_pos = -1):
		self.input.tag_remove('err', 1.0, tk.END)
		if pos >= 0:
			end = tk.END
			if end_pos >= 0:
				end = '1.'+str(end_pos)
			self.input.tag_add('err', '1.'+str(pos), end)
	def reset(self):
		self.set_semantics('')
		self.set_error(-1)
