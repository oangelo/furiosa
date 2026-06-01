#!/usr/bin/env python3
"""
Script para gerar desenho técnico automaticamente do bus-box.FCStd
Usa TechDraw workbench do FreeCAD via Python
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
import TechDraw

print("=" * 70)
print("GERADOR DE DESENHO TÉCNICO - BUS BOX")
print("=" * 70)


def generate_technical_drawing():
    """Gera desenho técnico com vistas ortográficas"""

    # Abrir documento
    doc_path = os.path.join(os.getcwd(), "bus-box.FCStd")
    print(f"\nAbrindo documento: {doc_path}")

    if not os.path.exists(doc_path):
        print(f"ERRO: Arquivo não encontrado: {doc_path}")
        return False

    doc = App.openDocument(doc_path)
    print(f"Documento carregado: {doc.Name}")

    # Encontrar objeto principal (Body da base)
    main_obj = None
    for obj in doc.Objects:
        if obj.Name == "Body":  # Corpo principal (base)
            main_obj = obj
            print(f"Objeto principal encontrado: {obj.Label}")
            break

    if not main_obj:
        print("ERRO: Objeto Body não encontrado!")
        return False

    # Criar página TechDraw
    print("\nCriando página TechDraw...")
    page = doc.addObject("TechDraw::DrawPage", "Page")
    template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")

    # Usar template A4 paisagem padrão do FreeCAD
    template_path = (
        App.getResourceDir() + "Mod/TechDraw/Templates/A4_Landscape_ISO7200.svg"
    )
    if os.path.exists(template_path):
        template.Template = template_path
        print(f"Template carregado: {template_path}")
    else:
        print(f"AVISO: Template não encontrado: {template_path}")
        print("Criando página sem template...")

    page.Template = template

    # Criar grupo de projeções (vistas ortográficas)
    print("\nCriando vistas ortográficas...")
    proj_group = doc.addObject("TechDraw::DrawProjGroup", "ProjGroup")
    proj_group.Source = main_obj
    page.addView(proj_group)

    # Configurar escala
    proj_group.Scale = 1.0  # Escala 1:1 (ajustar conforme necessário)

    # Adicionar projeções principais
    projections = [
        ("Front", "Frontal"),
        ("Top", "Superior"),
        ("Right", "Lateral Direita"),
    ]

    for proj_type, label in projections:
        try:
            item = proj_group.addProjection(proj_type)
            print(f"  ✓ Vista {label} ({proj_type}) adicionada")
        except Exception as e:
            print(f"  ✗ Erro ao adicionar vista {label}: {e}")

    # Adicionar vista isométrica separada
    print("\nAdicionando vista isométrica...")
    iso_view = doc.addObject("TechDraw::DrawViewPart", "ViewIso")
    iso_view.Source = main_obj
    iso_view.Direction = (1, 1, 1)  # Direção isométrica
    iso_view.X = 250
    iso_view.Y = 150
    iso_view.Scale = 0.8
    page.addView(iso_view)
    print("  ✓ Vista isométrica adicionada")

    # Recomputar documento
    print("\nRecomputando documento...")
    doc.recompute()

    # Salvar documento com desenho técnico
    output_fcstd = os.path.join(os.getcwd(), "bus-box-technical-drawing.FCStd")
    doc.saveAs(output_fcstd)
    print(f"\nDocumento salvo: {output_fcstd}")

    # Exportar como SVG
    try:
        output_svg = os.path.join(os.getcwd(), "bus-box-technical-drawing.svg")
        page.ViewObject.exportPage(output_svg)
        print(f"SVG exportado: {output_svg}")
    except Exception as e:
        print(f"AVISO: Não foi possível exportar SVG: {e}")

    # Exportar como DXF
    try:
        output_dxf = os.path.join(os.getcwd(), "bus-box-technical-drawing.dxf")
        TechDraw.writeDXFPage(page, output_dxf)
        print(f"DXF exportado: {output_dxf}")
    except Exception as e:
        print(f"AVISO: Não foi possível exportar DXF: {e}")

    print("\n" + "=" * 70)
    print("DESENHO TÉCNICO GERADO COM SUCESSO!")
    print("=" * 70)
    print("\nArquivos gerados:")
    print(f"  - bus-box-technical-drawing.FCStd (FreeCAD com desenho)")
    print(f"  - bus-box-technical-drawing.svg (Vetorial)")
    print(f"  - bus-box-technical-drawing.dxf (CAD)")

    return True


if __name__ == "__main__":
    success = generate_technical_drawing()
    sys.exit(0 if success else 1)
