import requests
import logging
import base64
import os

graph_endpoint = "https://graph.microsoft.com/v1.0"


def send_email(access_token, subject, body, recipients, user_email, attachments=None):
    try:
        url = f"{graph_endpoint}/users/{user_email}/sendMail"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        attachment_data = []
        if attachments:
            for attachment in attachments:
                if not os.path.exists(attachment['file_path']):
                    raise FileNotFoundError(f"Arquivo {attachment['file_path']} não encontrado")

                encoded_content = encode_file(attachment['file_path'])
                attachment_data.append({
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": attachment['file_name'],
                    "contentBytes": encoded_content,
                    "contentType": attachment['content_type']
                })

        email_msg = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body
                },
                "toRecipients": [{"emailAddress": {"address": recipient}} for recipient in recipients],
                "attachments": attachment_data
            },
            "saveToSentItems": "true"
        }

        response = requests.post(url, headers=headers, json=email_msg)

        if response.status_code == 202:
            logging.info("\033[32mE-mail enviado com sucesso!\033[0m")
            return True, "E-mail enviado com sucesso"
        elif response.status_code == 401:
            logging.error("Erro de autenticação. Verifique o token.")
            return False, "Erro de autenticação. Verifique o token."
        else:
            logging.error(f"Erro ao enviar e-mail: {response.status_code}, {response.text}")
            return False, f"Erro ao enviar e-mail: {response.status_code}, {response.text}"

    except requests.exceptions.RequestException as e:
        logging.exception("Erro de requisição ao enviar e-mail")
        return False, f"Erro de requisição: {str(e)}"
    except FileNotFoundError as e:
        logging.exception("Erro de arquivo não encontrado")
        return False, f"Erro de arquivo: {str(e)}"
    except Exception as e:
        logging.exception("Erro inesperado ao enviar o e-mail")
        return False, f"Erro inesperado: {str(e)}"
    finally:
        logging.info("\033[32mFunção send_email finalizada.\033[0m")


def encode_file(file_path):
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    return encoded
