
import FreeCAD as App
import FreeCADGui as Gui
import sys
import os

# Configurar caminhos
os.chdir('/home/oangelo/git/furiosa')

# Abrir documento
doc = App.openDocument("bus-box.FCStd")
Gui.showMainWindow()
Gui.setActiveDocument(doc.Name)

# Encontrar bodies
bodies = [obj for obj in doc.Objects if obj.TypeId == 'PartDesign::Body']

for body in bodies:
    print(f"Renderizando: {body.Label}")
    
    # Esconder todos
    for b in bodies:
        if hasattr(b, 'ViewObject'):
            b.ViewObject.Visibility = False
    
    # Mostrar atual
    if hasattr(body, 'ViewObject'):
        body.ViewObject.Visibility = True
    
    view = Gui.ActiveDocument.ActiveView
    
    # Isométrica
    view.viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    view.saveImage(f"bus-box-{body.Label}-isometric.png", 800, 600, 'White')
    
    # Frontal
    view.viewFront()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    view.saveImage(f"bus-box-{body.Label}-front.png", 800, 600, 'White')
    
    # Superior
    view.viewTop()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    view.saveImage(f"bus-box-{body.Label}-top.png", 800, 600, 'White')
    
    # Lateral
    view.viewRight()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    view.saveImage(f"bus-box-{body.Label}-right.png", 800, 600, 'White')

# Vista completa
for b in bodies:
    if hasattr(b, 'ViewObject'):
        b.ViewObject.Visibility = True

view.viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
Gui.updateGui()
view.saveImage("bus-box-complete-isometric.png", 800, 600, 'White')

print("Renderização concluída!")
App.closeDocument(doc.Name)
Gui.getMainWindow().close()
