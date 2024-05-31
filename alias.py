import tkinter as tk


inp=tk.Tk()
def dialogue():
  alias=ask.get()
  inp.quit()
  return alias


inp.title("Enter Alias:")
inp.minsize(width=80, height=80)

ask = tk.Entry(inp)
ask.place(x=0,y=30)
proceed=tk.Button(text="Enter",command=dialogue)
proceed.place(x=0,y=60)



inp.mainloop()