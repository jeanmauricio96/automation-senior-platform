# Projeto Automacao Preenchimento de Ponto

Este projeto automatiza o preenchimento do ponto na plataforma Senior utilizando Selenium em Python.

---

## Pre-requisitos

* Python 3 instalado (versao recomendada: 3.8+)
* Navegador Google Chrome instalado
* Chromedriver compativel com a versao do seu Chrome

---

## Instalacao do Python e pip

Se voce ainda nao tem o Python instalado, siga os passos:

### Windows

1. Acesse o site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Baixe o instalador para Windows.
3. Durante a instalacao, **marque a opcao "Add Python to PATH"**.
4. Finalize a instalacao.

### Verifique se o Python e o pip foram instalados corretamente

Abra o Prompt de Comando e digite:

```bash
python --version
pip --version
```

### Instalacao das dependencias

Apos garantir que Python e pip estao instalados, instale as bibliotecas necessarias com:

```bash
pip install -r requirements.txt
```

### Arquivo requirements.txt

O projeto deve conter um arquivo requirements.txt com o seguinte conteudo:

```bash
selenium
python-dotenv
```

---

## Configuracao das variaveis de ambiente

Para manter suas credenciais seguras, utilizamos variaveis de ambiente.

### Passos para configurar

1. Crie um arquivo `.env` na raiz do projeto.

2. Adicione as seguintes variaveis no `.env`:

```bash
DB_USERNAME=seu_email@empresa.com.br
DB_PASSWORD=sua_senha
```

---

## ✉️ Configuracao de envio de e-mail (SMTP)

O script pode enviar notificacoes por e-mail, como confirmacao de ponto registrado ou erros de execucao. Para isso, e necessario configurar as variaveis SMTP no arquivo `.env`.

### 📌 Variaveis necessarias no `.env`:

```env
EMAIL_FROM=seu_email@gmail.com
EMAIL_TO=destinatario@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASS=sua_senha_de_app
```

> ⚠️ **Importante:** O `SMTP_PASS` **nao e sua senha do Gmail**, e sim uma **senha de aplicativo**, gerada especialmente para esse script.

---

## 🔐 Como gerar uma senha de app no Gmail

Se voce usa Gmail, siga estes passos para gerar uma senha especifica para uso com scripts:

### Pre-requisitos:

* Verificacao em duas etapas ativada na sua conta Google.
* Conta Google com acesso a [Senhas de app](https://myaccount.google.com/apppasswords).

### Passos para gerar a senha:

1. Acesse: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Faca login na sua conta Google.
3. Em "Selecionar aplicativo", escolha **Outro (nome personalizado)**.
4. Digite por exemplo: `automacao-ponto`.
5. Clique em **Gerar**.
6. O Google exibira uma senha de 16 caracteres. **Copie-a**.
7. Use essa senha no campo `SMTP_PASS` do seu arquivo `.env`.

> Nunca compartilhe essa senha. Guarde com seguranca.

---

## Execucao do script

Com as dependencias instaladas e as variaveis configuradas, execute o script:

```bash
python main.py
```

O script abrira o navegador, fara o login na plataforma Senior e preenchera o ponto automaticamente.

---

## Observacoes importantes

* Nunca compartilhe o arquivo `.env` para proteger suas credenciais.
* Certifique-se de usar o Chromedriver compativel com sua versao do Google Chrome.
* Ajuste os tempos de espera (`time.sleep()`) conforme a velocidade da sua conexao e computador.