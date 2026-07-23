import os
import sys
import threading
import time
import webview
import pyautogui

NOME_DO_PERFIL = "MIKETV"

# MAPA OFICIAL DE LINKS DIRETOS PARA EVITAR A GRELA LATERAL
MAPA_CANAIS = {
    "1": "https://nostv.pt",
    "2": "https://nostv.pt",
    "3": "https://nostv.pt",
    "4": "https://nostv.pt-noticias"
}

NOMES_CANAIS_EXIBICAO = {
    "1": "RTP 1", "2": "SIC", "3": "TVI", "4": "SIC NOTÍCIAS"
}


def injetar_splash_gira(janela, segundos, mensagem):
    """Injeta a cortina escura com animação e auto-remoção no final da contagem."""
    try:
        script_splash = f"""
        (function() {{
            // 1. Limpar o intervalo anterior se ele já existir na janela global
            if (window.intervaloSplashActivo) {{
                clearInterval(window.intervaloSplashActivo);
            }}

            // 2. Procurar ou criar o ecrã splash
            var box = document.getElementById('nos-tv-box-splash');
            if (!box) {{
                box = document.createElement('div');
                box.id = 'nos-tv-box-splash';
                box.style.position = 'fixed'; box.style.top = '0'; box.style.left = '0';
                box.style.width = '100vw'; box.style.height = '100vh';
                box.style.background = 'radial-gradient(circle, #1a1a24 0%, #0d0d13 100%)';
                box.style.color = '#ffffff'; box.style.display = 'flex';
                box.style.flexDirection = 'column'; box.style.justifyContent = 'center';
                box.style.alignItems = 'center'; box.style.textAlign = 'center';
                box.style.fontFamily = "'Segoe UI', sans-serif"; box.style.zIndex = '99999999';
                box.style.pointerEvents = 'none'; box.style.userSelect = 'none';

                var content = document.createElement('div');
                content.style.background = 'rgba(255, 255, 255, 0.03)';
                content.style.padding = '40px'; content.style.borderRadius = '24px';
                content.style.border = '1px solid rgba(255, 255, 255, 0.05)';
                content.style.boxShadow = '0 20px 50px rgba(0,0,0,0.5)';

                var tvIcon = document.createElement('div');
                tvIcon.innerText = "📺"; tvIcon.style.fontSize = '90px'; tvIcon.style.marginBottom = '20px';
                tvIcon.style.animation = 'pulsar 2s infinite ease-in-out';

                var estilo = document.createElement('style');
                estilo.innerHTML = "@keyframes pulsar {{ 0% {{ transform: scale(1); opacity: 0.8; }} 50% {{ transform: scale(1.06); opacity: 1; }} 100% {{ transform: scale(1); opacity: 0.8; }} }}";
                document.head.appendChild(estilo);

                var texto = document.createElement('h1');
                texto.id = 'splash-texto-id';
                texto.style.fontSize = '42px'; texto.style.fontWeight = '700'; texto.style.margin = '0 0 20px 0';

                var crono = document.createElement('div');
                crono.id = 'splash-cronometro-id';
                crono.style.fontSize = '130px'; crono.style.fontWeight = '800'; crono.style.color = '#ffca28';
                crono.style.textShadow = '0 0 30px rgba(255, 202, 40, 0.3)';

                content.appendChild(tvIcon); content.appendChild(texto); content.appendChild(crono);
                box.appendChild(content); document.body.appendChild(box);
            }}

            // 3. Atualizar sempre o texto e repor o estilo visual visível
            document.getElementById('splash-texto-id').innerHTML = "{mensagem}";
            box.style.display = 'flex'; 

            // 4. Iniciar nova contagem decrescente
            var tempo = {segundos};
            var elCrono = document.getElementById('splash-cronometro-id');
            elCrono.innerText = tempo + "s";

            window.intervaloSplashActivo = setInterval(function() {{
                tempo--;
                if (tempo >= 0) {{
                    elCrono.innerText = tempo + "s";
                }} else {{
                    clearInterval(window.intervaloSplashActivo);
                    elCrono.innerText = "A iniciar...";

                    // 5. Remove o ecrã após 1 segundo para o idoso ver a transição
                    setTimeout(function() {{
                        if (box && box.parentNode) {{
                            box.parentNode.removeChild(box);
                        }}
                    }}, 1000);
                }}
            }}, 1000);
        }})();
        """
        janela.evaluate_js(script_splash)
    except Exception:
        pass

# Exemplo genérico se quiseres pelo menos registar o erro para depuração
import logging

def remover_splash_gira(janela):
    try:
        janela.evaluate_js("...")
    except Exception as e:
        logging.warning(f"Não foi possível remover a splash screen: {e}")



