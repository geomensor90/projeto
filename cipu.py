import streamlit as st
import requests
import time
import pymupdf as fitz


st.set_page_config(page_title="Análise de Projeto", layout="wide")

def get_input_float(label):
    valor = st.text_input(label, "0")
    try:
        return float(valor)
    except ValueError:
        return 0.0

AfastamentoFrontal1 = 0
AfastamentoFundo1 = 0
AfastamentoDireito1 = 0
AfastamentoEsquerdo1 = 0
TaxaOcupacao1 = 0
AlturaMaxima1 = 0
CoeficienteAprovBasico1 = 0
CoeficienteAprovMaximo1 = 0
TaxaPermeabilidade1 = 0
CotaSoleira1 = 0
AfastamentoFrontal3 = 0
AfastamentoFundo3 = 0
AfastamentoDireito3 = 0
AfastamentoEsquerdo3 = 0
TestadaFrontal3 = 0
TestadaFundo3 = 0
LateralDireito3 = 0
LateralEsquerdo3 = 0
Altura3 = 0
AreaPermeavel3 = 0
AreaDoLote = 0
AreaTotalConstrucao3 = 0
AreaConstruaoTerreo3 = 0
CotaCoroamento3 = 0
CotaSoleiraNumerica3 = 0
CotaSoleira3 = 0
AfastamentoFrontal4 = 0
AfastamentoFundo4 = 0
AfastamentoDireito4 = 0
AfastamentoEsquerdo4 = 0
TestadaFrontal4 = 0
TestadaFundo4 = 0
LateralDireito4 = 0
LateralEsquerdo4 = 0
CotaCoroamento4 = 0
CotaSoleiraNumerica4 = 0
CotaSoleira4 = 0
TestadaFrontal5 = 0
TestadaFundo5 = 0
LateralDireito5 = 0
LateralEsquerdo5 = 0
AreaDoLote5 = 0
CotaSoleiraSeudh = 0
AreaVerdeConstruida = 0 

with st.expander("📝 **Observações - Comece por aqui**"):
    # Escolha do modo
    st.write("Utilizar ponto ao em vez de vírgula. Ex.: 13.45")
    st.write("O buscador automático procura apenas pela LUOS, caso o imóvel não tenha LUOS, deverá ser utilizado a fórma **Preenchimento Manual** no próximo tópico")
    st.write("Versão 0.2. Corrigido: textos, importação automática, verificações extras, mais campos de preenchimento")
    st.write("Versão 0.3. Corrigido: importação automática")


with st.expander("📝 **Passo 1: Parâmetros Urbanísticos do Terreno**"):
    # Escolha do modo
    modo = st.radio("Escolha o modo de entrada dos parâmetros urbanísticos:", ["Extração Automática", "Preenchimento Manual"])

    if modo == "Extração Automática":
        codigo = st.text_input("Informe o CIPU", "418924")

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
                try:
                    def parse_float(valor_2):
                        try:
                            return float(valor_2.strip().replace(",", "."))
                        except:
                            return 0
                    AfastamentoFrontal1 = parse_float(linhas[106])
                    AfastamentoFundo1 = parse_float(linhas[107])
                    AfastamentoDireito1 = parse_float(linhas[108])
                    AfastamentoEsquerdo1 = parse_float(linhas[101])
                    TaxaOcupacao1 = parse_float(linhas[104])
                    AlturaMaxima1 = parse_float(linhas[87])
                    CoeficienteAprovBasico1 = parse_float(linhas[103])
                    CoeficienteAprovMaximo1 = parse_float(linhas[109])
                    TaxaPermeabilidade1 = parse_float(linhas[86])
                    CotaSoleira1 = linhas[83]
                except IndexError:
                    st.error("Erro ao extrair informações. Verifique se o PDF está no formato esperado.")
                    st.stop()

            except Exception as e:
                st.error(f"Erro ao extrair texto do PDF: {e}")
            st.subheader("📌 Parâmetros Urbanísticos Extraídos Automaticamente (Apenas para Consulta)")
            st.markdown(f"**Afastamento Frontal:** {AfastamentoFrontal1}")
            st.markdown(f"**Afastamento Fundo:** {AfastamentoFundo1}")
            st.markdown(f"**Afastamento Direito:** {AfastamentoDireito1}")
            st.markdown(f"**Afastamento Esquerdo:** {AfastamentoEsquerdo1}")
            st.markdown(f"**Taxa de Ocupação:** {TaxaOcupacao1}")
            st.markdown(f"**Altura Máxima:** {AlturaMaxima1}")
            st.markdown(f"**Coeficiente Aproveitamento Básico:** {CoeficienteAprovBasico1}")
            st.markdown(f"**Coeficiente Aproveitamento Máximo:** {CoeficienteAprovMaximo1}")
            st.markdown(f"**Taxa de Permeabilidade:** {TaxaPermeabilidade1}")
            st.markdown(f"**Cota de Soleira:** {CotaSoleira1}")
    else:
        # Campos para entrada manual
        

        AfastamentoFrontal1 = get_input_float("Afastamento Frontal")
        AfastamentoFundo1 = get_input_float("Afastamento Fundo")
        AfastamentoDireito1 = get_input_float("Afastamento Direito")
        AfastamentoEsquerdo1 = get_input_float("Afastamento Esquerdo")
        TaxaOcupacao1 = get_input_float("Taxa de Ocupação - Ex.:50")
        AlturaMaxima1 = get_input_float("Altura Máxima")
        CoeficienteAprovBasico1 = get_input_float("Coeficiente Aproveitamento Básico - Ex.:2")
        CoeficienteAprovMaximo1 = get_input_float("Coeficiente Aproveitamento Máximo - Ex.:3")
        TaxaPermeabilidade1 = get_input_float("Taxa de Permeabilidade  - Ex.:80")
        CotaSoleira1 = st.radio(
        "Posição da Cota de Soleira no parâmetro Urbanístico:",
        [
            "Ponto Médio da Edificação",
            "Cota Altimétrica média do Lote",
            "Ponto Médio da Testada Frontal"
        ]
        )


