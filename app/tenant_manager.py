"""
Gerenciador de tenants para o sistema multi-tenant.
Cada tenant possui suas próprias phrases, labels e idioma.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TenantConfig:
    """Configuração de um tenant"""
    tenant_id: str
    language: str = "portuguese"
    phrases: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Valida que phrases e labels tenham o mesmo tamanho"""
        if len(self.phrases) != len(self.labels):
            raise ValueError(
                f"O número de phrases ({len(self.phrases)}) deve ser igual ao número de labels ({len(self.labels)})"
            )


class TenantManager:
    """Gerenciador de tenants em memória"""
    
    def __init__(self):
        self._tenants: Dict[str, TenantConfig] = {}
        self._initialize_default_tenant()
    
    def _initialize_default_tenant(self):
        """Inicializa um tenant padrão com os dados originais"""
        default_phrases = [
            "Qual é o valor do produto X?",
            "Quanto custa o plano mensal?",
            "Como funciona o pagamento?",
            "Qual o prazo de entrega?",
            "Vocês aceitam cartão de crédito?",
            "Estou com problemas para realizar o pagamento",
            "Não consigo finalizar a compra",
            "O site está com erro",
            "O pagamento foi recusado",
            "Meu pedido não foi processado",
            "Gostaria de um cupom de desconto",
        ]
        
        default_labels = [
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "problema", "problema", "problema", "problema", "problema",
            "solicitação",
        ]
        
        default_tenant = TenantConfig(
            tenant_id="default",
            language="portuguese",
            phrases=default_phrases,
            labels=default_labels
        )
        self._tenants["default"] = default_tenant
    
    def create_tenant(
        self,
        tenant_id: str,
        language: str = "portuguese",
        phrases: Optional[List[str]] = None,
        labels: Optional[List[str]] = None
    ) -> TenantConfig:
        """Cria um novo tenant"""
        if tenant_id in self._tenants:
            raise ValueError(f"Tenant '{tenant_id}' já existe")
        
        phrases = phrases or []
        labels = labels or []
        
        tenant = TenantConfig(
            tenant_id=tenant_id,
            language=language,
            phrases=phrases,
            labels=labels
        )
        self._tenants[tenant_id] = tenant
        return tenant
    
    def get_tenant(self, tenant_id: str) -> Optional[TenantConfig]:
        """Obtém um tenant pelo ID"""
        return self._tenants.get(tenant_id)
    
    def update_tenant(
        self,
        tenant_id: str,
        language: Optional[str] = None,
        phrases: Optional[List[str]] = None,
        labels: Optional[List[str]] = None
    ) -> TenantConfig:
        """Atualiza um tenant existente"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            raise ValueError(f"Tenant '{tenant_id}' não encontrado")
        
        if language is not None:
            tenant.language = language
        if phrases is not None:
            tenant.phrases = phrases
        if labels is not None:
            tenant.labels = labels
        
        tenant.updated_at = datetime.now()
        
        # Valida novamente após atualização
        if len(tenant.phrases) != len(tenant.labels):
            raise ValueError(
                f"O número de phrases ({len(tenant.phrases)}) deve ser igual ao número de labels ({len(tenant.labels)})"
            )
        
        return tenant
    
    def delete_tenant(self, tenant_id: str) -> bool:
        """Remove um tenant"""
        if tenant_id == "default":
            raise ValueError("Não é possível deletar o tenant padrão")
        
        if tenant_id in self._tenants:
            del self._tenants[tenant_id]
            return True
        return False
    
    def list_tenants(self) -> List[str]:
        """Lista todos os IDs de tenants"""
        return list(self._tenants.keys())
    
    def tenant_exists(self, tenant_id: str) -> bool:
        """Verifica se um tenant existe"""
        return tenant_id in self._tenants


# Instância global do gerenciador de tenants
tenant_manager = TenantManager()

