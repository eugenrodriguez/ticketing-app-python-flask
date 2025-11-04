        import os
        import ctypes
        from ctypes import c_int, POINTER
        import tkinter as tk
        from tkinter import ttk, messagebox

        libname = None
        if os.name == 'nt':
            libname = os.path.join(os.path.dirname(__file__), 'dijkstra_lib', 'dijkstra.dll')
        else:
            libname = os.path.join(os.path.dirname(__file__), 'dijkstra_lib', 'libdijkstra.so')

        def load_lib():
            if not os.path.exists(libname):
                messagebox.showerror('Library not found', f'Compiled library not found: {libname}\\nPlease compile dijkstra.cpp as shared library (see README).')
                return None
            return ctypes.CDLL(libname)

        class App:
            def __init__(self, root):
                self.root = root
                root.title('Dijkstra - Tkinter + ctypes')
                frm = ttk.Frame(root, padding=12)
                frm.grid()

                ttk.Label(frm, text='Example graph: 5 vertices, 9 edges (preloaded)').grid(column=0, row=0, columnspan=3)
                self.text = tk.Text(frm, width=60, height=10)
                self.text.grid(column=0, row=1, columnspan=3)
                example = '5 9\\n1 2 7\\n1 4 2\\n2 3 1\\n2 4 2\\n3 5 4\\n4 2 3\\n4 3 8\\n4 5 5\\n5 3 5\\n1\\n'
                self.text.insert('1.0', example)

                ttk.Button(frm, text='Run (compile lib first)', command=self.run_dijkstra).grid(column=0, row=2)
                ttk.Button(frm, text='Clear', command=lambda: self.text.delete('1.0','end')).grid(column=1, row=2)
                ttk.Button(frm, text='Quit', command=root.quit).grid(column=2, row=2)

                self.output = tk.Text(frm, width=60, height=10)
                self.output.grid(column=0, row=3, columnspan=3, pady=(8,0))

            def run_dijkstra(self):
                lib = load_lib()
                if lib is None:
                    return
                data = self.text.get('1.0','end').strip().split()
                try:
                    it = iter(data)
                    V = int(next(it)); E = int(next(it))
                    src = []; dst = []; wt = []
                    for _ in range(E):
                        u = int(next(it)); v = int(next(it)); w = int(next(it))
                        src.append(u); dst.append(v); wt.append(w)
                    source = int(next(it))
                except Exception as e:
                    messagebox.showerror('Parse error', str(e))
                    return

                arr_type = c_int * len(src)
                src_arr = arr_type(*src)
                dst_arr = arr_type(*dst)
                wt_arr = arr_type(*wt)
                out_dist = (c_int * V)()
                out_prev = (c_int * V)()

                fn = lib.dijkstra_c
                fn.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), c_int, POINTER(c_int), POINTER(c_int)]
                fn.restype = c_int
                res = fn(V, E, src_arr, dst_arr, wt_arr, source, out_dist, out_prev)
                if res != 0:
                    messagebox.showerror('C error', f'dijkstra_c returned {res}')
                    return
                self.output.delete('1.0','end')
                self.output.insert('end', 'Vertex\\tDist\\tPrev\\n')
                for i in range(1, V+1):
                    self.output.insert('end', f'{i}\\t{out_dist[i-1]}\\t{out_prev[i-1]}\\n')

        if __name__ == '__main__':
            root = tk.Tk()
            app = App(root)
            root.mainloop()
