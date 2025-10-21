Branch 2 - Tkinter + ctypes + C++ Dijkstra
------------------------------------------

Steps to use:

1) Compile the C++ shared library.
   - Linux:
     g++ -O2 -shared -fPIC dijkstra.cpp -o libdijkstra.so
     (run from inside dijkstra_lib directory)
   - Windows (MinGW):
     g++ -O2 -shared -static-libgcc -static-libstdc++ -o dijkstra.dll dijkstra.cpp

2) Run Python Tkinter app:
     python tk_app.py

The app contains a preloaded example. If the compiled library is not found it will show instructions.
