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
            # PERGUNTA - Perguntas sobre produtos, serviços, preços
            "Qual é o valor do produto X?",
            "Quanto custa o plano mensal?",
            "Como funciona o pagamento?",
            "Qual o prazo de entrega?",
            "Vocês aceitam cartão de crédito?",
            "Qual a diferença entre os planos?",
            "O produto tem garantia?",
            "Quais são as formas de pagamento?",
            "Tem desconto para pagamento à vista?",
            "Qual o valor do frete?",
            "O produto está disponível em estoque?",
            "Vocês fazem entrega em todo o Brasil?",

            # PROBLEMA - Problemas técnicos, erros, bugs
            "Estou com problemas para realizar o pagamento",
            "Não consigo finalizar a compra",
            "O site está com erro",
            "O pagamento foi recusado",
            "Meu pedido não foi processado",
            "A página não está carregando",
            "Não consigo fazer login na minha conta",
            "O sistema está muito lento",
            "Recebi um erro ao tentar acessar",
            "A aplicação está travando",
            "Não consigo adicionar produtos ao carrinho",
            "O checkout não está funcionando",

            # SOLICITAÇÃO - Pedidos, requisições
            "Gostaria de um cupom de desconto",
            "Quero cancelar minha assinatura",
            "Preciso alterar meu endereço de entrega",
            "Gostaria de trocar o produto",
            "Quero atualizar meus dados cadastrais",
            "Preciso de um comprovante de pagamento",
            "Gostaria de solicitar uma nota fiscal",
            "Quero adicionar mais produtos ao pedido",
            "Preciso de ajuda para configurar minha conta",
            "Gostaria de receber informações sobre novos produtos",

            # RECLAMAÇÃO - Reclamações sobre produtos ou serviços
            "O produto chegou com defeito",
            "A entrega está atrasada",
            "Não recebi o que foi prometido",
            "O atendimento está muito ruim",
            "Estou insatisfeito com o serviço",
            "O produto não corresponde à descrição",
            "A qualidade está abaixo do esperado",
            "Tive uma experiência muito ruim",
            "O suporte não está resolvendo meu problema",
            "Estou decepcionado com a compra",

            # ELOGIO - Feedback positivo
            "Adorei o produto, muito bom!",
            "O atendimento foi excelente",
            "Parabéns pelo serviço de qualidade",
            "Superou minhas expectativas",
            "Recomendarei para meus amigos",
            "Muito satisfeito com a compra",
            "Ótimo produto e entrega rápida",
            "Excelente experiência de compra",
            "O suporte foi muito atencioso",
            "Produto de alta qualidade",

            # CANCELAMENTO - Pedidos de cancelamento
            "Quero cancelar meu pedido",
            "Preciso cancelar minha compra",
            "Como faço para cancelar?",
            "Gostaria de cancelar a assinatura",
            "Quero desistir da compra",
            "Preciso cancelar o serviço",
            "Como cancelo minha conta?",
            "Quero cancelar tudo",

            # REEMBOLSO - Solicitações de reembolso
            "Quero o reembolso do meu dinheiro",
            "Preciso receber meu dinheiro de volta",
            "Como solicito o estorno?",
            "Quero reembolso do produto",
            "Preciso do reembolso urgente",
            "Como faço para receber o estorno?",
            "Quero meu dinheiro de volta",
            "Preciso cancelar e receber reembolso",

            # DÚVIDA_TÉCNICA - Questões técnicas específicas
            "Como instalo o produto?",
            "Preciso de ajuda com a configuração",
            "O produto é compatível com Windows?",
            "Qual a versão mínima do sistema?",
            "Como atualizo o software?",
            "Preciso de suporte técnico",
            "Como faço backup dos meus dados?",
            "Qual a diferença entre as versões?",
            "Preciso de ajuda para integrar a API",
            "Como configuro as notificações?",

            # INFORMAÇÃO - Pedidos de informação
            "Quais são os horários de atendimento?",
            "Vocês têm loja física?",
            "Qual o endereço da empresa?",
            "Preciso do CNPJ para nota fiscal",
            "Quais documentos preciso enviar?",
            "Como entro em contato com vocês?",
            "Vocês têm WhatsApp?",
            "Qual o email de contato?",
            "Preciso de mais informações sobre o produto",
            "Quais são os termos de uso?",

            # SUPORTE - Pedidos de suporte técnico
            "Preciso de ajuda urgente",
            "Alguém pode me ajudar?",
            "Estou com dificuldades",
            "Não consigo resolver sozinho",
            "Preciso falar com um atendente",
            "Quero falar com o suporte",
            "Preciso de assistência técnica",
            "Alguém pode me orientar?",
        ]

        default_labels = [
            # PERGUNTA (12 exemplos)
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta",

            # PROBLEMA (12 exemplos)
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema",

            # SOLICITAÇÃO (10 exemplos)
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",

            # RECLAMAÇÃO (10 exemplos)
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",

            # ELOGIO (10 exemplos)
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",

            # CANCELAMENTO (8 exemplos)
            "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento",

            # REEMBOLSO (8 exemplos)
            "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso",

            # DÚVIDA_TÉCNICA (10 exemplos)
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",

            # INFORMAÇÃO (10 exemplos)
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",

            # SUPORTE (8 exemplos)
            "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte",
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
    
    def list_tenants(self) -> List[TenantConfig]:
        """Lista todos os tenants cadastrados"""
        return list(self._tenants.values())
    
    def tenant_exists(self, tenant_id: str) -> bool:
        """Verifica se um tenant existe"""
        return tenant_id in self._tenants


# Instância global do gerenciador de tenants
tenant_manager = TenantManager()

