import streamlit as st
import requests
import time
import pymupdf as fitz

# Configuração da página
st.set_page_config(page_title="Análise de Projeto", layout="wide")

# Função auxiliar para obter input numérico
def get_input_float(label):
    valor = st.text_input(label, "0")
    try:
        return float(valor)
    except ValueError:
        return 0.0

# Inicialização das variáveis de sessão
def init_session_state():
    if 'AfastamentoFrontal1' not in st.session_state:
        st.session_state['AfastamentoFrontal1'] = 0.0
    if 'AfastamentoFundo1' not in st.session_state:
        st.session_state['AfastamentoFundo1'] = 0.0
    if 'AfastamentoDireito1' not in st.session_state:
        st.session_state['AfastamentoDireito1'] = 0.0
    if 'AfastamentoEsquerdo1' not in st.session_state:
        st.session_state['AfastamentoEsquerdo1'] = 0.0
    if 'TaxaOcupacao1' not in st.session_state:
        st.session_state['TaxaOcupacao1'] = 0.0
    if 'AlturaMaxima1' not in st.session_state:
        st.session_state['AlturaMaxima1'] = 0.0
    if 'CoeficienteAprovBasico1' not in st.session_state:
        st.session_state['CoeficienteAprovBasico1'] = 0.0
    if 'CoeficienteAprovMaximo1' not in st.session_state:
        st.session_state['CoeficienteAprovMaximo1'] = 0.0
    if 'TaxaPermeabilidade1' not in st.session_state:
        st.session_state['TaxaPermeabilidade1'] = 0.0
    if 'CotaSoleira1' not in st.session_state:
        st.session_state['CotaSoleira1'] = ""
    if 'modo_auto' not in st.session_state:
        st.session_state['modo_auto'] = False
    if 'pdf_linhas' not in st.session_state:
        st.session_state['pdf_linhas'] = []

init_session_state()

# Seção de Observações
with st.expander("📝 **Observações - Comece por aqui**"):
    st.write("Utilizar ponto ao em vez de vírgula. Ex.: 13.45")
    st.write("O buscador automático procura apenas pela LUOS, caso o imóvel não tenha LUOS, deverá ser utilizado a fórma **Preenchimento Manual** no próximo tópico")
    st.write("Versão 0.4. Corrigido: importação automática e adicionado a constula aos mapas e quadros")



