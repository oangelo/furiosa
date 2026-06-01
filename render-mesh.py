#!/usr/bin/env python3
import FreeCAD as App
import FreeCADGui as Gui
import sys
import os

os.chdir("/home/oangelo/git/furiosa")

# Processar cada peça
parts = ["Base", "tampa"]

for part in parts:
    print(f"Renderizando: {part}")
    
    # Abrir documento temporário
    doc = App.openDocument(f"temp-{part}.FCStd")
    
    # Inicializar GUI se necessário
    if not Gui.getMainWindow():
        Gui.showMainWindow()
    
    Gui.setActiveDocument(doc.Name)
    
    view = Gui.ActiveDocument.ActiveView
    
    # Isométrica
    view.viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    view.saveImage(f"bus-box-{part}-isometric.png", 800, 600, "White")
    print(f"  ✓ Isométrica")
    
    # Frontal
    view.viewFront()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    view.saveImage(f"bus-box-{part}-front.png", 800, 600, "White")
    print(f"  ✓ Frontal")
    
    # Superior
    view.viewTop()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    view.saveImage(f"bus-box-{part}-top.png", 800, 600, "White")
    print(f"  ✓ Superior")
    
    # Lateral
    view.viewRight()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    view.saveImage(f"bus-box-{part}-right.png", 800, 600, "White")
    print(f"  ✓ Lateral")
    
    App.closeDocument(doc.Name)

print("Renderização concluída!")
