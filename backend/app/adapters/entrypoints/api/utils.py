import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import emails  # type: ignore
from fastapi import HTTPException, Request, UploadFile, status
from fastapi.openapi.models import OAuthFlowPassword, OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jinja2 import Template

from app.core.config import settings


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        auto_error: bool = True,
    ) -> None:
        super().__init__(
            flows=OAuthFlows(
                password=OAuthFlowPassword(
                    tokenUrl=tokenUrl,
                    scopes=scopes or {},
                ),
            ),
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> str | None:
        # changed to accept access token from httpOnly Cookie
        authorization: str | None = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if authorization is None or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent.parent
        / "static"
        / "email-templates"
        / "build"
        / template_name
    ).read_text()

    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def generate_new_auth_code_email(email_to: str, auth_code: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - 인증번호를 발송해 드립니다."
    html_content = render_email_template(
        template_name="auth_code.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "auth_code": auth_code,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def save_file_to_static(*, file: UploadFile, category: str) -> str:
    asset_file_path = "/".join(
        [
            "assets",
            category,
            str(file.filename),
        ]
    )

    real_file_path = Path(__file__).parent.parent / "static" / asset_file_path
    logging.error(f"saving file to {real_file_path} ... ")
    try:
        with real_file_path.open("wb") as buffer:
            buffer.write(file.file.read())

        return str(asset_file_path)
    except Exception as e:
        logging.error(f"Error saving file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving file",
        )
