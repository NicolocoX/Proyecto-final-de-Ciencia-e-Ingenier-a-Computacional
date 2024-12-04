import tkinter as tk
import numpy as np
import random


class Pez:
  esta_huyendo = False
  dir_rodear_x = None
  dir_rodear_y = None
  esperar = False
  esta_solo = True
  
  def __init__(self, x, y, dir_x = None, dir_y = None):
    self.pos_x = x
    self.pos_y = y
    
    if dir_x == None  or  dir_y == None:
      self.definir_direccion()
    else:
      self.dir_cardumen_x = None
      self.dir_cardumen_y = None
      self.dir_individual_x = dir_x
      self.dir_individual_y = dir_y
      
        
    self.energia = random.randint(8, 10)
  
  
  def definir_direccion(self):
    self.dir_cardumen_x = None
    self.dir_cardumen_y = None
    
    self.dir_individual_x = random.randint(-1, 1)
    self.dir_individual_y = random.randint(-1, 1)
    
    while self.dir_individual_x == 0  and  self.dir_individual_y == 0:
      if random.randint(0, 1):
        self.dir_individual_x = random.randint(-1, 1)
      else:
        self.dir_individual_y = random.randint(-1, 1)
  
  
  def rodear_muro(self, dir_actual_x, dir_actual_y):
    self.dir_cardumen_x = None
    
    # Se obtiene una dir para rodear
    self.dir_rodear_x = dir_actual_x
    self.dir_rodear_y = dir_actual_y
    
    if dir_actual_x == 0:
      if dir_actual_y == 1:
        self.dir_rodear_x = 1
      else:
        self.dir_rodear_x = -1
        
    elif dir_actual_y == 0:
      if dir_actual_x == 1:
        self.dir_rodear_y = -1
      else:
        self.dir_rodear_y = 1
    
    else:
      if dir_actual_x == dir_actual_y:
        self.dir_rodear_y = 0
      else:
        self.dir_rodear_x = 0
        
    # Se obtiene una dir perpendicular
    self.dir_individual_x = self.dir_rodear_y * -1
    self.dir_individual_y = self.dir_rodear_x
    
    #print("Rodear:", self.dir_rodear_x, self.dir_rodear_y, "Individual:", self.dir_individual_x, self.dir_individual_y)
    
    
   
class Tiburon:
  esta_cazando = False
  
  def __init__(self, pos_x, pos_y):
    self.pos_x = pos_x 
    self.pos_y = pos_y
    
    self.definir_direccion()
    
    self.energia = random.randint(9, 10)
    
  def definir_direccion(self):
    self.dir_individual_x = random.randint(-1, 1)
    self.dir_individual_y = random.randint(-1, 1)
    
    while self.dir_individual_x == 0  and  self.dir_individual_y == 0:
      if random.randint(0, 1):
        self.dir_individual_x = random.randint(-1, 1)
      else:
        self.dir_individual_y = random.randint(-1, 1)
    
    

