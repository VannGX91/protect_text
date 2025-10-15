import re

def protect_tags(text):
    """
    Melindungi semua tag <> , {}, [], dan <lf> agar tidak rusak saat diterjemahkan
    """
    tag_pattern = re.compile(r'(<[^>]+>|\{[^}]+\}|\[[^\]]+\]|<lf>|\\n\\n|\\n|[A-Za-z0-9?]+(?:_[A-Za-z0-9?]+)+)')
    
    placeholders = {}
    counter = 0

    def replacer(match):
        nonlocal counter
        tag = match.group(0)
        placeholder = f"__TAG{counter}__"
        placeholders[placeholder] = tag
        counter += 1
        return placeholder

    protected_text = tag_pattern.sub(replacer, text)
    return protected_text, placeholders


def restore_tags(text, placeholders):
    """
    Mengembalikan placeholder menjadi tag aslinya
    """
    for placeholder, tag in placeholders.items():
        text = text.replace(placeholder, tag)
    return text


def protect_file(input_file, output_file, placeholder_file):
    """
    Membaca input.txt → menghasilkan protected.txt + mapping placeholder
    """
    with open(input_file, "r", encoding="utf-8") as f:
        original_lines = f.readlines()

    protected_lines = []
    all_placeholders = []

    for line in original_lines:
        protected, placeholders = protect_tags(line.strip("\n"))
        protected_lines.append(protected)
        all_placeholders.append(placeholders)

    # Simpan hasil proteksi
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(protected_lines))

    # Simpan mapping placeholder (biar bisa dipakai lagi saat restore)
    import json
    with open(placeholder_file, "w", encoding="utf-8") as f:
        json.dump(all_placeholders, f, ensure_ascii=False, indent=2)

    print(f"[OK] Protected text disimpan ke {output_file}")
    print(f"[OK] Mapping placeholder disimpan ke {placeholder_file}")


def restore_file(translated_file, placeholder_file, output_file):
    """
    Membaca translated.txt + mapping placeholder → menghasilkan output.txt dengan tag kembali
    """
    with open(translated_file, "r", encoding="utf-8") as f:
        translated_lines = f.readlines()

    import json
    with open(placeholder_file, "r", encoding="utf-8") as f:
        all_placeholders = json.load(f)

    restored_lines = []
    for line, placeholders in zip(translated_lines, all_placeholders):
        restored = restore_tags(line.strip("\n"), placeholders)
        restored_lines.append(restored)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(restored_lines))

    print(f"[OK] Restored text disimpan ke {output_file}")


if __name__ == "__main__":
    # --- Mode proteksi ---
    protect_file("all_texts.txt", "protected.txt", "placeholders.json")

    # Setelah kamu translate manual `protected.txt` → jadi `translated.txt`
    # Jalankan bagian ini untuk mengembalikan tag:
    restore_file("translated.txt", "placeholders.json", "output.txt")