# Seção 1: Parâmetros Urbanísticos
with st.expander("📝 **Passo 1: Parâmetros Urbanísticos do Terreno**"):
    # Dados das regiões e links (no formato: Região;Link1;Link2)
    # Dados das regiões e links (no formato: Região;Link1;Link2)
    dados_regioes = """
    Gama;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-1A_Gama.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-1A_Gama.pdf
    Taguatinga;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-2A_Taguatinga.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-2A_Taguatinga.pdf
    Brazlândia;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-3A_Brazlandia.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-3A_Brazlandia.pdf
    Sobradinho;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-4A_Sobradinho.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-4A_Sobradinho.pdf
    Planaltina;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-5A-Planaltina.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-5A_Planaltina.pdf
    Paranoa;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-6A_Paranoa.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-6A_Paranoa.pdf
    Bandeirante;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-7A_Nucleo-Bandeirante.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-7A_Nucleo-Bandeirante.pdf
    Ceilândia;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-8A_Ceilandia.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-8A_Ceilandia.pdf
    Guara;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-9A_Guara.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-9A_Guara.pdf
    Samambaia;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-10A_Samambaia.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-10A_Samambaia.pdf
    Santa Maria;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-11A_Santa-Maria.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-11A_Santa-Maria.pdf
    Sao Sebastiao;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-12A_Sao-Sebastiao.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-12A_Sao-Sebastiao.pdf
    Recanto das Emas;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-13A_Recanto-das-Emas.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-13A_Recanto-das-Emas.pdf
    Lago Sul;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-14A_Lago-Sul.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-14A_Lago-Sul.pdf
    Riacho Fundo;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-15A_Riacho-Fundo.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-15A_Riacho-Fundo.pdf
    Lago Norte;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-16A_Lago-Norte.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-16A_Lago-Norte.pdf
    Aguas Claras;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-17A_Aguas-Claras.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-17A_Aguas-Claras.pdf
    Riacho Fundo II;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-18A_Riacho-Fundo-II.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-18A_Riacho-Fundo-II.pdf
    Varjao;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-19A_Varjao.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-19A_Varjao.pdf
    Park Way;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-20A_Park-Way.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-20A_Park-Way.pdf
    SCIA;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-21A_SCIA.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-21A_SCIA.pdf
    Sobradinho II;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-22A_Sobradinho-II.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-22A_Sobradinho.pdf
    Jardim Botanico;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-23A_Jardim-Botanico.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-23A_Jardim-Botanico.pdf
    Itapoa;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-24A_Itapoa.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-24A_Itapoa.pdf
    SIA;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-25A_SIA.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-25A_SIA.pdf
    Vicente Pires;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-26A_Vicente-Pires.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-26A_Vicente-Pires.pdf
    Fercal;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-27A_Fercal.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-27A_Fercal.pdf
    Sol Nascente;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-28A_Por-do-Sol_Sol-Nascente.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-28A_Sol-Nascente_Por-do-Sol.pdf
    Arniqueira;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-II-%25E2%2580%2593-Mapa-29A_Arniqueira.pdf;https://www.seduh.df.gov.br/documents/6726485/38572899/LC1007_2022_Anexo-III-%25E2%2580%2593-Quadro-29A_Arniqueira.pdf
    """

    # Processar os dados
    regioes = {}
    for linha in dados_regioes.strip().split('\n'):
        partes = linha.split(';')
        if len(partes) == 3:
            regiao = partes[0]
            link1 = partes[1]
            link2 = partes[2]
            regioes[regiao] = {'Mapa': link1, 'Quadro': link2}

    # Interface do Streamlit
    st.markdown('🗺️ **Consulta dos parâmetros urbanísticos - Mapas e Quadros do DF**')
    st.markdown('Selecione uma região administrativa do Distrito Federal para acessar os documentos relacionados.')

    # Seleção da região
    regiao_selecionada = st.selectbox(
        'Selecione a região:',
        sorted(regioes.keys()),
        index=0,
        help='Escolha uma região administrativa do DF'
    )

    # Exibir os links
    if regiao_selecionada:
        st.markdown(f'Documentos para {regiao_selecionada}')
        
        st.markdown(f'**Mapa:** [Abrir Mapa PDF]({regioes[regiao_selecionada]["Mapa"]})', unsafe_allow_html=True)
        st.markdown(f'**Quadro:** [Abrir Quadro PDF]({regioes[regiao_selecionada]["Quadro"]})', unsafe_allow_html=True)

    st.markdown('---')

    st.subheader("Aqui será a inserção dos parâmetros urbanísticos")
    modo = st.radio("Escolha o modo de entrada dos parâmetros urbanísticos:", ["Extração Automática", "Preenchimento Manual"])

    if modo == "Extração Automática":
        codigo = st.text_input("Informe o CIPU - Vão ser apenas números (Não confundir com o CIU)", "418924")

        if st.button("Consultar"):
            st.info("Enviando requisição...  - **Pode demorar até 10 segundos**")

            url_submit = "https://www.geoservicos.ide.df.gov.br/arcgis/rest/services/Geoprocessing/certidaoparametrosurb/GPServer/certidao_parametros_urb/submitJob"
            payload = {"codigo": codigo, "f": "json"}

            try:
                response = requests.post(url_submit, data=payload)
                response.raise_for_status()
                res_json = response.json()
            except Exception as e:
                st.error(f"Erro ao enviar requisição: {e}")
                st.stop()

            job_id = res_json.get("jobId")
            if not job_id:
                st.error("Job ID não retornado.")
                st.stop()

            status_url = f"https://www.geoservicos.ide.df.gov.br/arcgis/rest/services/Geoprocessing/certidaoparametrosurb/GPServer/certidao_parametros_urb/jobs/{job_id}?f=json"
            while True:
                status_resp = requests.get(status_url).json()
                job_status = status_resp.get("jobStatus", "")
                if job_status == "esriJobSucceeded":
                    break
                elif job_status in ["esriJobFailed", "esriJobCancelled"]:
                    st.error("Job falhou ou foi cancelado.")
                    st.stop()
                time.sleep(2)

            job_info = requests.get(status_url).json()
            pdf_url = None

            if "results" in job_info:
                for key, val in job_info["results"].items():
                    if key == "arquivo":
                        result_url = f"https://www.geoservicos.ide.df.gov.br/arcgis/rest/services/Geoprocessing/certidaoparametrosurb/GPServer/certidao_parametros_urb/jobs/{job_id}/{val['paramUrl']}?f=json"
                        result = requests.get(result_url).json()
                        pdf_url = result.get("value")

            if not pdf_url:
                st.warning("Link para o PDF não encontrado.")
                st.stop()

            st.subheader("📄 Certidão Gerada")
            st.markdown(f"[Clique aqui para abrir o PDF]({pdf_url})", unsafe_allow_html=True)

            # Extração de texto do PDF
            try:
                pdf_response = requests.get(pdf_url)
                pdf_response.raise_for_status()
                pdf_bytes = pdf_response.content

                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                texto = ""
                for page in doc:
                    texto += page.get_text()
                doc.close()

                # Extração dos parâmetros
                linhas = texto.split("\n")
                
                def parse_float(valor_2):
                    try:
                        return float(valor_2.strip().replace(",", "."))
                    except:
                        return 0

                # Armazena todos os valores na sessão
                st.session_state['AfastamentoFrontal1'] = parse_float(linhas[106])
                st.session_state['AfastamentoFundo1'] = parse_float(linhas[107])
                st.session_state['AfastamentoDireito1'] = parse_float(linhas[108])
                st.session_state['AfastamentoEsquerdo1'] = parse_float(linhas[101])
                st.session_state['TaxaOcupacao1'] = parse_float(linhas[104])
                st.session_state['AlturaMaxima1'] = parse_float(linhas[87])
                st.session_state['CoeficienteAprovBasico1'] = parse_float(linhas[103])
                st.session_state['CoeficienteAprovMaximo1'] = parse_float(linhas[109])
                st.session_state['TaxaPermeabilidade1'] = parse_float(linhas[86])
                st.session_state['CotaSoleira1'] = linhas[83]
                st.session_state['pdf_linhas'] = linhas
                st.session_state['modo_auto'] = True

                st.success("Dados extraídos com sucesso!")

            except Exception as e:
                st.error(f"Erro ao extrair texto do PDF: {e}")
                st.stop()

            # Mostra os valores extraídos
            st.subheader("📌 Parâmetros Urbanísticos Extraídos Automaticamente (Apenas para Consulta)")
            st.markdown(f"**Afastamento Frontal:** {st.session_state['AfastamentoFrontal1']:.2f}")
            st.markdown(f"**Afastamento Fundo:** {st.session_state['AfastamentoFundo1']:.2f}")
            st.markdown(f"**Afastamento Direito:** {st.session_state['AfastamentoDireito1']:.2f}")
            st.markdown(f"**Afastamento Esquerdo:** {st.session_state['AfastamentoEsquerdo1']:.2f}")
            st.markdown(f"**Taxa de Ocupação:** {st.session_state['TaxaOcupacao1']:.2f}")
            st.markdown(f"**Altura Máxima:** {st.session_state['AlturaMaxima1']:.2f}")
            st.markdown(f"**Coeficiente Aproveitamento Básico:** {st.session_state['CoeficienteAprovBasico1']:.2f}")
            st.markdown(f"**Coeficiente Aproveitamento Máximo:** {st.session_state['CoeficienteAprovMaximo1']:.2f}")
            st.markdown(f"**Taxa de Permeabilidade:** {st.session_state['TaxaPermeabilidade1']:.2f}")
            st.markdown(f"**Cota de Soleira:** {st.session_state['CotaSoleira1']}")

    else:  # Modo Manual
        st.session_state['modo_auto'] = False
        st.session_state['AfastamentoFrontal1'] = get_input_float("Afastamento Frontal")
        st.session_state['AfastamentoFundo1'] = get_input_float("Afastamento Fundo")
        st.session_state['AfastamentoDireito1'] = get_input_float("Afastamento Direito")
        st.session_state['AfastamentoEsquerdo1'] = get_input_float("Afastamento Esquerdo")
        st.session_state['TaxaOcupacao1'] = get_input_float("Taxa de Ocupação - Ex.:50")
        st.session_state['AlturaMaxima1'] = get_input_float("Altura Máxima")
        st.session_state['CoeficienteAprovBasico1'] = get_input_float("Coeficiente Aproveitamento Básico - Ex.:2")
        st.session_state['CoeficienteAprovMaximo1'] = get_input_float("Coeficiente Aproveitamento Máximo - Ex.:3")
        st.session_state['TaxaPermeabilidade1'] = get_input_float("Taxa de Permeabilidade  - Ex.:80")
        st.session_state['CotaSoleira1'] = st.radio(
            "Posição da Cota de Soleira no parâmetro Urbanístico:",
            [
                "Ponto Médio da Edificação",
                "Cota Altimétrica média do Lote",
                "Ponto Médio da Testada Frontal"
            ]
        )

