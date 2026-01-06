#!/usr/bin/env python3
import sys
from pathlib import Path

extensions = [
    '.c', '.cpp', '.cc', '.cxx', '.h', '.hh', '.hpp', '.hxx', '.ino',
    '.py', '.pyw', '.java', '.js', '.ts', '.tsx', '.jsx', '.rb',
    '.go', '.rs', '.swift', '.kt', '.kts', '.cs', '.php',
    '.html', '.htm', '.css', '.scss', '.sass', '.lua', '.sh',
    '.bat', '.ps1', '.sql', '.r', '.m', '.asm', '.s',
    '.json', '.xml', '.yml', '.yaml', '.toml', '.ini',
]

# Pastas que devem ser ignoradas para evitar erros de sistema e lentidão
ignored_dirs = {
    'node_modules', '.git', '.svn', '.hg', '.idea', '.vscode', 
    '__pycache__', 'venv', 'env', '.next', 'dist', 'build', 'coverage'
}

output_file = 'code2text_output.txt'

def read_file_with_fallback(file_path: Path):
    try:
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return file_path.read_text(encoding='latin1')
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
            return None

def main():
    current_dir = Path('.').resolve()
    script_file = Path(__file__).resolve()
    output_path = (current_dir / output_file).resolve()

    files = []
    
    # Iterar sobre todos os arquivos recursivamente
    for f in current_dir.rglob('*'):
        
        # 1. Verificação de Segurança: Pular pastas ignoradas ANTES de tocar no arquivo
        # Isso evita o WinError 1920 em links simbólicos do node_modules
        if any(part in ignored_dirs for part in f.parts):
            continue

        try:
            # 2. Verificação protegida: is_file() pode falhar em arquivos de sistema/bloqueados
            if not f.is_file():
                continue
            
            # Filtros de extensão e arquivo
            if f.suffix.lower() not in extensions:
                continue
            if f.resolve() == script_file:
                continue
            if f.resolve() == output_path:
                continue
            
            files.append(f)

        except OSError:
            # Captura erros de permissão ou arquivos "fantasmas" do OneDrive/Windows
            continue
        except Exception as e:
            print(f"Exception processing {f}: {e}")
            continue

    files.sort()

    if not files:
        print(f"No files with extensions {extensions} found in {current_dir}. Exiting.")
        sys.exit(0)

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write('Code:\n\n')
        for file in files:
            content = read_file_with_fallback(file)
            if content is None:
                continue
            
            try:
                rel_path = file.resolve().relative_to(current_dir)
            except Exception as e:
                print(f"Exception resolving path for {file}: {e}")
                rel_path = file.resolve()
            
            try:
                rel_dir = file.parent.resolve().relative_to(current_dir)
            except Exception as e:
                print(f"Exception resolving directory for {file}: {e}")
                rel_dir = file.parent.resolve()
            
            out.write(f"{rel_path}:\n")
            out.write(f"Directory: {rel_dir}\n\n")
            out.write(content)
            out.write('\n\n')

    print(f"Generated {output_file} with {len(files)} files.")

if __name__ == '__main__':
    main()