class Arrecife:
  def __init__(self, root, width=500, height=500, cell_size=10):
      self.width = width
      self.height = height
      self.cell_size = cell_size
      self.cols = self.width // self.cell_size
      self.rows = self.height // self.cell_size
      self.grid = np.zeros((self.cols, self.rows), dtype=int)
      self.entidad = tk.StringVar(value="white")
      self.iterando = False
      self.cont_giro_peces = 40
      self.vision_lateral = tk.BooleanVar()
      
      self.peces = []
      self.muros = []
      self.tiburones = []
      self.cuevas = []
      
      
      self.crear_widgets(root)
      
      self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
      self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
      
      self.inicializar_grilla()
  
  
  def inicializar_grilla(self):
    self.canvas.delete("all")
    
    for x in range(self.cols): 
      for y in range(self.rows):
        rect_id = self.canvas.create_rectangle(
          x * self.cell_size, y * self.cell_size, 
          (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
          fill='white'
        )
        self.canvas.tag_bind(rect_id, '<Button-1>', self.interaccion_celda)


  def interaccion_celda(self, event):
    global matriz_arrecife
    
    x = event.x
    y = event.y
    if x < self.width and y < self.height: 
      col = x // self.cell_size
      row = y // self.cell_size
      
      color = self.entidad.get()
      
      
      if color == "blue":
        for muro in self.muros:
          if col == muro[0]  and  row == muro[1]:
            self.muros.remove(muro)
            
        for tiburon in self.tiburones:
          if col == tiburon.pos_x  and  row == tiburon.pos_y:
            self.tiburones.remove(tiburon)
        
        for cueva in self.cuevas:
          if col == cueva[0]  and  row == cueva[1]:
            self.cuevas.remove(cueva)
        
        try:
          dir_x = int(self.text_entry_x.get())
          dir_y = int(self.text_entry_y.get())
          self.peces.append(Pez(col, row, dir_x, dir_y))
        except:
          self.peces.append(Pez(col, row))
          
      
      
      elif color == "white":
        for pez in self.peces:
          if col == pez.pos_x  and  row == pez.pos_y:
            self.peces.remove(pez)
            break
        
        for muro in self.muros:
          if col == muro[0] and  row == muro[1]:
            self.muros.remove(muro)
            break
        
        for tiburon in self.tiburones:
          if col == tiburon.pos_x and  row == tiburon.pos_y:
            self.tiburones.remove(tiburon)
            break
        
        for cueva in self.cuevas:
          if col == cueva[0]  and  row == cueva[1]:
            self.cuevas.remove(cueva)
            
      
      elif color == "black":
        for pez in self.peces:
          if col == pez.pos_x  and  row == pez.pos_y:
            self.peces.remove(pez)
        
        for tiburon in self.tiburones:
          if col == tiburon.pos_x  and  row == tiburon.pos_y:
            self.tiburones.remove(tiburon)
        
        for cueva in self.cuevas:
          if col == cueva[0]  and  row == cueva[1]:
            self.cuevas.remove(cueva)
        
        self.muros.append((col, row))
        
      
      elif color == "red":
        for pez in self.peces:
          if col == pez.pos_x  and  row == pez.pos_y:
            self.peces.remove(pez)
        
        for muro in self.muros:
          if col == muro[0]  and  row == muro[1]:
            self.muros.remove(muro)
        
        for cueva in self.cuevas:
          if col == cueva[0]  and  row == cueva[1]:
            self.cuevas.remove(cueva)
        
        self.tiburones.append(Tiburon(col, row))
      
      
      elif color == "green":
        for pez in self.peces:
          if col == pez.pos_x  and  row == pez.pos_y:
            self.peces.remove(pez)
            
        for tiburon in self.tiburones:
          if col == tiburon.pos_x  and  row == tiburon.pos_y:
            self.tiburones.remove(tiburon)
        
        for muro in self.muros:
          if col == muro[0]  and  row == muro[1]:
            self.muros.remove(muro)
        
        self.cuevas.append((col, row))
        
        
      self.actualizar_canvas()
        
        
  def actualizar_canvas(self):
    self.inicializar_grilla()
    
    
    for pez in self.peces:
      x = pez.pos_x
      y = pez.pos_y
      
      if pez.esta_solo:
        color = "purple"
      else:
        color = "blue"
      
      rect_id = self.canvas.create_rectangle(
        x * self.cell_size, y * self.cell_size, 
        (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
        fill=color
      )
      self.canvas.tag_bind(rect_id, '<Button-1>', self.interaccion_celda)
    
    
    for muro in self.muros:
      x = muro[0]
      y = muro[1]
      
      rect_id = self.canvas.create_rectangle(
        x * self.cell_size, y * self.cell_size, 
        (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
        fill="black"
      )
      self.canvas.tag_bind(rect_id, '<Button-1>', self.interaccion_celda)
      
    
    for tiburon in self.tiburones:
      x = tiburon.pos_x
      y = tiburon.pos_y
      
      rect_id = self.canvas.create_rectangle(
        x * self.cell_size, y * self.cell_size, 
        (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
        fill="red"
      )
      self.canvas.tag_bind(rect_id, '<Button-1>', self.interaccion_celda)
    
    
    for cueva in self.cuevas:
      x = cueva[0]
      y = cueva[1]
      
      rect_id = self.canvas.create_rectangle(
        x * self.cell_size, y * self.cell_size, 
        (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
        fill="green"
      )
      self.canvas.tag_bind(rect_id, '<Button-1>', self.interaccion_celda)
      
      
  def crear_widgets(self, root):
    control_frame = tk.Frame(root, bg="lightgray", width=200)
    control_frame.pack(side=tk.LEFT, fill=tk.Y)
    
    
    r1 = tk.Radiobutton(control_frame, text="Pez", variable=self.entidad, value="blue", bg="lightgray")
    r1.pack(anchor="w", pady=5, padx=10)
    
    label_frame = tk.Frame(control_frame, bg="lightgray")
    label_frame.pack(anchor="w", pady=5, padx=1)
    
    label = tk.Label(label_frame, text="Dirección x:", bg="lightgray")
    label.pack(side=tk.LEFT)
    
    self.text_entry_x = tk.Entry(label_frame, width=2)
    self.text_entry_x.pack(side=tk.LEFT)
    
    
    label_frame = tk.Frame(control_frame, bg="lightgray")
    label_frame.pack(anchor="w", pady=5, padx=1)
    
    label = tk.Label(label_frame, text="Dirección y:", bg="lightgray")
    label.pack(side=tk.LEFT)
    
    self.text_entry_y = tk.Entry(label_frame, width=2)
    self.text_entry_y.pack(side=tk.LEFT)
    
    
    label_frame = tk.Frame(control_frame, bg="lightgray")
    label_frame.pack(anchor="w", pady=5, padx=1)
    
    label = tk.Label(label_frame, text="Porcentaje de giro:", bg="lightgray")
    label.pack(side=tk.LEFT)
    
    self.text_entry_porcentaje = tk.Entry(label_frame, width=3)
    self.text_entry_porcentaje.pack(side=tk.LEFT)
    
    self.checkbutton = tk.Checkbutton(control_frame, text="Visión lateral", variable=self.vision_lateral, bg="lightgray")
    self.checkbutton.pack(anchor="w", pady=5, padx=10)
    
    
    r2 = tk.Radiobutton(control_frame, text="Tiburón", variable=self.entidad, value="red", bg="lightgray")
    r2.pack(anchor="w", pady=5, padx=10)
    
    r3 = tk.Radiobutton(control_frame, text="Muro", variable=self.entidad, value="black", bg="lightgray")
    r3.pack(anchor="w", pady=5, padx=10)
    
    r3 = tk.Radiobutton(control_frame, text="Cueva", variable=self.entidad, value="green", bg="lightgray")
    r3.pack(anchor="w", pady=5, padx=10)
    
    r4 = tk.Radiobutton(control_frame, text="Borrar", variable=self.entidad, value="white", bg="lightgray")
    r4.pack(anchor="w", pady=5, padx=10)
    
    self.boton_iterar = tk.Button(control_frame, text="Iterar", command=self.iniciar)
    self.boton_iterar.pack()
    
    self.boton_actualizar = tk.Button(control_frame, text="Actualizar", command=self.actualizar)
    self.boton_actualizar.pack()
    
    self.boton_cerrar_mundo = tk.Button(control_frame, text="Cerrar mundo", command=self.cerrar_mundo)
    self.boton_cerrar_mundo.pack()
    
    self.boton_reiniciar = tk.Button(control_frame, text="Reiniciar", command=self.reiniciar)
    self.boton_reiniciar.pack()
  
  
  def cerrar_mundo(self):
    for col in range(self.cols):
      self.muros.append((col, 0))
      self.muros.append((col, self.rows - 1))
    
    for row in range(1, self.rows - 1):
      self.muros.append((0, row))
      self.muros.append((self.cols - 1, row))
      
    self.actualizar_canvas()
  
  
  def reiniciar(self):
    self.peces = []
    self.muros = []
    self.tiburones = []
    self.cuevas = []
    self.cont_giro_peces = 40
    
    self.actualizar_canvas()
  
  
  def iniciar(self):
    self.iterando = not self.iterando
    if self.iterando:
      self.boton_iterar.config(text="Pausar")
    else:
      self.boton_iterar.config(text="Iterar")
    
    self.iterar()
      
      
  def iterar(self):
    if self.iterando:
      self.actualizar()
      
      self.cont_giro_peces -= 1
      if self.cont_giro_peces == 0:
        self.cont_giro_peces = 40
        self.girar_peces()
        
      self.canvas.after(150, self.iterar)
  
  
  def girar_peces(self):
    print("Giro de peces")
    
    try:
      porcentaje = float(self.text_entry_porcentaje.get())
      num_elementos = int(len(self.peces) * porcentaje)
      porcentaje_peces = random.sample(self.peces, num_elementos)
      for pez in porcentaje_peces:
        pez.definir_direccion()
    except:
      pass
    
  
  def actualizar(self):
    self.actualizar_peces()
    self.actualizar_tiburones()
    
    self.actualizar_canvas()
  
  
  def actualizar_tiburones(self):
    for tiburon in self.tiburones:
      
      tiburon.definir_direccion()
      
      hay_muro = True
      while hay_muro:
        dir_x = tiburon.dir_individual_x
        dir_y = tiburon.dir_individual_y
        
        hay_muro = self.evitar_muros_tiburones(tiburon, dir_x, dir_y)

      self.buscar_pez(tiburon)
      
      dir_x = tiburon.dir_individual_x
      dir_y = tiburon.dir_individual_y
      
      siguiente_pos_x = (tiburon.pos_x + dir_x) % self.cols
      siguiente_pos_y = (tiburon.pos_y + dir_y) % self.rows
      
      se_mueve = True
      for otro_tiburon in self.tiburones:
        if tiburon != otro_tiburon:
          if siguiente_pos_x == otro_tiburon.pos_x  and  siguiente_pos_y == otro_tiburon.pos_y: # posicion ocupada
            se_mueve = False
            break
          
          
      if tiburon.energia == 0:
        tiburon.esta_cazando = False
      
      if (tiburon.esta_cazando  or  tiburon.energia > 10)  and  se_mueve:
        tiburon.pos_x = siguiente_pos_x
        tiburon.pos_y = siguiente_pos_y
        
        self.comer_pez(tiburon)
        
        tiburon.energia -= 1
      else:
        tiburon.energia += 1
  
  
  def normalizar_a_rango(self, num):
    if num == 0:
        return 0  # Evita división por cero
    return num / abs(num) 
  
  
  def buscar_pez(self, tiburon):
    for eje_x in range(-2, 3):
      for eje_y in range(-2, 3):
        if not (eje_x == 0  and  eje_y == 0):
          siguiente_pos_x = (tiburon.pos_x + eje_x) % self.cols
          siguiente_pos_y = (tiburon.pos_y + eje_y) % self.rows
        
          for pez in self.peces:
            if siguiente_pos_x == pez.pos_x  and  siguiente_pos_y == pez.pos_y:
              tiburon.dir_individual_x = self.normalizar_a_rango(eje_x)
              tiburon.dir_individual_y = self.normalizar_a_rango(eje_y)
              
              tiburon.esta_cazando = True
              print("Cazando")
              break
            
        
  def comer_pez(self, tiburon): 
    for pez in self.peces:
      if tiburon.pos_x == pez.pos_x  and  tiburon.pos_y == pez.pos_y:
        self.peces.remove(pez)
        print("Pez devorado")
        
        tiburon.esta_cazando = False
        break
        
        
  def revisar_vecinos_tiburones(self, tiburon):
    siguiente_pos_x = (tiburon.pos_x + tiburon.dir_individual_x) % self.cols
    siguiente_pos_y = (tiburon.pos_y + tiburon.dir_individual_y) % self.rows
    
    for otro_tiburon in self.tiburones:
      if siguiente_pos_x == otro_tiburon.pos_x  and  siguiente_pos_y == otro_tiburon.pos_y:
        tiburon.definir_direccion()
        break
  
  
  def actualizar_peces(self):
    peces_asalvo = []
    
    for pez in self.peces:
      dir_contraria = self.revisar_vecinos(pez) # revisa peces y tiburones
      
      hay_muro = True
      while hay_muro:
        if dir_contraria:
          dir_x = dir_contraria[0]
          dir_y = dir_contraria[1]
          dir_contraria = None
        else:
          if pez.dir_cardumen_x != None:
            dir_x = pez.dir_cardumen_x
            dir_y = pez.dir_cardumen_y
          else:
            dir_x = pez.dir_individual_x
            dir_y = pez.dir_individual_y
            
        if pez.dir_rodear_x != None:
          dir_x = pez.dir_rodear_x
          dir_y = pez.dir_rodear_y
        
        hay_muro = self.evitar_muros_peces(pez, dir_x, dir_y)
      

      siguiente_pos_x = (pez.pos_x + dir_x) % self.cols
      siguiente_pos_y = (pez.pos_y + dir_y) % self.rows
      
      # revisa si el pez se puede mover ahi
      pos_desocupada = True
      for otro_pez in self.peces:
        if pez != otro_pez:
          if siguiente_pos_x == otro_pez.pos_x  and  siguiente_pos_y == otro_pez.pos_y:
            pos_desocupada = False
            break
      
      
      if pez.energia <= 0:
        pez.esta_huyendo = False
        pez.esperar = False
      
      if (pez.esta_huyendo  or  pez.energia > 10)  and  pos_desocupada:
        if not pez.esperar:
          pez.pos_x = siguiente_pos_x
          pez.pos_y = siguiente_pos_y

          pez.dir_rodear_x = None

          pez.energia -= 2
          
          for cueva in self.cuevas:
            if pez.pos_x == cueva[0]  and  pez.pos_y == cueva[1]:
              peces_asalvo.append(pez)
              break
            
        if pez.esta_huyendo:
          pez.esperar = not pez.esperar
      else:
        pez.energia += 1
        
    
    for pez in peces_asalvo:
      self.peces.remove(pez)
        
  
  def revisar_vecinos(self, pez):
    vecinos_eje_x = []
    vecinos_eje_y = []
    
    vecinos_dir_x = []
    vecinos_dir_y = []
    
    if self.vision_lateral.get():
      if pez.dir_cardumen_x == None:
        dir_x = pez.dir_cardumen_x
        dir_y = pez.dir_cardumen_y
      else:
        dir_x = pez.dir_individual_x
        dir_y = pez.dir_individual_y
      
    
    for eje_x in (-2, -1, 0, 1, 2):
      for eje_y in (-2, -1, 0, 1, 2):
        if not (eje_x == 0  and  eje_y == 0): 
          
          es_lateral = True
          if self.vision_lateral.get(): # Revisa si los vecinos son los laterales
            if dir_y == 0:
              if eje_y == 0:
                es_lateral = False
              
            elif dir_x == 0:
              if eje_x == 0:
                es_lateral = False
              
            elif dir_x == dir_y:
              if eje_x == eje_y:
                es_lateral = False
              
            elif dir_x != dir_y:
              if eje_x == (eje_y * -1):
                es_lateral = False
          
           
          if es_lateral:
            vecino_x = (pez.pos_x + eje_x) % self.cols
            vecino_y = (pez.pos_y + eje_y) % self.cols
            
            for tiburon in self.tiburones:
              if vecino_x == tiburon.pos_x  and  vecino_y == tiburon.pos_y: 
                pez.dir_individual_x = self.normalizar_a_rango(eje_x) * -1
                pez.dir_individual_y = self.normalizar_a_rango(eje_y) * -1
                
                pez.dir_cardumen_x = None
                pez.esta_huyendo = True
                print("Está huyendo")
                return
            
            for otro_pez in self.peces:
              if pez != otro_pez:
                
                if vecino_x == otro_pez.pos_x  and  vecino_y == otro_pez.pos_y:
                  if (eje_x < 2 and eje_x > -2)  and  (eje_y < 2 and eje_y > -2):
                    vecinos_eje_x.append(eje_x)
                    vecinos_eje_y.append(eje_y)
                  
                  vecinos_dir_x.append(otro_pez.dir_individual_x)
                  vecinos_dir_y.append(otro_pez.dir_individual_y)
              
              
    if vecinos_dir_x: # regla alineación
      vecinos_dir_x.append(pez.dir_individual_x)
      vecinos_dir_y.append(pez.dir_individual_y)
      
      
      if np.mean(vecinos_dir_x) >= 0.5:
        pez.dir_cardumen_x = 1
      elif np.mean(vecinos_dir_x) <= -0.5:
        pez.dir_cardumen_x = -1
      else:
        pez.dir_cardumen_x = 0
      
      if np.mean(vecinos_dir_y) >= 0.5:
        pez.dir_cardumen_y = 1
      elif np.mean(vecinos_dir_y) <= -0.5:
        pez.dir_cardumen_y = -1
      else:
        pez.dir_cardumen_y = 0
    
      
      if pez.dir_cardumen_x == 0  and  pez.dir_cardumen_y == 0: # para que los peces no se queden quietos
        pez.dir_cardumen_x = None
      
      pez.esta_solo = False
    else:
      pez.esta_solo = True
      
     
    if vecinos_eje_x: # regla separación
      siguiente_dir_x = round(np.mean(vecinos_eje_x)) * -1
      siguiente_dir_y = round(np.mean(vecinos_eje_y)) * -1
      
      return (siguiente_dir_x, siguiente_dir_y)
      
  
  def evitar_muros_peces(self, pez, dir_x, dir_y):
    pos_x = pez.pos_x + dir_x
    pos_y = pez.pos_y + dir_y
    
    for muro in self.muros:
      if pos_x == muro[0]  and  pos_y == muro[1]:
        pez.rodear_muro(dir_x, dir_y)
        return True
    
    pos_x += dir_x
    pos_y += dir_y
    
    for muro in self.muros:
      if pos_x == muro[0]  and  pos_y == muro[1]:
        pez.rodear_muro(dir_x, dir_y)
        return True
    
    return False
  
  
  def evitar_muros_tiburones(self, pez, dir_x, dir_y):
    pos_x = pez.pos_x + dir_x
    pos_y = pez.pos_y + dir_y
    
    for muro in self.muros:
      if pos_x == muro[0]  and  pos_y == muro[1]:
        pez.definir_direccion()
        return True
    
    for cueva in self.cuevas:
      if pos_x == cueva[0]  and  pos_y == cueva[1]:
        pez.definir_direccion()
        return True
    
    
    pos_x += dir_x
    pos_y += dir_y
    
    for muro in self.muros:
      if pos_x == muro[0]  and  pos_y == muro[1]:
        pez.definir_direccion()
        return True
    
    for cueva in self.cuevas:
      if pos_x == cueva[0]  and  pos_y == cueva[1]:
        pez.definir_direccion()
        return True
    
    return False




root = tk.Tk()
app = Arrecife(root)
root.mainloop()