# Seção 2: Dados do Projeto
with st.expander("**📝 Passo 2: Dados do Projeto**"):
    # Recupera todos os valores da sessão
    AfastamentoFrontal1 = st.session_state['AfastamentoFrontal1']
    AfastamentoFundo1 = st.session_state['AfastamentoFundo1']
    AfastamentoDireito1 = st.session_state['AfastamentoDireito1']
    AfastamentoEsquerdo1 = st.session_state['AfastamentoEsquerdo1']
    TaxaOcupacao1 = st.session_state['TaxaOcupacao1']
    AlturaMaxima1 = st.session_state['AlturaMaxima1']
    CoeficienteAprovBasico1 = st.session_state['CoeficienteAprovBasico1']
    CoeficienteAprovMaximo1 = st.session_state['CoeficienteAprovMaximo1']
    TaxaPermeabilidade1 = st.session_state['TaxaPermeabilidade1']
    CotaSoleira1 = st.session_state['CotaSoleira1']

    # Mostra os valores extraídos
    st.markdown("📌 Parâmetros Urbanísticos Utilizados (Apenas para Consulta) 📌")
    st.markdown(f"**Afastamento Frontal:** {AfastamentoFrontal1:.2f}")
    st.markdown(f"**Afastamento Fundo:** {AfastamentoFundo1:.2f}")
    st.markdown(f"**Afastamento Direito:** {AfastamentoDireito1:.2f}")
    st.markdown(f"**Afastamento Esquerdo:** {AfastamentoEsquerdo1:.2f}")
    st.markdown(f"**Taxa de Ocupação:** {TaxaOcupacao1:.2f}")
    st.markdown(f"**Altura Máxima:** {AlturaMaxima1:.2f}")
    st.markdown(f"**Coeficiente Aproveitamento Básico:** {CoeficienteAprovBasico1:.2f}")
    st.markdown(f"**Coeficiente Aproveitamento Máximo:** {CoeficienteAprovMaximo1:.2f}")
    st.markdown(f"**Taxa de Permeabilidade:** {TaxaPermeabilidade1:.2f}")
    st.markdown(f"**Cota de Soleira:** {CotaSoleira1}")
    st.write("-----------------")
    
    # Se foi modo automático, temos as linhas do PDF disponíveis
    if st.session_state['modo_auto']:
        linhas = st.session_state['pdf_linhas']
    

    
    # Campos para entrada manual
    AreaDoLote = get_input_float("Área do Lote (terreno)- Projeto Arquitetônico")
    st.write("-----------------")


    st.write(f"Afastamento Frontal mínimo permitido: {AfastamentoFrontal1}")

  
    AfastamentoFrontal3 = get_input_float("Afastamento Frontal - Projeto Arquitetônico")
    if AfastamentoFrontal3 < AfastamentoFrontal1:
        st.error(f"🔴 **O afastamento frontal é inferior ao mínimo permitido** 🔴")
    st.write("-----------------")

    st.markdown(f"Afastamento Fundo mínimo permitido: {AfastamentoFundo1}")
    AfastamentoFundo3 = get_input_float("Afastamento Fundo - Projeto Arquitetônico")
    if AfastamentoFundo3 < AfastamentoFundo1:
        st.error(f"🔴 **O afastamento de fundo é inferior ao mínimo permitido** 🔴")
    st.write("-----------------")

    st.markdown(f"Afastamento Direito mínimo permitido: {AfastamentoDireito1}")
    AfastamentoDireito3 = get_input_float("Afastamento Direito - Projeto Arquitetônico")
    if AfastamentoDireito3 < AfastamentoDireito1:
        st.error(f"🔴 **O afastamento da lateral direita é inferior ao mínimo permitido** 🔴")
    st.write("-----------------")

    st.markdown(f"Afastamento Esquerdo mínimo permitido: {AfastamentoEsquerdo1}")
    AfastamentoEsquerdo3 = get_input_float("Afastamento Esquerdo - Projeto Arquitetônico")
    if AfastamentoEsquerdo3 < AfastamentoEsquerdo1:
        st.error(f"🔴 **O afastamento da lateral esquerda é inferior ao mínimo permitido** 🔴")
    st.write("-----------------")

    st.markdown(f"Altura Máxima: {AlturaMaxima1}")
    Altura3 = get_input_float("Altura (m) - Projeto Arquitetônico")
    if Altura3 > AlturaMaxima1:
        st.error(f"🔴 **Altura Máxima excedida** 🔴")    
    st.write("-----------------")

    st.markdown(f"Área mínima permeável: {AreaDoLote * (TaxaPermeabilidade1/100)}")
    AreaPermeavel3 = get_input_float("Área Permável - Projeto Arquitetônico")
    if AreaPermeavel3 < (AreaDoLote * (TaxaPermeabilidade1/100)):
        st.error(f"🔴 **O projeto não possui a área de permeabilidade mínima** 🔴")   
    st.write("-----------------")

    st.markdown(f"Área total de construção permitida: {AreaDoLote * CoeficienteAprovBasico1}")
    AreaTotalConstrucao3 = get_input_float("Área total da Construção - Projeto Arquitetônico")
    if AreaTotalConstrucao3 > (AreaDoLote * CoeficienteAprovBasico1):
        st.error(f"🔴 **Extrapolado o coeficiente de aproveitamento básico do lote** 🔴")  
    st.write("-----------------")

    st.markdown(f"Área de construção do térreo (Para cálculo da taxa de ocupação): {AreaDoLote * (TaxaOcupacao1/100)}")
    AreaConstruaoTerreo3 = get_input_float("Área de construção do térreo (para cálculo do coeficiente de aproveitamento) - Projeto Arquitetônico")
    if AreaConstruaoTerreo3 > (AreaDoLote * (TaxaOcupacao1/100)):
        st.error(f"🔴 **Extrapolado o coeficiente de aproveitamento do lote** 🔴")  
    st.write("-----------------")

    st.markdown(f"Cota de soleira extraída através da Seduh - GeoPortal")
    CotaSoleiraNumerica3 = get_input_float("Cota de Soleira Ex.: 1.105,64: - Projeto Arquitetônico")    
    CotaCoroamento3 = CotaSoleiraNumerica3 + Altura3
    st.markdown(f"Cota de coroamento calculada: {CotaCoroamento3}")
    st.write("-----------------")

    PossuiCoroamento = st.radio(
    "No Corte da Arquitetura, possui a cota da soleira com sua respectiva metragem até o ponto mais alto da edificação?",
    [
        "Sim",
        "Não"
    ]
    )
    if PossuiCoroamento == "Não":
        st.error("**❌ Falta a cota da soleira e distância até o coroamento da edificação**")
    st.write("-----------------")


    CotaSoleira3 = st.radio(
    "Critério utilizado para determinação da Cota de Soleira:",
    [
        "Ponto Médio da Edificação",
        "Cota Altimétrica média do Lote",
        "Ponto Médio da Testada Frontal"
    ]
    )
    st.write("-----------------")

    st.markdown("Medidas do terreno")   
    TestadaFrontal3 = get_input_float("Testada Frontal do lote - Projeto Arquitetônico")
    TestadaFundo3 = get_input_float("Testada Fundo do lote - Projeto Arquitetônico")
    LateralDireito3 = get_input_float("Lateral da lateral Direita do lote - Projeto Arquitetônico")
    LateralEsquerdo3 = get_input_float("Lateral da lateral Esquerda do lote - Projeto Arquitetônico")



