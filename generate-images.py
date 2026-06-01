#!/usr/bin/env python3
"""
Script para gerar imagens PNG de cada peça do bus-box.FCStd
Usa FreeCADGui de forma mais robusta
"""

import sys
import os

# Configurar FreeCAD
freecad_paths = [
    "/usr/lib/freecad/lib",
    "/usr/lib/freecad/Mod",
    "/usr/share/freecad/Mod",
]

for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

import FreeCAD as App

print("=" * 70)
print("GERADOR DE IMAGENS - BUS BOX (PEÇAS SEPARADAS)")
print("=" * 70)


def generate_part_images():
    """Gera imagens PNG para cada peça separadamente"""

    # Abrir documento
    doc_path = os.path.join(os.getcwd(), "bus-box.FCStd")
    print(f"\nAbrindo documento: {doc_path}")

    if not os.path.exists(doc_path):
        print(f"ERRO: Arquivo não encontrado: {doc_path}")
        return False

    # Abrir documento no FreeCAD
    doc = App.openDocument(doc_path)
    print(f"Documento carregado: {doc.Name}")

    # Encontrar todos os Bodies (peças)
    bodies = []
    for obj in doc.Objects:
        if obj.TypeId == "PartDesign::Body":
            bodies.append(obj)
            print(f"Peça encontrada: {obj.Label}")

    if not bodies:
        print("ERRO: Nenhuma peça encontrada!")
        return False

    # Salvar cada peça como arquivo STEP separado
    print("\nExportando peças como STEP...")
    for body in bodies:
        step_filename = f"bus-box-{body.Label}.step"
        body.Shape.exportStep(step_filename)
        print(f"  ✓ {step_filename}")

    # Salvar informações
    info_filename = "bus-box-parts-info.txt"
    with open(info_filename, "w") as f:
        f.write("BUS BOX - INFORMAÇÕES DAS PEÇAS\n")
        f.write("=" * 50 + "\n\n")

        for i, body in enumerate(bodies, 1):
            f.write(f"Peça {i}: {body.Label}\n")
            f.write(f"  Nome: {body.Name}\n")
            f.write(f"  Tipo: {body.TypeId}\n")

            if hasattr(body, "Shape"):
                bbox = body.Shape.BoundBox
                f.write(f"  Dimensões:\n")
                f.write(f"    Comprimento (X): {bbox.XLength:.2f} mm\n")
                f.write(f"    Largura (Y): {bbox.YLength:.2f} mm\n")
                f.write(f"    Altura (Z): {bbox.ZLength:.2f} mm\n")
                f.write(f"  Volume: {body.Shape.Volume:.2f} mm³\n")

            f.write("\n")

    print(f"\nInformações salvas: {info_filename}")

    # Criar script para renderização com GUI
    render_script = (
        """
import FreeCAD as App
import FreeCADGui as Gui
import sys
import os

# Configurar caminhos
os.chdir('"""
        + os.getcwd()
        + """')

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
"""
    )

    render_script_file = "render-parts.py"
    with open(render_script_file, "w") as f:
        f.write(render_script)

    print(f"\nScript de renderização criado: {render_script_file}")
    print("Para gerar as imagens PNG, execute:")
    print(f"  freecad {render_script_file}")

    print("\n" + "=" * 70)
    print("PEÇAS EXPORTADAS COMO STEP!")
    print("=" * 70)
    print("\nArquivos gerados:")
    for body in bodies:
        print(f"  - bus-box-{body.Label}.step")
    print(f"  - {info_filename}")
    print(f"  - {render_script_file} (para gerar PNGs)")

    return True


if __name__ == "__main__":
    success = generate_part_images()
    sys.exit(0 if success else 1)
