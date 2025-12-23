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
            # PERGUNTA - Perguntas sobre produtos, serviços, preços (50 exemplos)
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
            "Qual o preço do produto?",
            "Quanto custa a assinatura anual?",
            "Há algum desconto disponível?",
            "Qual a forma de pagamento mais barata?",
            "O produto tem parcelamento?",
            "Quantas vezes posso parcelar?",
            "Qual o juro do parcelamento?",
            "Vocês aceitam boleto?",
            "Qual o prazo para pagamento via boleto?",
            "O produto tem estoque?",
            "Quando o produto volta ao estoque?",
            "Qual o tempo de entrega para minha cidade?",
            "Vocês fazem entrega expressa?",
            "Qual o custo do frete expresso?",
            "O produto tem garantia de fábrica?",
            "Qual o período de garantia?",
            "Como funciona a troca do produto?",
            "Posso testar antes de comprar?",
            "O produto tem versão de teste?",
            "Qual a diferença entre os modelos?",
            "Qual produto é melhor para mim?",
            "O produto funciona offline?",
            "Preciso de internet para usar?",
            "Qual a capacidade de armazenamento?",
            "O produto suporta quantos usuários?",
            "Há limite de uso?",
            "Qual o custo adicional por usuário?",
            "O plano inclui suporte?",
            "Qual o horário de atendimento?",
            "Vocês têm plantão 24 horas?",
            "O produto é compatível com meu sistema?",
            "Preciso de algum software adicional?",
            "Qual a política de reembolso?",
            "Posso cancelar a qualquer momento?",
            "Há multa por cancelamento?",
            "O produto tem atualizações gratuitas?",
            "Com que frequência há atualizações?",
            "Qual a duração da licença?",

            # PROBLEMA - Problemas técnicos, erros, bugs (50 exemplos)
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
            "O botão de pagamento não responde",
            "A página fica em branco",
            "Recebo erro 404 ao navegar",
            "O formulário não envia",
            "Não consigo criar minha conta",
            "A senha não está sendo aceita",
            "Esqueci minha senha e não consigo recuperar",
            "O email de confirmação não chegou",
            "Não consigo verificar meu email",
            "O código de verificação não funciona",
            "A sessão expira muito rápido",
            "Sou deslogado constantemente",
            "Não consigo acessar minha área restrita",
            "Os dados não estão salvando",
            "As alterações não são aplicadas",
            "O upload de arquivo falha",
            "Não consigo fazer download",
            "O arquivo corrompeu durante o download",
            "A imagem não carrega",
            "Os vídeos não reproduzem",
            "O áudio não funciona",
            "A busca não retorna resultados",
            "Os filtros não estão funcionando",
            "A ordenação está incorreta",
            "Os produtos não aparecem",
            "O carrinho está vazio mas tinha itens",
            "O preço exibido está errado",
            "O desconto não foi aplicado",
            "O cupom não está sendo aceito",
            "O frete calculado está incorreto",
            "O rastreamento não atualiza",
            "Não recebo notificações",
            "Os emails não chegam",
            "O SMS não é enviado",
            "A integração com pagamento falha",
            "O gateway de pagamento está offline",
            "A API retorna erro",
            "O webhook não está funcionando",

            # SOLICITAÇÃO - Pedidos, requisições (50 exemplos)
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
            "Preciso do link de pagamento",
            "Me envie o link de pagamento",
            "Solicito o link de pagamento",
            "Gostaria de receber um orçamento",
            "Preciso de uma proposta comercial",
            "Quero solicitar uma demonstração",
            "Gostaria de agendar uma reunião",
            "Preciso de um relatório detalhado",
            "Quero solicitar acesso à área premium",
            "Gostaria de aumentar meu plano",
            "Preciso reduzir meu plano",
            "Quero adicionar mais usuários",
            "Gostaria de remover usuários",
            "Preciso de um backup dos meus dados",
            "Quero exportar minhas informações",
            "Gostaria de importar dados de outro sistema",
            "Preciso de integração com outro serviço",
            "Quero solicitar uma customização",
            "Gostaria de personalizar minha conta",
            "Preciso de um treinamento",
            "Quero solicitar material de apoio",
            "Gostaria de receber documentação técnica",
            "Preciso de um certificado de conclusão",
            "Quero solicitar um recibo",
            "Gostaria de receber um boleto",
            "Preciso de segunda via da nota fiscal",
            "Quero alterar a forma de pagamento",
            "Gostaria de adiar o vencimento",
            "Preciso de um desconto especial",
            "Quero solicitar um crédito",
            "Gostaria de transferir minha conta",
            "Preciso de ajuda para migrar dados",
            "Quero solicitar suporte prioritário",
            "Gostaria de participar do programa de beta",
            "Preciso de acesso antecipado a recursos",
            "Quero solicitar uma parceria",
            "Gostaria de me tornar um revendedor",
            "Preciso de credenciais de API",
            "Quero solicitar aumento de limite",

            # RECLAMAÇÃO - Reclamações sobre produtos ou serviços (50 exemplos)
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
            "O produto veio quebrado",
            "Faltam peças na embalagem",
            "O produto não funciona como anunciado",
            "A embalagem estava danificada",
            "Recebi o produto errado",
            "O tamanho não corresponde ao pedido",
            "A cor está diferente do site",
            "O produto é de qualidade inferior",
            "A entrega demorou muito",
            "O entregador não respeitou o horário",
            "Não fui avisado sobre a entrega",
            "A entrega foi feita no lugar errado",
            "O produto não foi entregue",
            "O rastreamento não funciona",
            "Não consigo falar com ninguém",
            "O atendimento é muito demorado",
            "Ninguém responde minhas mensagens",
            "O suporte não tem conhecimento técnico",
            "Fui transferido várias vezes sem solução",
            "O problema não foi resolvido",
            "Estou há dias sem resposta",
            "O sistema está sempre fora do ar",
            "A plataforma é muito instável",
            "Perdi dados importantes",
            "As funcionalidades não funcionam",
            "O serviço é muito caro para o que oferece",
            "Há cobranças indevidas",
            "Fui cobrado duas vezes",
            "O valor cobrado está incorreto",
            "Não recebi o desconto prometido",
            "A fatura está com valores errados",
            "O suporte não é 24 horas como prometido",
            "As atualizações quebraram funcionalidades",
            "O produto não tem as features anunciadas",
            "A documentação está desatualizada",
            "Os tutoriais não ajudam",
            "A interface é confusa",
            "O sistema é difícil de usar",
            "Não há suporte em português adequado",
            "O produto não atende minhas necessidades",

            # ELOGIO - Feedback positivo (50 exemplos)
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
            "O produto chegou antes do prazo",
            "A embalagem estava perfeita",
            "O produto superou todas as expectativas",
            "A qualidade é excepcional",
            "Valeu cada centavo investido",
            "O atendimento foi rápido e eficiente",
            "Resolveram meu problema na hora",
            "O suporte técnico é muito competente",
            "A plataforma é intuitiva e fácil",
            "As funcionalidades são incríveis",
            "O sistema é muito estável",
            "Nunca tive problemas técnicos",
            "A interface é linda e moderna",
            "A experiência do usuário é perfeita",
            "O produto é exatamente como descrito",
            "A entrega foi super rápida",
            "O entregador foi muito educado",
            "Fui bem informado sobre tudo",
            "A comunicação foi clara e objetiva",
            "O processo de compra foi simples",
            "O checkout é muito fácil",
            "Os métodos de pagamento são variados",
            "O preço é justo pelo que oferece",
            "Há muito valor pelo preço pago",
            "As atualizações são frequentes",
            "Sempre adicionam novas funcionalidades",
            "A documentação é completa",
            "Os tutoriais são muito úteis",
            "Aprender a usar foi fácil",
            "O produto resolveu meu problema",
            "Economizei muito tempo",
            "Aumentou minha produtividade",
            "Melhorou meu fluxo de trabalho",
            "A integração foi simples",
            "Funciona perfeitamente com outros sistemas",
            "O suporte responde rápido",
            "Sempre disponíveis para ajudar",
            "Profissionais muito qualificados",
            "A empresa tem valores sólidos",
            "Confio totalmente no produto",

            # CANCELAMENTO - Pedidos de cancelamento (50 exemplos)
            "Quero cancelar meu pedido",
            "Preciso cancelar minha compra",
            "Como faço para cancelar?",
            "Gostaria de cancelar a assinatura",
            "Quero desistir da compra",
            "Preciso cancelar o serviço",
            "Como cancelo minha conta?",
            "Quero cancelar tudo",
            "Preciso cancelar urgentemente",
            "Quero cancelar antes do vencimento",
            "Como cancelo minha assinatura?",
            "Gostaria de cancelar meu plano",
            "Quero encerrar minha conta",
            "Preciso cancelar o pedido que acabei de fazer",
            "Quero cancelar e fazer outro pedido",
            "Como faço para cancelar online?",
            "Preciso cancelar pelo telefone?",
            "Quero cancelar via email",
            "Gostaria de cancelar pelo chat",
            "Preciso cancelar minha conta premium",
            "Quero cancelar o upgrade",
            "Gostaria de voltar ao plano anterior",
            "Preciso cancelar o plano anual",
            "Quero cancelar o plano mensal",
            "Como cancelo sem multa?",
            "Preciso cancelar antes de ser cobrado",
            "Quero cancelar e não renovar",
            "Gostaria de cancelar a renovação automática",
            "Preciso desativar minha conta",
            "Quero suspender minha conta temporariamente",
            "Como cancelo todos os serviços?",
            "Preciso cancelar múltiplas assinaturas",
            "Quero cancelar e deletar meus dados",
            "Gostaria de cancelar e exportar tudo",
            "Preciso cancelar por motivos financeiros",
            "Quero cancelar porque não uso mais",
            "Gostaria de cancelar por insatisfação",
            "Preciso cancelar por mudança de necessidade",
            "Quero cancelar e migrar para outro serviço",
            "Gostaria de cancelar sem justificativa",
            "Preciso cancelar imediatamente",
            "Quero cancelar hoje mesmo",
            "Como cancelo agora?",
            "Preciso de ajuda para cancelar",
            "Quero confirmar o cancelamento",
            "Gostaria de saber se o cancelamento foi processado",
            "Preciso do comprovante de cancelamento",
            "Quero garantir que não serei mais cobrado",
            "Gostaria de cancelar e receber reembolso",
            "Preciso cancelar e estornar o pagamento",

            # REEMBOLSO - Solicitações de reembolso (50 exemplos)
            "Quero o reembolso do meu dinheiro",
            "Preciso receber meu dinheiro de volta",
            "Como solicito o estorno?",
            "Quero reembolso do produto",
            "Preciso do reembolso urgente",
            "Como faço para receber o estorno?",
            "Quero meu dinheiro de volta",
            "Preciso cancelar e receber reembolso",
            "Gostaria de solicitar reembolso",
            "Quero estorno do pagamento",
            "Preciso reembolsar a compra",
            "Como recebo meu dinheiro de volta?",
            "Quero reembolso total",
            "Preciso de reembolso parcial",
            "Gostaria de estornar a transação",
            "Quero reembolso porque o produto veio com defeito",
            "Preciso reembolsar porque não recebi o produto",
            "Quero estorno porque foi cobrado errado",
            "Preciso reembolso porque cancelei",
            "Gostaria de reembolso por insatisfação",
            "Quero meu dinheiro de volta urgente",
            "Preciso do reembolso até amanhã",
            "Como solicito reembolso online?",
            "Quero reembolso pelo cartão de crédito",
            "Preciso estornar no débito",
            "Gostaria de reembolso no PIX",
            "Quero reembolso no boleto",
            "Preciso reembolsar na conta bancária",
            "Como recebo o reembolso?",
            "Quanto tempo demora o reembolso?",
            "Preciso saber o prazo do estorno",
            "Quero acompanhar o reembolso",
            "Preciso do comprovante de reembolso",
            "Gostaria de confirmar o reembolso",
            "Quero garantir que vou receber",
            "Preciso do número do estorno",
            "Quero reembolso completo do valor",
            "Preciso reembolsar as taxas também",
            "Gostaria de reembolso dos juros",
            "Quero estornar o frete pago",
            "Preciso reembolsar o valor total",
            "Quero reembolso imediato",
            "Preciso do dinheiro de volta hoje",
            "Gostaria de reembolso sem burocracia",
            "Quero processo de reembolso simples",
            "Preciso de ajuda para solicitar reembolso",
            "Quero reembolso porque não usei",
            "Preciso estornar compra duplicada",
            "Gostaria de reembolso de assinatura",
            "Quero reembolso proporcional",

            # DÚVIDA_TÉCNICA - Questões técnicas específicas (50 exemplos)
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
            "O produto funciona no Linux?",
            "É compatível com macOS?",
            "Preciso de requisitos específicos?",
            "Qual a versão do Python necessária?",
            "Funciona com Node.js?",
            "Como configuro o banco de dados?",
            "Preciso de servidor próprio?",
            "Funciona na nuvem?",
            "Como faço deploy?",
            "Qual a configuração recomendada?",
            "Preciso de SSL?",
            "Como configuro HTTPS?",
            "Qual porta usar?",
            "Preciso abrir firewall?",
            "Como configuro variáveis de ambiente?",
            "Onde coloco as credenciais?",
            "Como gero chaves de API?",
            "Preciso de token de autenticação?",
            "Como faço autenticação?",
            "Qual protocolo usar?",
            "Preciso configurar webhook?",
            "Como recebo notificações?",
            "Qual formato de dados usar?",
            "Preciso de JSON ou XML?",
            "Como faço integração?",
            "Há SDK disponível?",
            "Qual linguagem de programação usar?",
            "Como faço requisições?",
            "Qual endpoint usar?",
            "Preciso de rate limiting?",
            "Como trato erros?",
            "Qual código de status esperar?",
            "Como faço paginação?",
            "Preciso de cache?",
            "Como otimizo performance?",
            "Qual banco de dados usar?",
            "Preciso de migração?",
            "Como faço rollback?",
            "Preciso de monitoramento?",
            "Como configuro logs?",

            # INFORMAÇÃO - Pedidos de informação (50 exemplos)
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
            "Qual a política de privacidade?",
            "Quais são os termos e condições?",
            "Preciso da política de reembolso",
            "Qual a política de cancelamento?",
            "Quais são as formas de pagamento aceitas?",
            "Vocês têm programa de fidelidade?",
            "Como funciona o programa de pontos?",
            "Há desconto para estudantes?",
            "Vocês fazem parcerias?",
            "Como me torno revendedor?",
            "Preciso de informações comerciais",
            "Quais são os planos disponíveis?",
            "Qual plano é melhor para mim?",
            "Há plano gratuito?",
            "Qual a diferença entre os planos?",
            "Preciso de informações sobre preços",
            "Há desconto para pagamento anual?",
            "Qual o preço do plano empresarial?",
            "Vocês têm teste gratuito?",
            "Qual a duração do trial?",
            "Preciso de informações sobre suporte",
            "O suporte é 24 horas?",
            "Há suporte em português?",
            "Qual o tempo de resposta?",
            "Preciso de informações sobre segurança",
            "Como meus dados são protegidos?",
            "Vocês têm certificação?",
            "Há compliance com LGPD?",
            "Preciso de informações sobre integração",
            "Quais sistemas vocês integram?",
            "Há API disponível?",
            "Preciso de documentação técnica",
            "Onde encontro tutoriais?",
            "Há vídeos explicativos?",
            "Preciso de informações sobre atualizações",
            "Com que frequência atualizam?",
            "Há changelog disponível?",
            "Preciso de roadmap de funcionalidades",
            "Quais features estão planejadas?",
            "Quando será lançada a próxima versão?",

            # SUPORTE - Pedidos de suporte técnico (50 exemplos)
            "Preciso de ajuda urgente",
            "Alguém pode me ajudar?",
            "Estou com dificuldades",
            "Não consigo resolver sozinho",
            "Preciso falar com um atendente",
            "Quero falar com o suporte",
            "Preciso de assistência técnica",
            "Alguém pode me orientar?",
            "Estou perdido e preciso de ajuda",
            "Não entendo como funciona",
            "Preciso de explicação detalhada",
            "Quero um tutorial passo a passo",
            "Preciso de suporte imediato",
            "Estou com problema crítico",
            "Algo não está funcionando",
            "Preciso de ajuda para configurar",
            "Não consigo fazer funcionar",
            "Estou tendo erro constante",
            "Preciso de suporte especializado",
            "Quero falar com técnico",
            "Preciso de ajuda de especialista",
            "Estou bloqueado e não consigo avançar",
            "Preciso de orientação urgente",
            "Não sei o que fazer",
            "Estou confuso sobre o processo",
            "Preciso de clarificação",
            "Quero entender melhor",
            "Preciso de ajuda para começar",
            "Não sei por onde começar",
            "Estou tendo dificuldade inicial",
            "Preciso de onboarding",
            "Quero treinamento básico",
            "Preciso de ajuda avançada",
            "Estou em nível intermediário",
            "Preciso de suporte para integração",
            "Quero ajuda com API",
            "Preciso de suporte para desenvolvimento",
            "Estou com problema de código",
            "Preciso de ajuda para debug",
            "Quero suporte para troubleshooting",
            "Preciso de ajuda para migração",
            "Estou mudando de sistema",
            "Preciso de suporte para backup",
            "Quero ajuda para restaurar dados",
            "Preciso de suporte para segurança",
            "Estou com problema de acesso",
            "Preciso de ajuda para recuperar conta",
            "Quero suporte para performance",
            "Estou com sistema lento",
        ]

        default_labels = [
            # PERGUNTA (50 exemplos)
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",
            "pergunta", "pergunta", "pergunta", "pergunta", "pergunta",

            # PROBLEMA (50 exemplos)
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",
            "problema", "problema", "problema", "problema", "problema",

            # SOLICITAÇÃO (50 exemplos)
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",
            "solicitação", "solicitação", "solicitação", "solicitação", "solicitação",

            # RECLAMAÇÃO (50 exemplos)
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",
            "reclamação", "reclamação", "reclamação", "reclamação", "reclamação",

            # ELOGIO (50 exemplos)
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",
            "elogio", "elogio", "elogio", "elogio", "elogio",

            # CANCELAMENTO (50 exemplos)
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",
            "cancelamento", "cancelamento", "cancelamento", "cancelamento", "cancelamento",

            # REEMBOLSO (50 exemplos)
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",
            "reembolso", "reembolso", "reembolso", "reembolso", "reembolso",

            # DÚVIDA_TÉCNICA (50 exemplos)
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",
            "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica", "dúvida_técnica",

            # INFORMAÇÃO (50 exemplos)
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",
            "informação", "informação", "informação", "informação", "informação",

            # SUPORTE (50 exemplos)
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
            "suporte", "suporte", "suporte", "suporte", "suporte",
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

