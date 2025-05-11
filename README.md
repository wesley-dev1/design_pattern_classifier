# Detector de Padrões de Projeto via Gemini 2 Flash

Identifica automaticamente se um trecho de código implementa **Adapter**, **Singleton**, **Composite**, **Observer** ou **Iterator** usando o modelo **Gemini 2 Flash** da Google AI.

---

## Índice

1. [Pré‑requisitos](#pré-requisitos)
2. [Instalação](#instalação)
3. [Configuração da API‑key](#configuração-da-api-key)
4. [Execução](#execução)
5. [Como Funciona](#como-funciona)
6. [Solução de Problemas](#solucao-de-problemas)
7. [Licença](#licença)

---

## Pré‑requisitos

| Item                      | Versão mínima | Observação                                                 |
| ------------------------- | ------------- | ---------------------------------------------------------- |
| Python                    | 3.10          | Precisa ter Tkinter instalado (vem por padrão no Windows). |
| Conta Google AI Studio    | —             | Para gerar a variável **GOOGLE\_GENAI\_API\_KEY**.         |
| Biblioteca `google‑genai` | 1.14          | SDK oficial que expõe o método `models.generate_content`.  |

---

## Instalação

### 1. Clonar o repositório

```bash
# escolha sua pasta de trabalho
git clone https://github.com/<seu-usuario>/gemini-pattern-detector.git
cd gemini-pattern-detector
```

### 2. (Opcional) criar ambiente virtual

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install --upgrade pip
pip install google-genai
```

---

## Configuração da API‑key

1. Gere a chave em [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).
2. Defina a variável de ambiente.

| Sistema                             | Comando                                    |
| ----------------------------------- | ------------------------------------------ |
| Windows (PowerShell) – permanente   | `setx GOOGLE_GENAI_API_KEY "SUA_CHAVE" /M` |
| Windows (PowerShell) – sessão atual | `set GOOGLE_GENAI_API_KEY=SUA_CHAVE`       |
| Linux / macOS                       | `export GOOGLE_GENAI_API_KEY="SUA_CHAVE"`  |

Você também pode abrir o programa e escolher **2) Definir/alterar API‑KEY** para colar a chave.

---

## Execução

```bash
python menu_design_pattern_classifier_gui.py
```

Menu mostrado:

```
=== DETECTOR DE PADRÕES VIA GEMINI ===
1) Escolher arquivo (abre janela)
2) Definir/alterar API-KEY (OK)
0) Sair
```

1. Selecione **1** e escolha um arquivo `.py`, `.java`, `.txt` etc.
2. O Gemini analisa o código e um pop‑up exibe o padrão detectado.

Exemplo:

```
Padrão detectado: Singleton
```

---

## Como Funciona

1. `tkinter.filedialog.askopenfilename` abre o diálogo nativo.
2. O arquivo é lido (UTF‑8 ou Latin‑1).
3. O código é inserido em um prompt que limita a resposta a uma palavra.
4. `client.models.generate_content` envia o prompt ao modelo `gemini-2.0-flash`.
5. A primeira palavra da resposta é verificada → `Adapter`, `Singleton`, `Composite`, `Observer`, `Iterator` ou `Unknown`.
6. O resultado aparece em um `messagebox`.

---

## Solução de Problemas

| Erro                                            | Causa / Solução                                                                         |
| ----------------------------------------------- | --------------------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'google'` | O pacote não foi instalado no Python correto. Use `python -m pip install google-genai`. |
| Janela não abre no WSL                          | O WSL padrão não tem interface gráfica. Execute no Windows ou em outra máquina com GUI. |
| `UnicodeDecodeError`                            | Regrave o arquivo como UTF‑8 ou Latin‑1.                                                |
| Várias classes no mesmo arquivo                 | O modelo devolve o primeiro padrão que encontrar. Separe os testes.                     |

---

## Licença

Distribuído sob a licença MIT. Consulte `LICENSE` para detalhes.