def mapear_atalhos_teclado(janela):
    """Parte 2 Corrigida: Simula a rota linear oficial (Aba Canais -> Clica no Canal) na troca"""
    while True:
        try:
            script_teclado = """
            (function() {
                if (window.ultimoCodigoTecla) {
                    var tecla = window.ultimoCodigoTecla;
                    window.ultimoCodigoTecla = null; return tecla;
                }
                if (!window.tecladoConfigurado) {
                    window.tecladoConfigurado = true;
                    window.addEventListener('keydown', function(e) {
                        if (['1','2','3','4', 'F11', 'Escape'].includes(e.key)) {
                            window.ultimoCodigoTecla = e.key;
                        }
                    });
                }
                return null;
            })();
            """
            tecla_carregada = janela.evaluate_js(script_teclado)

            if tecla_carregada and tecla_carregada in MAPA_CANAIS:
                nome_canal = NOMES_CANAIS_EXIBICAO.get(tecla_carregada, "Canal")
                print(f"[BOX CONTROL] Botão {tecla_carregada} -> A iniciar rota oficial para: {nome_canal}")

                # 1. REMOVE O FULLSCREEN ATUAL PARA LIBERTAR OS MENUS
                pyautogui.press('escape')
                time.sleep(0.4)

                # 2. INJETA O SPLASH ANIMADO IMEDIATAMENTE (Cortina protetora de 20 segundos para todo o fluxo)
                injetar_splash_gira(janela, 20,
                                    f"A MUDAR PARA A {nome_canal.upper()}<br>Por favor, aguarde pela imagem")
                time.sleep(0.5)

                # 3. PASSO DA ABA CANAIS: Clica no menu superior para abrir a grelha
                script_voltar_grelha = """
                (function() {
                    var abas = Array.from(document.querySelectorAll('a, button, span, p'));
                    var btn = abas.find(el => el.textContent && (el.textContent.trim() === "Canais" || el.textContent.trim() === "Televisão" || el.textContent.trim() === "Guia TV" || el.textContent.trim() === "Direto"));
                    if (btn) { btn.click(); return true; }
                    return false;
                })();
                """
                janela.evaluate_js(script_voltar_grelha)
                print("[BACKGROUND] Aba Canais acionada. A aguardar renderização...")

                # DELAY DE RENDERIZAÇÃO: Aguarda 6 segundos para a NOS desenhar a lista de canais no fundo
                time.sleep(6)

                # 4. PASSO DA ESCOLHA DO CANAL: Localiza e sintoniza o canal escolhido de forma legítima
                canal_alvo_limpo = nome_canal.replace(" ", "")
                script_clicar_canal_teclado = f"""
                (function() {{
                    var elementos = Array.from(document.querySelectorAll('p, span, img, div, h4'));
                    var alvoCanal = elementos.find(el => {{
                        var txt = el.textContent ? el.textContent.trim().replace(/\s+/g, "") : "";
                        var alt = el.alt ? el.alt.trim().replace(/\s+/g, "") : "";
                        return (/{canal_alvo_limpo}/i).test(txt) || (/{canal_alvo_limpo}/i).test(alt);
                    }});
                    if (alvoCanal) {{
                        var item = alvoCanal.closest('a') || alvoCanal.closest('button') || alvoCanal.closest('[role="button"]') || alvoCanal;
                        item.click();
                        return true;
                    }}
                    return false;
                }})();
                """
                janela.evaluate_js(script_clicar_canal_teclado)
                print(f"[BACKGROUND] Clique enviado ao alvo {nome_canal}. A processar buffer de vídeo...")

                # DELAY DE STREAMING: Aguarda 12 segundos para o leitor de vídeo arrancar o som e imagem
                time.sleep(12)

                # 5. REMOVE A CORTINA DO SPLASH PARA LIBERTAR A TELA
                remover_splash_gira(janela)
                time.sleep(0.5)

                # 6. EXECUTA O CLIQUE DE REPOSIÇÃO DO FULLSCREEN NA TUA COORDENADA CALIBRADA (940, 677)
                alvo_fs_x, alvo_y_fs = 940, 677
                print(f"[AÇÃO TECLADO] A reativar ecrã inteiro em: X={alvo_fs_x}, Y={alvo_y_fs}")
                pyautogui.moveTo(alvo_fs_x, alvo_y_fs, duration=0.5)
                time.sleep(0.2)
                pyautogui.click(alvo_fs_x, alvo_y_fs)
                time.sleep(0.2)
                pyautogui.click(alvo_fs_x, alvo_y_fs)
                time.sleep(0.5)

                # Força a ocultação definitiva da barra do Windows
                pyautogui.press('f')
                print(f"[SEQUÊNCIA] Transição para {nome_canal} concluída com sucesso!")

            elif tecla_carregada in ['F11', 'Escape']:
                janela.toggle_fullscreen()
                time.sleep(0.5)
        except Exception as e:
            print(f"Aviso na linha de comandos do teclado: {e}")
            break
        time.sleep(0.15)


