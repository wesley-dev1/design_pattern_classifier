#!/usr/bin/env python3
"""
menu_design_pattern_classifier_gui_min.py
Versão simplificada: remove a opção de colar código manualmente.
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Final
import tkinter as tk
from tkinter import filedialog, messagebox
from google import genai                    # pip install google-genai

MODEL: Final[str] = "gemini-2.0-flash"
PATTERNS: Final[set[str]] = {
    "Adapter", "Singleton", "Composite", "Observer", "Iterator"
}

# ───────────────── utilidades ─────────────────
def _prompt(code: str) -> str:
    return (
        "You are an expert software architect.\n"
        "Analyse the CODE below and answer with ONLY one word "
        "chosen from this list (case-sensitive):\n"
        "Adapter | Singleton | Composite | Observer | Iterator\n"
        "If none applies, answer 'Unknown'. No explanations.\n\n"
        f"CODE:\n```language\n{code}\n```"
    )

def _classify(code: str, api_key: str) -> str:
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(model=MODEL, contents=_prompt(code))
    word = resp.text.strip().split()[0]
    return word if word in PATTERNS else "Unknown"

def _select_file() -> str | None:
    root = tk.Tk(); root.withdraw()
    path = filedialog.askopenfilename(
        title="Selecione o arquivo de código",
        filetypes=[
            ("Arquivos Python", "*.py"),
            ("Arquivos Java", "*.java *.class"),
            ("Arquivos de texto", "*.txt *.md *.json"),
            ("Todos os arquivos", "*.*"),
        ],
    )
    root.destroy()
    return path or None

# ───────────────── menu ─────────────────
def main() -> None:
    api_key = os.getenv("GOOGLE_GENAI_API_KEY") or ""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== DETECTOR DE PADRÕES VIA GEMINI ===")
        print("1) Escolher arquivo (abre janela)")
        print("2) Definir/alterar API-KEY "
              f"({'OK' if api_key else '⚠️ não definida'})")
        print("0) Sair")
        op = input("Opção: ").strip()

        match op:
            case "1":
                path = _select_file()
                if not path:
                    continue
                try:
                    code = Path(path).read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    code = Path(path).read_text("latin-1", errors="ignore")
                pattern = _classify(code, api_key)
                messagebox.showinfo("Resultado", f"Padrão detectado: {pattern}")

            case "2":
                api_key = input("Cole a GOOGLE_GENAI_API_KEY: ").strip()
                os.environ["GOOGLE_GENAI_API_KEY"] = api_key

            case "0" | "q" | "Q":
                break

            case _:
                print("Opção inválida!")
                input("Enter p/ tentar de novo…")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
