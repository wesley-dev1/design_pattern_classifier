#!/usr/bin/env python3
"""
menu_design_pattern_classifier_gui_plus.py
Detecta o Design Pattern e apresenta uma breve justificativa.

Requisitos:
  pip install google-genai
  export GOOGLE_GENAI_API_KEY="SUA_CHAVE"
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Final, Tuple
import tkinter as tk
from tkinter import filedialog, messagebox
from google import genai
import textwrap

MODEL: Final[str] = "gemini-2.0-flash"
PATTERNS: Final[set[str]] = {
    "Adapter", "Singleton", "Composite", "Observer", "Iterator"
}

# ────────────────────────── prompt ──────────────────────────
def _prompt(code: str) -> str:
    patterns_list = " | ".join(sorted(PATTERNS))
    return (
        "You are a highly experienced software architect.\n"
        "Analyze the CODE below and answer using the following format, in exactly **three parts**, all in Brazilian Portuguese (pt-BR):\n\n"
        f"1. PADRÃO DETECTADO: <one of {patterns_list} or Unknown>\n"
        "2. JUSTIFICATIVA: <detailed explanation in 2-3 sentences>\n"
        "3. TRECHO ANALISADO:\n<include a relevant, clean and indented code excerpt from the input>\n\n"
        "DO NOT TRANSLATE CODE.\n"
        "Be clear, professional, and structured.\n\n"
        f"CODE:\n```language\n{code}\n```"
    )

# ────────────────────────── análise ──────────────────────────
def _analyse(code: str, api_key: str) -> Tuple[str, str]:
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(model=MODEL, contents=_prompt(code))

    text = resp.text.strip()

    pattern, justification, snippet = "Unknown", "—", "—"

    for line in text.splitlines():
        if line.startswith("1. PADRÃO DETECTADO:"):
            pattern = line.split(":", 1)[1].strip()
        elif line.startswith("2. JUSTIFICATIVA:"):
            justification = line.split(":", 1)[1].strip()
        elif line.startswith("3. TRECHO ANALISADO:"):
            snippet_start = text.index("3. TRECHO ANALISADO:") + len("3. TRECHO ANALISADO:")
            snippet = text[snippet_start:].strip()
            break

    # Garante indentação visual adequada no tkinter
    snippet = textwrap.indent(snippet.strip(), "  ")

    mensagem = (
        f"🧠 Padrão Detectado: {pattern}\n\n"
        f"📌 Justificativa:\n{justification.strip()}\n\n"
        f"📄 Trecho analisado:\n{'-'*34}\n{snippet}\n{'-'*34}"
    )

    return pattern, mensagem

# ────────────────────────── seleção de arquivo ──────────────────────────
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

# ───────────────────────────── menu ─────────────────────────────
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

                pattern, mensagem = _analyse(code, api_key)
                messagebox.showinfo("Resultado", mensagem)

            case "2":
                api_key = input("Cole a GOOGLE_GENAI_API_KEY: ").strip()
                os.environ["GOOGLE_GENAI_API_KEY"] = api_key

            case "0" | "q" | "Q":
                break

            case _:
                print("Opção inválida!")
                input("Enter p/ tentar de novo…")

# ───────────────────────────── execução ─────────────────────────────
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
