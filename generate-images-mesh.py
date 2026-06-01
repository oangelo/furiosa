#!/usr/bin/env python3
"""
Script para gerar imagens PNG de cada peça do bus-box.FCStd
Usa FreeCAD com offscreen rendering
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
import Part
import Mesh

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

    # Para cada peça, exportar como STL e gerar imagem via mesh
    for body in bodies:
        print(f"\nProcessando: {body.Label}")

        # Exportar como STL
        stl_file = f"bus-box-{body.Label}.stl"
        body.Shape.exportStl(stl_file)
        print(f"  ✓ STL exportado: {stl_file}")

        # Carregar mesh
        mesh = Mesh.Mesh(stl_file)

        # Criar documento temporário para visualização
        temp_doc = App.newDocument(f"Temp_{body.Label}")
        mesh_obj = temp_doc.addObject("Mesh::Feature", "Mesh")
        mesh_obj.Mesh = mesh
        temp_doc.recompute()

        # Salvar como FCStd temporário
        temp_fcstd = f"temp-{body.Label}.FCStd"
        temp_doc.saveAs(temp_fcstd)
        App.closeDocument(temp_doc.Name)

        print(f"  ✓ Documento temporário criado: {temp_fcstd}")

    # Criar script para renderização com FreeCAD GUI
    render_script = (
        '''#!/usr/bin/env python3
import FreeCAD as App
import FreeCADGui as Gui
import sys
import os

os.chdir("'''
        + os.getcwd()
        + """")

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
"""
    )

    render_file = "render-mesh.py"
    with open(render_file, "w") as f:
        f.write(render_script)

    print(f"\n✓ Script de renderização criado: {render_file}")
    print(f"\nPara gerar as imagens PNG, execute manualmente:")
    print(f"  freecad {render_file}")
    print(f"\nOu no FreeCAD GUI:")
    print(f"  1. Abra cada arquivo temp-*.FCStd")
    print(f"  2. Use File → Export para salvar como PNG")

    # Limpar arquivos STL temporários
    for body in bodies:
        stl_file = f"bus-box-{body.Label}.stl"
        if os.path.exists(stl_file):
            os.remove(stl_file)
            print(f"\n  ✓ Arquivo temporário removido: {stl_file}")

    print("\n" + "=" * 70)
    print("ARQUIVOS TEMPORÁRIOS CRIADOS!")
    print("=" * 70)
    print("\nArquivos gerados:")
    for body in bodies:
        print(f"  - temp-{body.Label}.FCStd (abra no FreeCAD GUI)")
    print(f"  - {render_file} (script para renderização automática)")

    return True


if __name__ == "__main__":
    success = generate_part_images()
    sys.exit(0 if success else 1)