#terceiro tópico - dados da topografia
with st.expander("**📝 Passo 3: Dados da Topografia**"):
    AfastamentoFrontal4 = get_input_float("Afastamento Frontal - Topografia")
    AfastamentoFundo4 = get_input_float("Afastamento Fundo - Topografia")
    AfastamentoDireito4 = get_input_float("Afastamento Direito - Topografia")
    AfastamentoEsquerdo4 = get_input_float("Afastamento Esquerdo - Topografia")
    TestadaFrontal4 = get_input_float("Testada Frontal - Topografia")
    TestadaFundo4 = get_input_float("Testada Fundo - Topografia")
    LateralDireito4 = get_input_float("Lateral Direito - Topografia")
    LateralEsquerdo4 = get_input_float("Lateral Esquerdo - Topografia")
    CotaCoroamento4 = get_input_float("Cota de Coroamento - Topografia")
    CotaSoleiraNumerica4 = get_input_float("Cota de Soleira - Topografia:")
    CotaSoleiraTopografia = st.radio(
    "Critério utilizado para determinação da posição da Cota de Soleira na topografia:",
    [
        "Ponto Médio da Edificação",
        "Cota Altimétrica média do Lote",
        "Ponto Médio da Testada Frontal"
    ]
    )


#quarto tópico - Documentação do imóvel
with st.expander("**📝 Passo 4: Documentação do Imóvel**"):
    TestadaFrontal5 = get_input_float("Testada Frontal - Documentação")
    TestadaFundo5 = get_input_float("Testada Fundo - Documentação")
    LateralDireito5 = get_input_float("Lateral Direito - Documentação")
    LateralEsquerdo5 = get_input_float("Lateral Esquerdo - Documentação")
    AreaDoLote5 = get_input_float("Área do Lote - Documentação")
    CotaSoleiraSeudh = get_input_float("Cota de Soleira da SEDUH - Documentação")

    # Botão principal com padrão "Sim"
    opcao_principal = st.radio("Existe condomínio devidamente constituido? Ex.: Park Way, SMBD...", ["Não", "Sim"], index=0)

    # Define variáveis com valores padrão
    instituicao = plano = ngb = None

    if opcao_principal == "Sim":
        instituicao = st.radio("Consta Instituição de Condomínio no processo?:", ["Sim", "Não"])
        plano = st.radio("Consta o Plano de Ocupação no processo:", ["Sim", "Não"])
        ngb = st.radio("Consta a NGB no processo:", ["Sim", "Não"])

