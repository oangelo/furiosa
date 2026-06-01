#!/usr/bin/env python3
"""
Script para gerar imagens PNG de cada peça do bus-box.FCStd
Usa OpenSCAD para renderizar vistas ortográficas
"""

import sys
import os
import subprocess

print("=" * 70)
print("GERADOR DE IMAGENS - BUS BOX (PEÇAS SEPARADAS)")
print("=" * 70)


def generate_part_images():
    """Gera imagens PNG para cada peça separadamente usando OpenSCAD"""

    # Verificar se OpenSCAD está instalado
    try:
        result = subprocess.run(
            ["openscad", "--version"], capture_output=True, text=True
        )
        print(f"OpenSCAD encontrado: {result.stderr.strip()}")
    except FileNotFoundError:
        print("ERRO: OpenSCAD não encontrado!")
        print("Instale com: sudo apt-get install openscad")
        return False

    # Verificar arquivos STEP
    step_files = ["bus-box-Base.step", "bus-box-tampa.step"]

    print("\nVerificando arquivos STEP...")
    for step_file in step_files:
        if not os.path.exists(step_file):
            print(f"  ✗ {step_file} não encontrado")
            print("  Execute primeiro: python3 generate-images.py")
            return False
        print(f"  ✓ {step_file}")

    # Gerar imagens para cada peça
    for step_file in step_files:
        part_name = step_file.replace("bus-box-", "").replace(".step", "")
        print(f"\nProcessando: {part_name}")

        # Criar script OpenSCAD para cada vista
        views = {
            "isometric": 'import("{file}");',
            "front": 'import("{file}");',
            "top": 'import("{file}");',
            "right": 'import("{file}");',
        }

        for view_name, scad_code in views.items():
            scad_file = f"temp-{part_name}-{view_name}.scad"
            png_file = f"bus-box-{part_name}-{view_name}.png"

            # Criar arquivo SCAD
            with open(scad_file, "w") as f:
                f.write(scad_code.format(file=step_file))

            # Renderizar com OpenSCAD
            print(f"  Gerando {view_name}...")
            try:
                cmd = [
                    "openscad",
                    "-o",
                    png_file,
                    "--imgsize=800,600",
                    "--camera=0,0,0,55,0,25,140"
                    if view_name == "isometric"
                    else "--camera=0,0,0,0,0,0,140"
                    if view_name == "front"
                    else "--camera=0,0,0,0,0,90,140"
                    if view_name == "top"
                    else "--camera=0,0,0,0,90,0,140",
                    scad_file,
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

                if os.path.exists(png_file):
                    print(f"    ✓ {png_file}")
                else:
                    print(f"    ✗ Falha ao gerar {png_file}")
                    if result.stderr:
                        print(f"      Erro: {result.stderr[:200]}")

            except subprocess.TimeoutExpired:
                print(f"    ✗ Timeout ao renderizar {view_name}")
            except Exception as e:
                print(f"    ✗ Erro: {e}")
            finally:
                # Limpar arquivo temporário
                if os.path.exists(scad_file):
                    os.remove(scad_file)

    print("\n" + "=" * 70)
    print("PROCESSO CONCLUÍDO!")
    print("=" * 70)
    print("\nNota: A qualidade das imagens depende do OpenSCAD.")
    print("Para melhores resultados, abra os arquivos STEP no FreeCAD GUI.")

    return True


if __name__ == "__main__":
    success = generate_part_images()
    sys.exit(0 if success else 1)
