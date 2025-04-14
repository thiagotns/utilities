import os
import pdfplumber
import pandas as pd
import re
import sys

if len(sys.argv) != 3:
    print("Uso: python extrair_notas.py <pasta_com_pdfs> <arquivo_saida.csv>")
    sys.exit(1)

PASTA_RAIZ = sys.argv[1]
SAIDA_CSV = sys.argv[2]

regex_valor = re.compile(r"VALOR TOTAL DA NOTA = R\$ ?([\d\.,]+)")
regex_mes_ano = re.compile(r"Mês de (\d{2}/\d{4})")
regex_servico = re.compile(r"(?i)(SESSÕES DE .+?)\s*\n")
regex_prestador = re.compile(r"Nome / Razão Social:\s*([^\n]+)")
regex_quantidade = re.compile(r"Item\s+Quantidade\s+Valor Unitário.+?\n(\d+)")

def extrair_dados(texto):
    valor = regex_valor.search(texto)
    mes_ano = regex_mes_ano.search(texto)
    servico = regex_servico.search(texto)
    prestador = regex_prestador.search(texto)
    quantidade = regex_quantidade.search(texto)

    mes, ano = (mes_ano.group(1).split("/") if mes_ano else (None, None))

    return {
        "valor_total": valor.group(1) if valor else None,
        "mes_referencia": mes,
        "ano_referencia": ano,
        "tipo_servico": servico.group(1).strip().title() if servico else None,
        "prestador": prestador.group(1).strip().title() if prestador else None,
        "quantidade_sessoes": int(quantidade.group(1)) if quantidade else None
    }

dados = []

for raiz, _, arquivos in os.walk(PASTA_RAIZ):
    for nome_arquivo in arquivos:
        if nome_arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(raiz, nome_arquivo)
            with pdfplumber.open(caminho_pdf) as pdf:
                texto = "\n".join(p.extract_text() or "" for p in pdf.pages)
                info = extrair_dados(texto)
                info["arquivo"] = nome_arquivo
                dados.append(info)

df = pd.DataFrame(dados)
df.to_csv(SAIDA_CSV, index=False, encoding="utf-8-sig")
print(f"✅ CSV exportado com sucesso para: {SAIDA_CSV}")
