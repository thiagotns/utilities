# nf-extractor

Este script Python percorre uma pasta com PDFs de notas fiscais e extrai:

- Valor total da nota
- Mês e ano de referência
- Tipo de serviço prestado
- Nome do prestador
- Quantidade de sessões

Os dados são exportados para um arquivo CSV.

## Requisitos

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## Requisitos

```bash
pip install pdfplumber pandas
```

## Uso

```bash
python script.py <caminho/para/pasta_com_pdfs> <saida.csv>
```

### Exemplo:

```bash
python script.py ./notas ./saida.csv
```

O script processa todos os PDFs da pasta e subpastas.
