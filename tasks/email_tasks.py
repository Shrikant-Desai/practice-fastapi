import smtplib
from email.message import EmailMessage
from core.config import get_settings
from tasks.celery_app import celery_app

settings = get_settings()

@celery_app.task(
    bind=True,
    max_retries=3,  # retry up to 3 times on failure
    default_retry_delay=60,  # wait 60 seconds between retries
)
def send_welcome_email(self, user_email: str, username: str) -> dict:
    try:
        msg = EmailMessage()
        msg["Subject"] = "Welcome to Learning Backend! 🎉"
        msg["From"] = settings.smtp_from_email
        msg["To"] = user_email
        
        # Simple, modern responsive HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background-color: #f3f4f6;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #4F46E5; /* Indigo 600 */
                    color: #ffffff;
                    padding: 40px 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                }}
                .content {{
                    padding: 40px 30px;
                    color: #374151; /* Gray 700 */
                    line-height: 1.6;
                    font-size: 16px;
                }}
                .content p {{
                    margin: 0 0 20px 0;
                }}
                .btn-container {{
                    text-align: center;
                    margin-top: 30px;
                }}
                .btn {{
                    display: inline-block;
                    padding: 14px 28px;
                    background-color: #4F46E5;
                    color: #ffffff !important;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 16px;
                    transition: background-color 0.2s;
                }}
                .btn:hover {{
                    background-color: #4338CA; /* Indigo 700 */
                }}
                .footer {{
                    background-color: #f8fafc; /* Slate 50 */
                    padding: 24px 30px;
                    text-align: center;
                    font-size: 13px;
                    color: #64748b; /* Slate 500 */
                    border-top: 1px solid #e2e8f0;
                }}
                .footer p {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome Aboard, {username}! 🚀</h1>
                </div>
                <div class="content">
                    <p>Hi <strong>{username}</strong>,</p>
                    <p>We're absolutely thrilled to have you join <strong>Learning Backend</strong>! Your account has been successfully created and you're all set to go.</p>
                    <p>Dive right in to explore all the amazing features, databases, and microservices we're building together.</p>
                    <div class="btn-container">
                        <a href="https://yourwebsite.com/login" class="btn">Login to Your Account</a>
                    </div>
                </div>
                <div class="footer">
                    <p>&copy; 2026 Learning Backend. All rights reserved.</p>
                    <p>If you didn't create this account, you can safely ignore this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        plain_text = (
            f"Hi {username},\n\n"
            f"Welcome to Learning Backend! We're thrilled to have you here.\n\n"
            f"Login to your account: https://yourwebsite.com/login\n\n"
            f"If you didn't create this account, you can safely ignore this email."
        )
        msg.set_content(plain_text)
        
        # Attach the HTML version
        msg.add_alternative(html_content, subtype='html')

        # Logic: If SMTP credentials are set, actually send it. Otherwise, print for debugging.
        if settings.smtp_username and settings.smtp_password:
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)
            print(f"[Celery] Welcome email successfully sent via SMTP to {user_email}")
        else:
            print(f"[Celery] MOCK EMAIL: Pretending to send welcome email to {user_email}")
            print(f"Content length: {len(html_content)} bytes")
            # You can uncomment this line for full output debugging in terminal:
            # print(html_content)
            
        return {"status": "sent", "to": user_email}
        
    except Exception as exc:
        print(f"[Celery] Failed to send email to {user_email}. Retrying... Error: {str(exc)}")
        # Raise retry passing the exception to exponentially backoff according to Celery settings
        raise self.retry(exc=exc)