#segundo tópico - dados do projeto
with st.expander("**📝 Passo 2: Dados do Projeto**"):
    # Campos para entrada manual
    AreaDoLote = get_input_float("Área do Lote (terreno)- Projeto Arquitetônico")
    st.write("-----------------")

    st.write(f"Afastamento Frontal mínimo permitido: {AfastamentoFrontal1}") 
    AfastamentoFrontal3 = get_input_float("Afastamento Frontal - Projeto Arquitetônico")
    if AfastamentoFrontal3 < AfastamentoFrontal1:
        st.markdown(f"🔴 **O afastamento frontal é inferior ao mínimo permitido** 🔴")
    st.write("-----------------")

    st.markdown(f"Afastamento Fundo mínimo permitido: {AfastamentoFundo1}")
    AfastamentoFundo3 = get_input_float("Afastamento Fundo - Projeto Arquitetônico")
    if AfastamentoFundo3 < AfastamentoFundo1:
        st.markdown(f"🔴 **O afastamento de fundo é inferior ao mínimo permitido** 🔴")
    st.write("-----------------")

    st.markdown(f"Afastamento Direito mínimo permitido: {AfastamentoDireito1}")
    AfastamentoDireito3 = get_input_float("Afastamento Direito - Projeto Arquitetônico")
    if AfastamentoDireito3 < AfastamentoDireito1:
        st.markdown(f"🔴 **O afastamento da lateral direita é inferior ao mínimo permitido** 🔴")
    st.write("-----------------")

    st.markdown(f"Afastamento Esquerdo mínimo permitido: {AfastamentoEsquerdo1}")
    AfastamentoEsquerdo3 = get_input_float("Afastamento Esquerdo - Projeto Arquitetônico")
    if AfastamentoEsquerdo3 < AfastamentoEsquerdo1:
        st.markdown(f"🔴 **O afastamento da lateral esquerda é inferior ao mínimo permitido** 🔴")
    st.write("-----------------")

    st.markdown(f"Altura Máxima: {AlturaMaxima1}")
    Altura3 = get_input_float("Altura (m) - Projeto Arquitetônico")
    if Altura3 > AlturaMaxima1:
        st.markdown(f"🔴 **Altura Máxima excedida** 🔴")    
    st.write("-----------------")

    st.markdown(f"Área mínima permeável: {AreaDoLote * (TaxaPermeabilidade1/100)}")
    AreaPermeavel3 = get_input_float("Área Permável - Projeto Arquitetônico")
    if AreaPermeavel3 < (AreaDoLote * (TaxaPermeabilidade1/100)):
        st.markdown(f"🔴 **O projeto não possui a área de permeabilidade mínima** 🔴")   
    st.write("-----------------")

    st.markdown(f"Área total de construção permitida: {AreaDoLote * CoeficienteAprovBasico1}")
    AreaTotalConstrucao3 = get_input_float("Área total da Construção - Projeto Arquitetônico")
    if AreaTotalConstrucao3 > (AreaDoLote * CoeficienteAprovBasico1):
        st.markdown(f"🔴 **Extrapolado o coeficiente de aproveitamento básico do lote** 🔴")  
    st.write("-----------------")

    st.markdown(f"Áreade construção do térreo (Para cálculo da taxa de ocupação): {AreaDoLote * (TaxaOcupacao1/100)}")
    AreaConstruaoTerreo3 = get_input_float("Área de construção do térreo (para cálculo do coeficiente de aproveitamento) - Projeto Arquitetônico")
    if AreaConstruaoTerreo3 > (AreaDoLote * (TaxaOcupacao1/100)):
        st.markdown(f"🔴 **Extrapolado o coeficiente de aproveitamento do lote** 🔴")  
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
        st.markdown("**❌ Falta a cota da soleira e distância até o coroamento da edificação**")
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

    #área verde
    st.write(f"**🌳 Área verde no projeto:** {AreaVerdeConstruida}")
    st.write(f"**Área de permeabilidade mínima:** {AreaVerdeMinima}")     
    if AreaVerdeConstruida >= AreaVerdeMinima:
        st.write("✅ Área permeável dentro dos limites")
    else:
        st.write("🔴 Área verde insuficiente 🔴")
        
    #taxa de ocupação
    st.write(f"**🔳 Área da Taxa de Ocupação do projeto:** {AreaConstruaoTerreo3}")
    st.write(f"**Área da Taxa de Ocupação permitida para o lote:** {CoeficienteAproveitamentoReal}")     
    if AreaConstruaoTerreo3 > CoeficienteAproveitamentoReal:
        st.write("🔴 Taxa de ocupação ultrapassada 🔴")
    else:
        st.write("✅ Taxa de ocupação atendida")
    
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

