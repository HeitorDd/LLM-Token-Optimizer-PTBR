import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import tiktoken

#Configuração
def configurar_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)

configurar_nltk()

PRECO_POR_1M_TOKENS = 2.50 

def contar_tokens(texto):
    try:
        encoding = tiktoken.encoding_for_model("gpt-4o")
        return len(encoding.encode(texto))
    except:
        return int(len(texto.split()) * 1.3)

def otimizar_e_calcular(prompt_original):
    #Carrega as Stop Words
    palavras_inuteis = set(stopwords.words('portuguese'))
    

    #Lista de palavras que proibidas do sistema apagar
    lista_protecao = {'não', 'nem', 'nunca', 'jamais', 'nada', 'ninguém', 'sem', 'exceto'}
    
    palavras_inuteis = palavras_inuteis - lista_protecao

    tokens = word_tokenize(prompt_original, language='portuguese')
    
    prompt_limpo = [
        p for p in tokens 
        if p.lower() not in palavras_inuteis and p.isalnum()
    ]
    texto_final = " ".join(prompt_limpo)

    #Cálculos
    tok_orig = contar_tokens(prompt_original)
    tok_otim = contar_tokens(texto_final)
    reducao = tok_orig - tok_otim
    pct = (reducao / tok_orig) * 100 if tok_orig > 0 else 0
    dinheiro = (reducao * 1000 / 1_000_000) * PRECO_POR_1M_TOKENS

    return texto_final, tok_orig, tok_otim, pct, dinheiro

#Loop de Teste
print("=== Otimizador Seguro (Preserva negativas) ===")

while True:
    entrada = input("\nDigite seu prompt: ")
    if entrada.lower() in ['sair', 'exit']: break
    if not entrada.strip(): continue

    otimizado, t_orig, t_novo, pct, _ = otimizar_e_calcular(entrada)
    print("")
    print(f"Original : {entrada}")
    print("")
    print(f"Otimizado: {otimizado}") 
    print("")
    print(f"📉 Redução: {pct:.1f}%")