def fluxo_linear_box(janela):
    """Parte 3: Sequência inicial automática com o Splash por cima e clique calibrado (940, 677)"""
    try:
        # Carrega o site base da NOS para detetar a sessão guardada
        janela.load_url("https://nostv.pt")

        # =========================================================================
        # 1. PASSO DO PERFIL - INJETA O SPLASH POR CIMA DO SITE E AGUARDA (5 segundos)
        # =========================================================================
        print("[ROTINA] 1. A iniciar a Box e a injetar ecrã de carregamento...")
        time.sleep(3)  # Tempo para a estrutura inicial da página responder

        # Injeta o Splash gigante por cima do ecrã com 26 segundos de tempo total
        injetar_splash_gira(janela, 26, "A INICIAR A BOX DE TELEVISÃO...<br>Por favor, aguarde que o sistema carregue")
        time.sleep(4)  # Completa o tempo de leitura do perfil em background

        perfil_maiusculo = NOME_DO_PERFIL.upper()
        script_perfil = f"""
        (function() {{
            var elementos = Array.from(document.querySelectorAll('p, span, div, h1, h2, h3'));
            var alvo = elementos.find(el => el.textContent && el.textContent.trim().toUpperCase() === "{perfil_maiusculo}");
            if (alvo) {{
                var botao = alvo.closest('button') || alvo.closest('a') || alvo.closest('[role="button"]') || alvo;
                botao.click();
                return true;
            }}
            return false;
        }})();
        """
        janela.evaluate_js(script_perfil)
        print("[ROTINA] Perfil MIKETV acionado.")

        # =========================================================================
        # 2. VAI PARA A ABA DE CANAIS (Aguardando 7 segundos com o Splash ativo)
        # =========================================================================
        print("[ROTINA] 2. A abrir a grelha de canais...")
        time.sleep(7)

        script_menu_canais = """
        (function() {
            var abas = Array.from(document.querySelectorAll('a, button, span, p'));
            var btn = abas.find(el => el.textContent && (el.textContent.trim() === "Canais" || el.textContent.trim() === "Televisão" || el.textContent.trim() === "Guia TV" || el.textContent.trim() === "Direto"));
            if (btn) { btn.click(); return true; }
            return false;
        })();
        """
        janela.evaluate_js(script_menu_canais)
        print("[ROTINA] Aba de Canais acionada.")

        # =========================================================================
        # 3. ESCOLHE A POSIÇÃO 2 (SIC) (Aguardando 7 segundos com o Splash ativo)
        # =========================================================================
        print("[ROTINA] 3. A sintonizar a SIC de forma automática...")
        time.sleep(7)

        script_clicar_sic = """
        (function() {
            var elementos = Array.from(document.querySelectorAll('p, span, img, div, h4'));
            var alvoSic = elementos.find(el => {
                var txt = el.textContent ? el.textContent.trim() : "";
                var alt = el.alt ? el.alt.trim() : "";
                return (/^sic$/i).test(txt) || (/^sic$/i).test(alt);
            });
            if (alvoSic) {
                var item = alvoSic.closest('a') || alvoSic.closest('button') || alvoSic.closest('[role="button"]') || alvoSic;
                item.click(); return true;
            }
            return false;
        })();
        """
        janela.evaluate_js(script_clicar_sic)
        print("[ROTINA] SIC selecionada.")

        # =========================================================================
        # 4. BUFFER DE STREAMING E ATIVAÇÃO DO FULLSCREEN (940, 677)
        # =========================================================================
        print("[ROTINA] 4. A carregar o sinal de vídeo da SIC...")
        time.sleep(12)  # Tempo final para o leitor de vídeo renderizar e o som assentar

        # REMOVE EM DEFINITIVO A CORTINA DO SPLASH PARA O RATO PODER INTERAGIR
        remover_splash_gira(janela)
        time.sleep(0.5)

        # Executa o clique mecânico na sua coordenada calibrada da janela pequena
        alvo_x, alvo_y = 940, 677
        print(f"[AÇÃO] A executar o clique mecânico de Fullscreen em: X={alvo_x}, Y={alvo_y}")

        pyautogui.moveTo(alvo_x, alvo_y, duration=0.6)
        time.sleep(0.2)
        pyautogui.click(alvo_x, alvo_y)
        time.sleep(0.3)
        pyautogui.click(alvo_x, alvo_y)
        time.sleep(0.5)

        # Força o ecrã inteiro do Windows e esconde a barra de tarefas
        janela.toggle_fullscreen()
        pyautogui.press('f')
        print("[ROTINA] Box TV inicializada com sucesso na SIC!")

    except Exception as e:
        print(f"[AVISO] Interrupção na rotina: {e}")


def iniciar_app():
    """Garante o arranque da janela maximizada e as margens sem erros de sintaxe"""
    data_dir = os.path.join(os.path.expanduser("~"), ".nostv_app_data")
    os.makedirs(data_dir, exist_ok=True)

    print("A iniciar a NOS TV Box nativa completa...")

    # Abre maximizado para que o ponto 940, 677 caia exatamente em cima do botão
    janela = webview.create_window(
        title="NOS TV Box",
        url="about:blank",  # Inicia limpo antes de receber o load_url da rotina
        width=1920, height=1080,
        maximized=True,
        text_select=False,
    )

    threading.Thread(target=mapear_atalhos_teclado, args=(janela,), daemon=True).start()
    threading.Thread(target=fluxo_linear_box, args=(janela,), daemon=True).start()

    webview.start(private_mode=False, storage_path=data_dir)


if __name__ == "__main__":
    iniciar_app()