#quinto tópico - Análise Automática
with st.expander("**📝 Passo 5: Análise Automática**"):
    CoeficienteAproveitamentoReal = ((TaxaOcupacao1/100) * AreaDoLote)
    CoeficienteBasicoreal = (CoeficienteAprovBasico1 * AreaDoLote)
    AreaVerdeMinima = AreaPermeavel3 * AreaDoLote

    st.subheader("Projeto")

    if CotaSoleiraTopografia != CotaSoleira3:
        st.write("🔴 **A posição da Cota de Soleira informada na topografia é diferente da informada no Projeto Arquitetônico** 🔴")

    if CotaSoleira3 != CotaSoleira1:
        st.write("🔴 **A posição da Cota de Soleira informada na arquitetura é diferente do parâmetro urbanístico** 🔴")

    #coeficiente de aproveitamento básico
    st.write(f"**🏚️ Área Construída total:** {AreaTotalConstrucao3}")
    st.write(f"**Área de Construção máxima permitida para o lote:** {CoeficienteBasicoreal}")     
    if AreaTotalConstrucao3 > CoeficienteBasicoreal:
        st.write("🔴 A área total de construção ultrapassou o máximo permitido 🔴")
    else:
        st.write("✅ Área total de construção dentro do limite")
    st.write("-----------------")

    #área verde
    st.write(f"**🌳 Área verde no projeto:** {AreaPermeavel3}")
    st.write(f"**Área de permeabilidade mínima:** {AreaVerdeMinima}")     
    if AreaPermeavel3 >= AreaVerdeMinima:
        st.write("✅ Área permeável dentro dos limites")
    #else:
        st.write("🔴 Área verde insuficiente 🔴")
    st.write("-----------------")   

    #taxa de ocupação
    st.write(f"**🔳 Área da Taxa de Ocupação do projeto:** {AreaConstruaoTerreo3}")
    st.write(f"**Área da Taxa de Ocupação permitida para o lote:** {CoeficienteAproveitamentoReal}")     
    if AreaConstruaoTerreo3 > CoeficienteAproveitamentoReal:
        st.write("🔴 Taxa de ocupação ultrapassada 🔴")
    else:
        st.write("✅ Taxa de ocupação atendida")
    st.write("-----------------")

    # altura máxima
    if Altura3 <= AlturaMaxima1:
        st.write("✅ Altura nos limites permitidos")
    else: 
        st.write("🔴 Altura máxima maior do que a permitida 🔴")
        st.write(f"**Altura máxima permitida:** {AlturaMaxima1}")
        st.write(f"**Altura de acordo com o projeto arquitetônico:** {Altura3}")
        st.write("--------------------------------------")

    #afastamento frontal    
    if (AfastamentoFrontal3 >= AfastamentoFrontal1):
        st.write("✅ O afastamento frontal no projeto arquitetônico está dentro do limite permitido.")
    else: 
        st.write("🔴 O afastamento frontal no projeto arquitetônico NÃO está dentro do limite permitido. 🔴")

    #afastamento fundos   
    if (AfastamentoFundo3 >= AfastamentoFundo1):
        st.write("✅ O afastamento de fundos no projeto arquitetônico está dentro do limite permitido.")
    else: 
        st.write("🔴 O afastamento de fundos no projeto arquitetônico NÃO está dentro do limite permitido. 🔴")

    #afastamento direito  
    if (AfastamentoDireito3 >= AfastamentoDireito1):
        st.write("✅ O afastamento da lateral direita no projeto arquitetônico está dentro do limite permitido.")
    else: 
        st.write("🔴 O afastamento da lateral direita no projeto arquitetônico NÃO está dentro do limite permitido. 🔴")

    #afastamento esquerda
    if (AfastamentoEsquerdo3 >= AfastamentoEsquerdo1):
        st.write("✅ O afastamento da lateral esquerda no projeto arquitetônico está dentro do limite com relação ao limite permitido.")
    else: 
        st.write("🔴 O afastamento da lateral esquerda no projeto arquitetônico NÃO está dentro do limite com relação ao limite permitido.🔴")

    #altura topografia
    AlturaTopografia = 0
    AlturaTopografia = CotaCoroamento4 - CotaSoleiraNumerica4
    st.write(f"**Altura da Edificação de acordo com a Topografia:** {AlturaTopografia}")

    st.subheader("Documentação do Imóvel")
    if AreaDoLote5 != AreaDoLote:
        st.write("🔴 A área da documentação NÃO é a mesma do projeto arquitetônico 🔴")
    else:
        st.write("✅ A área da documentação é a mesma do projeto arquitetônico")

    if TestadaFrontal5 != TestadaFrontal4:
        st.write("🔴 A Testada Frontal na documentação NÃO é a mesma da Tesada Frontal da Topografia 🔴")
    else:
        st.write("✅ A Testada Frontal na documentação é a mesma da Tesada Frontal da Topografia")

    if TestadaFundo5 != TestadaFundo4:
        st.write("🔴 A Testada Fundos na documentação NÃO é a mesma da Tesada Fundos da Topografia 🔴")
    else:
        st.write("✅ A Testada Fundos na documentação é a mesma da Tesada Fundos da Topografia")

    if LateralDireito5 != LateralDireito4:
        st.write("🔴 A Lateral Direita na documentação NÃO é a mesma da Lateral Direita da Topografia 🔴")
    else:
        st.write("✅ A Lateral Direita na documentação é a mesma da Lateral Direita da Topografia")

    if LateralEsquerdo5 != LateralEsquerdo4:
        st.write("🔴 A Lateral Esquerda na documentação NÃO é a mesma da Lateral Esquerda da Topografia 🔴")
    else:
        st.write("✅ A Lateral Esquerda na documentação é a mesma da Lateral Esquerda da Topografia")

    if CotaSoleiraSeudh == CotaSoleiraNumerica4:
        st.write("✅ O valor da Cota da soleira da Seduh(GeoPortal) é a mesma da topografia")
    else:
        if abs(CotaSoleiraSeudh - CotaSoleiraNumerica4) <= 0.20:
            st.write("✅ O valor da Cota da soleira da Seduh(GeoPortal) possui uma diferença de + ou - 20cm com relação a topografia, situação aceitável")
        else:
            st.write("🔴 O valor da Cota da soleira da Seduh(GeoPortal) possui divergência, não aceitável, com relação a topografia 🔴")


    if opcao_principal == "Sim":
        if instituicao == "Não":
            st.write("🔴 Falta a Instituição de Condomínio.")
        if plano == "Não":
            st.write("🔴 Falta o Plano de Ocupação.")
        if ngb == "Não":
            st.write("🔴 Falta a NGB.")

    st.subheader("Topografia do Imóvel")
    
    # afastamentos
    if abs(AfastamentoFrontal4 - AfastamentoFrontal3) <= min(0.50, AfastamentoFrontal3 * 0.05):
        st.write("✅ O afastamento frontal na topografia está dentro do limite com relação ao projeto arquitetônico.")
    else: 
        st.write("🔴 O afastamento frontal na topografia NÃO está dentro do limite com relação ao projeto arquitetônico. 🔴")
        st.write(f"**Afastamento frontal de acordo com o Projeto Arquitetônico:** {AfastamentoFrontal3}")
        st.write(f"**Afastamento máximo e mínimo (5%) permitidos** {AfastamentoFrontal3 * 1.05} e {AfastamentoFrontal3 * 0.95} limitados a 50cm")
        st.write(f"**Afastamento frontal de acordo com a Topografia:** {AfastamentoFrontal4}")
        st.write("--------------------------------------")

    if abs(AfastamentoFundo4 - AfastamentoFundo3) <= min(0.50, AfastamentoFrontal3 * 0.05):
        st.write("✅ O afastamento fundos na topografia está dentro do limite com relação ao projeto arquitetônico.")
    else: 
        st.write("🔴 O afastamento fundos na topografia NÃO está dentro do limite com relação ao projeto arquitetônico. 🔴")
        st.write(f"**Afastamento fundos de acordo com o Projeto Arquitetônico:** {AfastamentoFundo3}")
        st.write(f"**Afastamento máximo e mínimo (5%) permitidos** {AfastamentoFundo3 * 1.05} e {AfastamentoFundo3 * 0.95} limitados a 50cm")
        st.write(f"**Afastamento fundos de acordo com a Topografia:** {AfastamentoFundo4}")
        st.write("--------------------------------------")   

    if abs(AfastamentoDireito4 - AfastamentoDireito3) <= min(0.50, AfastamentoFrontal3 * 0.05):
        st.write("✅ O afastamento da Lateral Direita na topografia está dentro do limite com relação ao projeto arquitetônico.")
    else: 
        st.write("🔴 O afastamento da Lateral Direita na topografia NÃO está dentro do limite com relação ao projeto arquitetônico. 🔴")
        st.write(f"**Afastamento da Lateal Direita de acordo com o Projeto Arquitetônico:** {AfastamentoDireito3}")
        st.write(f"**Afastamento máximo e mínimo (5%) permitidos** {AfastamentoDireito3 * 1.05} e {AfastamentoDireito3 * 0.95} limitados a 50cm")
        st.write(f"**Afastamento da Lateal Direita de acordo com a Topografia:** {AfastamentoDireito4}")
        st.write("--------------------------------------")      

    if abs(AfastamentoEsquerdo4 - AfastamentoEsquerdo3) <= min(0.50, AfastamentoFrontal3 * 0.05):
        st.write("✅ O afastamento da Lateral Esquerda na topografia está dentro do limite com relação ao projeto arquitetônico.")
    else: 
        st.write("🔴 O afastamento da Lateral Esquerda na topografia NÃO está dentro do limite com relação ao projeto arquitetônico. 🔴")
        st.write(f"**Afastamento da Lateal Esquerda de acordo com o Projeto Arquitetônico:** {AfastamentoEsquerdo3}")
        st.write(f"**Afastamento máximo e mínimo (5%) permitidos** {AfastamentoEsquerdo3 * 1.05} e {AfastamentoEsquerdo3 * 0.95} limitados a 50cm")
        st.write(f"**Afastamento da Lateal Direita de acordo com a Topografia:** {AfastamentoEsquerdo4}")
        st.write("--------------------------------------")

    #testadas
    if TestadaFrontal4 != TestadaFrontal3:
        st.write("🔴 A Testada Frontal (Frente do imóvel) da Topografia NÃO é a mesma da Arquitetura 🔴")
    else:
        st.write("✅ A Testada Frontal (Frente do imóvel) da Topografia é a mesma da Arquitetura")

    if TestadaFundo4 != TestadaFundo3:
        st.write("🔴 A Testada Fundos (Fundos do imóvel) da Topografia NÃO é a mesma da Arquitetura 🔴")
    else:
        st.write("✅ A Testada Fundos (Fundos do imóvel) da Topografia é a mesma da Arquitetura")

    if LateralDireito4 != LateralDireito3:
        st.write("🔴 A Testada da lateral direita (Lateral do imóvel) da Topografia NÃO é a mesma da Arquitetura 🔴")
    else:
        st.write("✅ A Testada da lateral direita (Lateral do imóvel) da Topografia é a mesma da Arquitetura")
      
    if LateralEsquerdo4 != LateralEsquerdo3:
        st.write("🔴 A Testada da lateral esquerda (Lateral do imóvel) da Topografia NÃO é a mesma da Arquitetura 🔴")
    else:
        st.write("✅ A Testada da lateral esquerda (Lateral do imóvel) da Topografia é a mesma da Arquitetura")
