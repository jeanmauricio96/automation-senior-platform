
# Projeto Automacao Preenchimento de Ponto

Este projeto automatiza o preenchimento do ponto na plataforma Senior utilizando Selenium em Python.

---

## Pre-requisitos

* Python 3 instalado (versão recomendada: 3.8+)
* Navegador Google Chrome instalado
* Chromedriver compatível com a versão do seu Chrome

---

## Instalação do Python e pip

Se você ainda não tem o Python instalado, siga os passos:

### Windows

1. Acesse o site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Baixe o instalador para Windows.
3. Durante a instalação, **marque a opção "Add Python to PATH"**.
4. Finalize a instalação.

### Verifique se o Python e o pip foram instalados corretamente

Abra o Prompt de Comando e digite:

```bash
python --version
pip --version
```

### Instalação das dependências

Após garantir que Python e pip estão instalados, instale as bibliotecas necessárias com:

```bash
pip install -r requirements.txt
```

### Arquivo requirements.txt

O projeto deve conter um arquivo requirements.txt com o seguinte conteúdo:

```bash
selenium
python-dotenv
```

---

## Configuração das variáveis de ambiente

Para manter suas credenciais seguras, utilizamos variáveis de ambiente.

### Passos para configurar

1. Crie um arquivo `.env` na raiz do projeto.

2. Adicione as seguintes variáveis no `.env`:

```bash
DB_USERNAME=seu_email@empresa.com.br
DB_PASSWORD=sua_senha
```
---

### 📧 Envio de E-mail (Opcional)

O script pode enviar notificações por e-mail em casos como sucesso na marcação de ponto ou ocorrência de erros. Para habilitar ou desabilitar esse recurso, configure a variável de ambiente EMAIL_ENABLED no seu arquivo .env.

## ✅ Variável de controle:

```env
EMAIL_ENABLED=true  # Para habilitar o envio de e-mails
EMAIL_ENABLED=false # Para desabilitar (padrão seguro)
```

---

## ✉️ Configuração de envio de e-mail (SMTP)

O script pode enviar notificações por e-mail, como confirmação de ponto registrado ou erros de execução. Para isso, é necessário configurar as variáveis SMTP no arquivo `.env`.

### 📌 Variáveis necessárias no `.env`:

```env
EMAIL_FROM=seu_email@gmail.com
EMAIL_TO=destinatario@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASS=sua_senha_de_app
EMAIL_ENABLED=true  # Defina como 'false' para desabilitar o envio de e-mails
```

> ⚠️ **Importante:** O `SMTP_PASS` **não é sua senha do Gmail**, é sim uma **senha de aplicativo**, gerada especialmente para esse script.

---

## 🔐 Como gerar uma senha de app no Gmail

Se você usa Gmail, siga estes passos para gerar uma senha específica para uso com scripts:

### Pré-requisitos:

* Verificação em duas etapas ativada na sua conta Google.
* Conta Google com acesso a [Senhas de app](https://myaccount.google.com/apppasswords).

### Passos para gerar a senha:

1. Acesse: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Faça login na sua conta Google.
3. Em "Selecionar aplicativo", escolha **Outro (nome personalizado)**.
4. Digite por exemplo: `automacao-ponto`.
5. Clique em **Gerar**.
6. O Google exibirá uma senha de 16 caracteres. **Copie-a**.
7. Use essa senha no campo `SMTP_PASS` do seu arquivo `.env`.

> Nunca compartilhe essa senha. Guarde com segurança.

---

## Execução do script

Com as dependências instaladas e as variáveis configuradas, execute o script:

```bash
python main.py
```

O script abrirá o navegador, fará o login na plataforma Senior e preencherá o ponto automaticamente.

---

## Observações importantes

* Nunca compartilhe o arquivo `.env` para proteger suas credenciais.
* Certifique-se de usar o Chromedriver compatível com sua versão do Google Chrome.
* Ajuste os tempos de espera (`time.sleep()`) conforme a velocidade da sua conexão e computador.