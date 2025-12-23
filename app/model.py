"""
Modelo de classificação multi-tenant.
Cada tenant possui seu próprio modelo treinado com suas phrases, labels e idioma.
"""
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from typing import Dict, Tuple, Optional, List
import logging

# Garante que o corpus de stopwords do NLTK esteja disponível
nltk.download('stopwords', quiet=True)

logger = logging.getLogger(__name__)

class TenantModel:
    """Modelo de classificação para um tenant específico"""
    
    def __init__(self, tenant_id: str, language: str, phrases: List[str], labels: List[str]):
        self.tenant_id = tenant_id
        self.language = language
        self.phrases = phrases
        self.labels = labels
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.model: Optional[MultinomialNB] = None
        self._trained = False
        
        if phrases and labels:
            self._train()
    
    def _get_stopwords(self, language: str) -> List[str]:
        """Obtém as stopwords para o idioma especificado"""
        try:
            # Suporta vários idiomas comuns
            language_map = {
                "portuguese": "portuguese",
                "português": "portuguese",
                "english": "english",
                "inglês": "english",
                "espanol": "spanish",
                "espanhol": "spanish",
                "french": "french",
                "francês": "french",
            }
            
            nltk_lang = language_map.get(language.lower(), language.lower())
            return stopwords.words(nltk_lang)
        except Exception as e:
            logger.warning(f"Idioma '{language}' não suportado, usando lista vazia de stopwords. Erro: {e}")
            return []
    
    def _train(self):
        """Treina o modelo com as phrases e labels do tenant"""
        if not self.phrases or not self.labels:
            raise ValueError("Phrases e labels são necessários para treinar o modelo")
        
        if len(self.phrases) != len(self.labels):
            raise ValueError(
                f"O número de phrases ({len(self.phrases)}) deve ser igual ao número de labels ({len(self.labels)})"
            )
        
        # Obtém stopwords para o idioma do tenant
        stop_words = self._get_stopwords(self.language)
        
        # Inicializa o TfidfVectorizer com as stopwords do idioma
        self.vectorizer = TfidfVectorizer(
            stop_words=stop_words,
            strip_accents='unicode',
            lowercase=True
        )
        
        # Transforma as phrases em vetores
        X = self.vectorizer.fit_transform(self.phrases)
        
        # Cria e treina o modelo
        self.model = MultinomialNB()
        self.model.fit(X, self.labels)
        self._trained = True
        
        logger.info(f"Modelo treinado para tenant '{self.tenant_id}' com {len(self.phrases)} exemplos")
    
    def classify(self, message: str) -> Tuple[str, float]:
        """
        Classifica uma mensagem e retorna a categoria e probabilidade
        
        Args:
            message: Mensagem a ser classificada
            
        Returns:
            Tupla (classificação, probabilidade)
        """
        if not self._trained:
            raise ValueError(f"Modelo do tenant '{self.tenant_id}' não foi treinado")
        
        if not self.vectorizer or not self.model:
            raise ValueError(f"Modelo do tenant '{self.tenant_id}' não está inicializado")
        
        # Transforma a mensagem
        msg_vector = self.vectorizer.transform([message])
        
        # Obtém as probabilidades
        probs = self.model.predict_proba(msg_vector)[0]
        
        # Obtém as classes
        classes = self.model.classes_
        result = dict(zip(classes, probs))
        
        # Retorna a classificação com maior probabilidade
        classification = max(result, key=result.get)
        probability = result[classification]
        
        return classification, probability
    
    def retrain(self, phrases: List[str], labels: List[str]):
        """Retreina o modelo com novas phrases e labels"""
        self.phrases = phrases
        self.labels = labels
        self._train()

class ModelManager:
    """Gerenciador de modelos multi-tenant"""
    
    def __init__(self):
        self._models: Dict[str, TenantModel] = {}
    
    def get_or_create_model(
        self,
        tenant_id: str,
        language: str,
        phrases: List[str],
        labels: List[str]
    ) -> TenantModel:
        """Obtém um modelo existente ou cria um novo"""
        if tenant_id in self._models:
            model = self._models[tenant_id]
            # Verifica se precisa retreinar
            if (model.language != language or 
                model.phrases != phrases or 
                model.labels != labels):
                model.language = language
                model.retrain(phrases, labels)
            return model
        
        # Cria novo modelo
        model = TenantModel(tenant_id, language, phrases, labels)
        self._models[tenant_id] = model
        return model
    
    def get_model(self, tenant_id: str) -> Optional[TenantModel]:
        """Obtém um modelo existente"""
        return self._models.get(tenant_id)
    
    def remove_model(self, tenant_id: str):
        """Remove um modelo"""
        if tenant_id in self._models:
            del self._models[tenant_id]
    
    def classify_message(
        self,
        tenant_id: str,
        language: str,
        phrases: List[str],
        labels: List[str],
        message: str
    ) -> Tuple[str, float]:
        """
        Classifica uma mensagem para um tenant específico
        
        Args:
            tenant_id: ID do tenant
            language: Idioma do tenant
            phrases: Lista de phrases de treinamento
            labels: Lista de labels de treinamento
            message: Mensagem a ser classificada
            
        Returns:
            Tupla (classificação, probabilidade)
        """
        model = self.get_or_create_model(tenant_id, language, phrases, labels)
        return model.classify(message)

# Instância global do gerenciador de modelos
model_manager = ModelManager()

# Função de compatibilidade com código antigo (usa tenant "default")
def classify_message(message: str) -> Tuple[str, float]:
    """
    Função de compatibilidade que classifica usando o tenant padrão.
    Para novos códigos, use model_manager.classify_message diretamente.
    """
    from .tenant_manager import tenant_manager
    
    tenant = tenant_manager.get_tenant("default")
    if not tenant:
        raise ValueError("Tenant 'default' não encontrado")
    
    return model_manager.classify_message(
        tenant_id="default",
        language=tenant.language,
        phrases=tenant.phrases,
        labels=tenant.labels,
        message=message
    )
