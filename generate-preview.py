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

print("=" * 60)
print("GERADOR DE PREVIEW - BUS BOX")
print("=" * 60)


def main():
    # Abrir documento
    doc_path = os.path.join(os.getcwd(), "bus-box.FCStd")
    print(f"\nAbrindo documento: {doc_path}")

    if not os.path.exists(doc_path):
        print(f"ERRO: Arquivo não encontrado: {doc_path}")
        return False

    doc = App.openDocument(doc_path)
    print(f"Documento carregado: {doc.Name}")
    print(f"Total de objetos: {len(doc.Objects)}")

    # Listar todos os objetos
    print("\n--- Objetos no documento ---")
    for obj in doc.Objects:
        print(f"  {obj.Name}: {obj.Label} (Type: {obj.TypeId})")
        if hasattr(obj, "Shape"):
            vol = obj.Shape.Volume
            if vol > 0:
                print(f"    Volume: {vol:.2f} mm³")

    # Encontrar objeto principal (com maior volume)
    main_obj = None
    max_volume = 0

    for obj in doc.Objects:
        if hasattr(obj, "Shape") and obj.Shape.Volume > max_volume:
            max_volume = obj.Shape.Volume
            main_obj = obj

    if not main_obj:
        print("\nERRO: Nenhum objeto sólido encontrado!")
        return False

    print(f"\n--- Objeto Principal ---")
    print(f"Nome: {main_obj.Name}")
    print(f"Label: {main_obj.Label}")
    print(f"Volume: {max_volume:.2f} mm³")

    # Calcular dimensões
    bbox = main_obj.Shape.BoundBox
    print(f"\n--- Dimensões ---")
    print(f"Comprimento (X): {bbox.XLength:.2f} mm")
    print(f"Largura (Y): {bbox.YLength:.2f} mm")
    print(f"Altura (Z): {bbox.ZLength:.2f} mm")

    # Exportar STL
    stl_file = os.path.join(os.getcwd(), "bus-box-preview.stl")
    print(f"\nExportando STL: {stl_file}")
    main_obj.Shape.exportStl(stl_file)

    if os.path.exists(stl_file):
        size = os.path.getsize(stl_file)
        print(f"STL gerado com sucesso! Tamanho: {size} bytes")
    else:
        print("ERRO: Falha ao gerar STL")
        return False

    # Salvar informações em texto
    info_file = os.path.join(os.getcwd(), "bus-box-info.txt")
    with open(info_file, "w") as f:
        f.write("BUS BOX - INFORMAÇÕES DO MODELO\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Arquivo: bus-box.FCStd\n")
        f.write(f"Objeto: {main_obj.Label}\n")
        f.write(f"Volume: {max_volume:.2f} mm³\n\n")
        f.write("Dimensões:\n")
        f.write(f"  Comprimento (X): {bbox.XLength:.2f} mm\n")
        f.write(f"  Largura (Y): {bbox.YLength:.2f} mm\n")
        f.write(f"  Altura (Z): {bbox.ZLength:.2f} mm\n")

    print(f"Informações salvas: {info_file}")
    print("\n" + "=" * 60)
    print("CONCLUÍDO COM SUCESSO!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
