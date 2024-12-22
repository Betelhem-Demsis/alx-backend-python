from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet


router = DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversation')


nested_router = NestedDefaultRouter(router, 'conversations', lookup='conversation')
nested_router.register('messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
