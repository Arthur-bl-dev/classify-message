from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from .model import model_manager
from .tenant_manager import tenant_manager

app = FastAPI(
    title="Classify Message - Multi-Tenant",
    description="API para classificação de mensagens com suporte multi-tenant. Cada tenant possui suas próprias phrases, labels e idioma."
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (em produção, especifique os domínios)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)


# ========== Modelos de Requisição/Resposta ==========

class MessageRequest(BaseModel):
    message: str = Field(..., description="Mensagem a ser classificada")
    tenant_id: str = Field(default="default", description="ID do tenant")


class ClassificationResponse(BaseModel):
    classification: str
    probability: float
    tenant_id: str


class TenantCreateRequest(BaseModel):
    tenant_id: str = Field(..., description="ID único do tenant")
    language: str = Field(default="portuguese", description="Idioma do tenant (portuguese, english, spanish, etc.)")
    phrases: List[str] = Field(..., description="Lista de phrases de treinamento")
    labels: List[str] = Field(..., description="Lista de labels correspondentes às phrases")


class TenantUpdateRequest(BaseModel):
    language: Optional[str] = Field(None, description="Idioma do tenant")
    phrases: Optional[List[str]] = Field(None, description="Lista de phrases de treinamento")
    labels: Optional[List[str]] = Field(None, description="Lista de labels correspondentes às phrases")


class TenantResponse(BaseModel):
    tenant_id: str
    language: str
    phrases: List[str]
    labels: List[str]
    created_at: str
    updated_at: str


# ========== Endpoints de Classificação ==========

@app.post("/classify", response_model=ClassificationResponse)
def classify(data: MessageRequest):
    """
    Classifica uma mensagem usando o modelo do tenant especificado.
    """
    tenant = tenant_manager.get_tenant(data.tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant '{data.tenant_id}' não encontrado"
        )
    
    if not tenant.phrases or not tenant.labels:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tenant '{data.tenant_id}' não possui phrases e labels configuradas"
        )
    
    try:
        classification, probability = model_manager.classify_message(
            tenant_id=tenant.tenant_id,
            language=tenant.language,
            phrases=tenant.phrases,
            labels=tenant.labels,
            message=data.message
        )
        
        return {
            "classification": classification,
            "probability": round(probability, 2),
            "tenant_id": tenant.tenant_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao classificar mensagem: {str(e)}"
        )


# ========== Endpoints de Gerenciamento de Tenants ==========

@app.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(data: TenantCreateRequest):
    """
    Cria um novo tenant com suas phrases, labels e idioma.
    """
    try:
        tenant = tenant_manager.create_tenant(
            tenant_id=data.tenant_id,
            language=data.language,
            phrases=data.phrases,
            labels=data.labels
        )
        
        # Treina o modelo para o novo tenant
        model_manager.get_or_create_model(
            tenant_id=tenant.tenant_id,
            language=tenant.language,
            phrases=tenant.phrases,
            labels=tenant.labels
        )
        
        return {
            "tenant_id": tenant.tenant_id,
            "language": tenant.language,
            "phrases": tenant.phrases,
            "labels": tenant.labels,
            "created_at": tenant.created_at.isoformat(),
            "updated_at": tenant.updated_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/tenants", response_model=List[str])
def list_tenants():
    """
    Lista todos os IDs de tenants cadastrados.
    """
    return tenant_manager.list_tenants()


@app.get("/tenants/{tenant_id}", response_model=TenantResponse)
def get_tenant(tenant_id: str):
    """
    Obtém informações de um tenant específico.
    """
    tenant = tenant_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant '{tenant_id}' não encontrado"
        )
    
    return {
        "tenant_id": tenant.tenant_id,
        "language": tenant.language,
        "phrases": tenant.phrases,
        "labels": tenant.labels,
        "created_at": tenant.created_at.isoformat(),
        "updated_at": tenant.updated_at.isoformat()
    }


@app.put("/tenants/{tenant_id}", response_model=TenantResponse)
def update_tenant(tenant_id: str, data: TenantUpdateRequest):
    """
    Atualiza as configurações de um tenant existente.
    """
    try:
        tenant = tenant_manager.update_tenant(
            tenant_id=tenant_id,
            language=data.language,
            phrases=data.phrases,
            labels=data.labels
        )
        
        # Retreina o modelo se necessário
        if data.phrases is not None or data.labels is not None or data.language is not None:
            model_manager.get_or_create_model(
                tenant_id=tenant.tenant_id,
                language=tenant.language,
                phrases=tenant.phrases,
                labels=tenant.labels
            )
        
        return {
            "tenant_id": tenant.tenant_id,
            "language": tenant.language,
            "phrases": tenant.phrases,
            "labels": tenant.labels,
            "created_at": tenant.created_at.isoformat(),
            "updated_at": tenant.updated_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.delete("/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(tenant_id: str):
    """
    Remove um tenant (não é possível deletar o tenant 'default').
    """
    try:
        deleted = tenant_manager.delete_tenant(tenant_id)
        if deleted:
            # Remove o modelo do tenant
            model_manager.remove_model(tenant_id)
            return None
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tenant '{tenant_id}' não encontrado"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ========== Endpoint de Health Check ==========

@app.get("/health")
def health_check():
    """
    Endpoint de verificação de saúde da API.
    """
    return {
        "status": "healthy",
        "tenants_count": len(tenant_manager.list_tenants())
    }
