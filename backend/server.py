import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any
import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
import random
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Temporary Email Service",
    description="Сервис для создания одноразовых email адресов",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class EmailAddress(BaseModel):
    id: str
    email: str
    domain: str
    password: str
    created_at: datetime
    token: Optional[str] = None

class EmailMessage(BaseModel):
    id: str
    from_address: str
    to_address: str
    subject: str
    body: str
    html_body: Optional[str] = None
    received_at: datetime
    attachments: List[Dict[str, Any]] = []

class CreateEmailRequest(BaseModel):
    custom_name: Optional[str] = None

class EmailInboxResponse(BaseModel):
    inbox: EmailAddress
    messages: List[EmailMessage] = []
    message_count: int = 0

# Mail.tm API integration
class MailTmAdapter:
    def __init__(self, base_url: str = "https://api.mail.tm"):
        self.base_url = base_url
        self.sessions = {}
        
    async def _get_session(self):
        session = aiohttp.ClientSession()
        return session
    
    async def _make_request(self, method: str, endpoint: str, token: str = None, **kwargs):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}{endpoint}"
            
            headers = kwargs.get('headers', {})
            if token:
                headers['Authorization'] = f'Bearer {token}'
            kwargs['headers'] = headers
            
            try:
                async with session.request(method, url, **kwargs) as response:
                    if response.status in [200, 201]:
                        return await response.json()
                    elif response.status == 404:
                        return None
                    else:
                        error_text = await response.text()
                        logger.error(f"Mail.tm request failed: {response.status} - {error_text}")
                        raise HTTPException(status_code=response.status, detail=error_text)
            except aiohttp.ClientError as e:
                logger.error(f"Mail.tm request failed: {e}")
                raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    
    async def get_domains(self) -> List[str]:
        try:
            response = await self._make_request('GET', '/domains')
            if response and 'hydra:member' in response:
                domains = [domain['domain'] for domain in response['hydra:member']]
                return domains if domains else ['1secmail.com']
            return ['1secmail.com']
        except Exception as e:
            logger.error(f"Failed to get domains: {e}")
            return ['1secmail.com']
    
    async def create_inbox(self, name: Optional[str] = None) -> EmailAddress:
        try:
            domains = await self.get_domains()
            domain = domains[0]
            
            if not name:
                name = f"user{int(datetime.now().timestamp())}{random.randint(100, 999)}"
            else:
                # Add timestamp to custom name to ensure uniqueness
                name = f"{name}{int(datetime.now().timestamp())}{random.randint(10, 99)}"
            
            email_address = f"{name}@{domain}"
            password = f"password{random.randint(10000, 99999)}"
            
            # Create account
            account_data = {
                "address": email_address,
                "password": password
            }
            
            account = await self._make_request('POST', '/accounts', json=account_data)
            if not account:
                raise HTTPException(status_code=500, detail="Failed to create account")
            
            # Login to get token
            token_response = await self._make_request('POST', '/token', json=account_data)
            token = None
            if token_response and 'token' in token_response:
                token = token_response['token']
            
            return EmailAddress(
                id=account['id'],
                email=email_address,
                domain=domain,
                password=password,
                created_at=datetime.now(),
                token=token
            )
        except Exception as e:
            logger.error(f"Mail.tm inbox creation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to create inbox: {str(e)}")
    
    async def get_messages(self, token: str) -> List[EmailMessage]:
        try:
            response = await self._make_request('GET', '/messages', token=token)
            if not response or 'hydra:member' not in response:
                return []
            
            messages = []
            for msg_data in response['hydra:member']:
                # Get full message content
                msg_id = msg_data['id']
                full_message = await self._make_request('GET', f'/messages/{msg_id}', token=token)
                
                if full_message:
                    # Handle html_body properly - it can be a list or string
                    html_body = full_message.get('html', [])
                    if isinstance(html_body, list):
                        html_body = ' '.join(html_body) if html_body else None
                    elif not html_body:
                        html_body = None
                    
                    message = EmailMessage(
                        id=full_message['id'],
                        from_address=full_message.get('from', {}).get('address', ''),
                        to_address=full_message.get('to', [{}])[0].get('address', ''),
                        subject=full_message.get('subject', ''),
                        body=full_message.get('text', ''),
                        html_body=html_body,
                        received_at=datetime.fromisoformat(
                            full_message.get('createdAt', datetime.now().isoformat()).replace('Z', '+00:00')
                        )
                    )
                    messages.append(message)
            
            return messages
        except Exception as e:
            logger.error(f"Mail.tm message retrieval failed: {e}")
            return []

# Global service instance
mail_service = MailTmAdapter()

# API Routes
@app.post("/api/inbox/create", response_model=EmailInboxResponse)
async def create_inbox(request: CreateEmailRequest):
    """
    Создать новый временный email адрес
    """
    try:
        logger.info(f"Creating inbox with custom name: {request.custom_name}")
        inbox = await mail_service.create_inbox(name=request.custom_name)
        
        logger.info(f"Successfully created inbox: {inbox.email}")
        return EmailInboxResponse(inbox=inbox, messages=[], message_count=0)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating inbox: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/inbox/{inbox_id}/messages", response_model=List[EmailMessage])
async def get_inbox_messages(inbox_id: str, token: str):
    """
    Получить все сообщения из временного email адреса
    """
    try:
        logger.info(f"Retrieving messages for inbox {inbox_id}")
        messages = await mail_service.get_messages(token)
        
        logger.info(f"Retrieved {len(messages)} messages")
        return messages
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving messages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/domains", response_model=List[str])
async def get_available_domains():
    """Получить список доступных доменов"""
    try:
        domains = await mail_service.get_domains()
        return domains
    except Exception as e:
        logger.error(f"Error getting domains: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)