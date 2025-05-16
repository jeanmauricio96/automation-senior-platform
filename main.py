import os
import random
import logging
import time
import smtplib
from logging.handlers import TimedRotatingFileHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from datetime import datetime, timedelta
from email.mime.text import MIMEText

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, 'ponto.log')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    filename=log_path,
    when='midnight',        
    interval=1,             
    backupCount=7,          
    encoding='utf-8',
    utc=False               
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

load_dotenv()

USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

def enviar_email(subject, body):
    try:
        from_email = os.getenv('EMAIL_FROM')
        to_email = os.getenv('EMAIL_TO')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASS')

        if not all([from_email, to_email, smtp_server, smtp_port, smtp_user, smtp_pass]):
            logger.error("Variáveis de ambiente para envio de e-mail estão incompletas.")
            return

        try:
            smtp_port = int(smtp_port)
        except ValueError:
            logger.error(f"Porta SMTP inválida: {smtp_port}")
            return

        subject = subject or ""
        body = body or ""

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()

        logger.info("E-mail enviado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")

def main():
    start_time = time.time()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-accelerated-2d-canvas")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        logger.info('1. Configurando o navegador')
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 30)
    except Exception as e:
        logger.error(f"Falha ao iniciar Selenium WebDriver: {e}")
        enviar_email(
            "Erro ao iniciar script de ponto",
            f"Falha ao iniciar Selenium WebDriver:\n{e}"
        )
        return

    try:
        logger.info('2. Acessando plataforma')
        driver.get("https://platform.senior.com.br/login/?redirectTo=https%3A%2F%2Fplatform.senior.com.br%2Fsenior-x%2F")

        logger.info('3. Adicionando o E-mail')
        driver.find_element(By.ID, "username-input-field").send_keys(USERNAME)
        driver.find_element(By.ID, "nextBtn").click()

        time.sleep(3)

        logger.info('4. Adicionando a Senha')
        driver.find_element(By.ID, "password-input-field").send_keys(PASSWORD)
        driver.find_element(By.ID, "loginbtn").click()

        time.sleep(3)

        logger.info('5. Acessando a pagina de marcações do Sênior')
        driver.get("https://platform.senior.com.br/senior-x/#/Gest%C3%A3o%20de%20Pessoas%20%7C%20HCM/1/res:%2F%2Fsenior.com.br%2Fmenu%2Frh%2Fponto%2Fgestaoponto%2Fcolaborador?category=frame&link=https:%2F%2Fweb32.seniorcloud.com.br:36701%2Fgestaoponto-frontend%2Fuser%2Fredirect%3Factiveview%3Demployee%26portal%3Dg7&withCredentials=true&helpUrl=http:%2F%2Fdocumentacao.senior.com.br%2Fgestao-de-pessoas-hcm%2F6.10.4%2F%23gestao-ponto%2Fnova-interface%2Fapuracao-do-ponto%2Fcolaborador%2Fmeus-acertos-de-ponto.htm&r=0")

        time.sleep(10)

        logger.info('6. Buscando o campo para marcação')
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "custom_iframe")))

        hoje_datetime = datetime.now()
        if hoje_datetime.weekday() in [5, 6]:
            logger.info("Hoje é fim de semana. Não será feito registro.")
            return

        hoje = datetime.now().strftime("%Y-%m-%d")
        id_dinamico = f"dia_{hoje}_InserirMarcacao"

        try:
            registrar_btn = wait.until(EC.element_to_be_clickable((By.ID, id_dinamico)))
            registrar_btn.click()
        except Exception:
            logger.info(f"{hoje} - O ponto de hoje já foi registrado.")
            enviar_email(
                "Ponto já registrado",
                f"O ponto do dia {hoje} já foi registrado, não houve nova marcação."
            )
            return

        logger.info('7. Criando as marcações para adicionar os horários e justificativas')
        for _ in range(4):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addMarcacao")))
            btn.click()
            time.sleep(2)

        logger.info('8. Adicionando horários e justificativas')
        def gerar_horario(base_str, minutos_range=10):
            base = datetime.strptime(base_str, "%H:%M")
            aleatorio = random.randint(0, minutos_range)
            return base + timedelta(minutes=aleatorio)

        entrada = gerar_horario("08:00", 10)
        saida_almoco = gerar_horario("12:00", 10)
        retorno_almoco = saida_almoco + timedelta(hours=1)

        antes_almoco = saida_almoco - entrada
        tempo_necessario = timedelta(hours=10, minutes=0) #<========= Carga Horaria (10 horas está no padrão de recuperação de Banco de horas)
        depois_almoco = tempo_necessario - antes_almoco

        limite_saida_final = datetime.strptime("19:00", "%H:%M")
        saida_final_max = retorno_almoco + depois_almoco
        saida_final = min(saida_final_max, limite_saida_final)

        horarios = [entrada, saida_almoco, retorno_almoco, saida_final]
        horarios_formatados = [h.strftime("%H:%M") for h in horarios]

        for i, hora in enumerate(horarios_formatados):
            driver.find_element(By.ID, f"marcacaoTime-{i}").send_keys(hora)
            driver.find_element(By.ID, f"justificative-{i}").click()
            driver.find_element(By.ID, "justificative_4").click()
            time.sleep(1.5)

        logger.info('9. Salvando as alterações')
        driver.find_element(By.ID, "saveAppointment").click()

        logger.info(f"{hoje} - {horarios_formatados} - Trabalho Externo")
        enviar_email(
            "Registro de ponto realizado",
            f"Ponto do dia {hoje} registrado com horários: {horarios_formatados}."
        )

    except Exception as e:
        logger.error(f"Erro geral no fluxo do script: {e}")
        enviar_email(
            "Erro no script de ponto",
            f"Ocorreu um erro durante a execução do script:\n{e}"
        )
    finally:
        driver.quit()
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Tempo total de execução: {execution_time:.2f} segundos")

if __name__ == "__main__":
    main()