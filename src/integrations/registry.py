"""Registry for all external API integrations"""
from typing import Dict, Type
from src.integrations.base import BaseAPIIntegration
import logging

logger = logging.getLogger(__name__)

class IntegrationRegistry:
    """Central registry for all API integrations"""
    
    def __init__(self):
        self._integrations: Dict[str, BaseAPIIntegration] = {}
        self._integration_classes: Dict[str, Type[BaseAPIIntegration]] = {}
    
    def register(self, name: str, integration_class: Type[BaseAPIIntegration]):
        """Register a new integration class"""
        self._integration_classes[name] = integration_class
    
    async def initialize_all(self):
        """Initialize all registered integrations"""
        for name, integration_class in self._integration_classes.items():
            try:
                integration = integration_class()
                if await integration.validate_connection():
                    self._integrations[name] = integration
                    logger.info(f"Initialized {name} integration")
                else:
                    logger.warning(f"Failed to validate {name} integration")
            except Exception as e:
                logger.error(f"Failed to initialize {name}: {e}")
    
    def get(self, name: str) -> BaseAPIIntegration:
        """Get integration by name"""
        if name not in self._integrations:
            raise ValueError(f"Integration {name} not found or not initialized")
        return self._integrations[name]
    
    async def close_all(self):
        """Close all integrations"""
        for integration in self._integrations.values():
            await integration.close()

# Global registry instance
integration_registry = IntegrationRegistry()
