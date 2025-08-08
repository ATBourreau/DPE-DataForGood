#!/usr/bin/env python3
import sys

"""script qui filtre l'insersion de 1000 lignes par table. à partir du fichier sql d'importation (pgdump.sql)
*powered by ChatGPT...*
"""

LIMIT = 1000  # nombre max de lignes à garder par table

def truncate_dump(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:

        in_copy = False
        lines_copied = 0

        for line in infile:
            if not in_copy:
                outfile.write(line)
                if line.startswith('COPY ') and ' FROM STDIN;' in line:
                    print(line)
                    in_copy = True
                    lines_copied = 0

            else:
                # On est dans un bloc COPY
                if line.strip() == '\\.':
                    # fin du bloc COPY
                    outfile.write(line)
                    in_copy = False
                else:
                    # ligne de données, on limite à LIMIT lignes
                    if lines_copied < LIMIT:
                        outfile.write(line)
                    lines_copied += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 truncate_pg_dump.py dump_full.sql dump_truncated.sql")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    truncate_dump(input_file, output_file)
    print(f"Dump tronqué généré dans : {output_file}")
