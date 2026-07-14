import os
import csv
import sys
from pathlib import Path

def analizza_csv_folder(folder_path: str, separatore: str = ";"):
    folder = Path(folder_path)

    if not folder.exists():
        print(f"❌ Cartella non trovata: {folder_path}")
        sys.exit(1)

    csv_files = sorted(folder.glob("*.csv"))

    if not csv_files:
        print(f"⚠️  Nessun file CSV trovato in: {folder_path}")
        sys.exit(0)

    print(f"\n📂 Cartella: {folder.resolve()}")
    print(f"{'File':<70} {'Righe':>8}  {'Colonne':>8}  {'Encoding':<12}")
    print("-" * 110)

    totale_righe = 0
    totale_file = 0
    errori = []

    for csv_file in csv_files:
        # Prova prima utf-8-sig, poi latin-1
        for encoding in ("utf-8-sig", "latin-1"):
            try:
                with open(csv_file, encoding=encoding, newline="") as f:
                    reader = csv.reader(f, delimiter=separatore)
                    righe = list(reader)

                num_righe_dati = len(righe) - 1  # escludi intestazione
                num_colonne = len(righe[0]) if righe else 0

                print(f"{csv_file.name:<70} {num_righe_dati:>8}  {num_colonne:>8}  {encoding:<12}")
                totale_righe += num_righe_dati
                totale_file += 1
                break

            except Exception as e:
                if encoding == "latin-1":
                    errori.append((csv_file.name, str(e)))
                    print(f"{csv_file.name:<70} {'ERRORE':>8}")

    print("-" * 110)
    print(f"\n✅ File CSV trovati:       {totale_file}")
    print(f"✅ Righe dati totali:      {totale_righe:,}  (escluse intestazioni)")
    print(f"✅ Intestazioni escluse:   {totale_file}")

    if errori:
        print(f"\n⚠️  File con errori ({len(errori)}):")
        for nome, err in errori:
            print(f"   - {nome}: {err}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python count.py <percorso_cartella> [separatore]")
        print("Esempio: python count.py C:\n8n\files\gini2")
        sys.exit(1)

    folder = sys.argv[1]
    sep = sys.argv[2] if len(sys.argv) > 2 else ";"

    analizza_csv_folder(folder, sep)