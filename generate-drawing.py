#!/usr/bin/env python3
"""
Script para gerar desenho técnico automaticamente do bus-box.FCStd
Usa o TechDraw workbench do FreeCAD via Python
"""

import FreeCAD as App
import FreeCADGui as Gui
import TechDraw
import os


def generate_technical_drawing():
    """Gera desenho técnico com vistas principais"""

    # Abrir o arquivo
    doc = App.openDocument("bus-box.FCStd")

    # Criar página TechDraw
    page = doc.addObject("TechDraw::DrawPage", "Page")
    doc.addObject("TechDraw::DrawSVGTemplate", "Template")
    page.Template = doc.Template

    # Usar template A4 paisagem
    template_path = (
        App.getResourceDir() + "Mod/TechDraw/Templates/A4_Landscape_ISO7200.svg"
    )
    if os.path.exists(template_path):
        doc.Template.Template = template_path

    # Criar vistas
    # Vista frontal
    view_front = doc.addObject("TechDraw::DrawViewPart", "ViewFront")
    view_front.Source = doc.ActiveObject
    view_front.Direction = (0, 0, 1)
    view_front.X = 100
    view_front.Y = 100
    view_front.Scale = 0.5
    page.addView(view_front)

    # Vista superior
    view_top = doc.addObject("TechDraw::DrawViewPart", "ViewTop")
    view_top.Source = doc.ActiveObject
    view_top.Direction = (0, 1, 0)
    view_top.X = 250
    view_top.Y = 100
    view_top.Scale = 0.5
    page.addView(view_top)

    # Vista lateral
    view_right = doc.addObject("TechDraw::DrawViewPart", "ViewRight")
    view_right.Source = doc.ActiveObject
    view_right.Direction = (1, 0, 0)
    view_right.X = 400
    view_right.Y = 100
    view_right.Scale = 0.5
    page.addView(view_right)

    # Vista isométrica
    view_iso = doc.addObject("TechDraw::DrawViewPart", "ViewIso")
    view_iso.Source = doc.ActiveObject
    view_iso.Direction = (1, 1, 1)
    view_iso.X = 550
    view_iso.Y = 100
    view_iso.Scale = 0.3
    page.addView(view_iso)

    # Recomputar
    doc.recompute()

    # Exportar como SVG
    output_svg = "bus-box-technical-drawing.svg"
    page.ViewObject.exportPage(output_svg)
    print(f"Desenho técnico exportado: {output_svg}")

    # Exportar como PDF (se disponível)
    try:
        output_pdf = "bus-box-technical-drawing.pdf"
        page.ViewObject.exportPage(output_pdf)
        print(f"PDF exportado: {output_pdf}")
    except:
        print("Exportação PDF não disponível, apenas SVG gerado")

    # Salvar documento com o desenho
    doc.saveAs("bus-box-with-drawing.FCStd")

    return output_svg


if __name__ == "__main__":
    # Inicializar GUI (necessário para TechDraw)
    Gui.showMainWindow()
    Gui.activateWorkbench("TechDrawWorkbench")

    # Gerar desenho
    result = generate_technical_drawing()
    print(f"Concluído! Arquivo gerado: {result}")
