from aiogram import Router


def get_handlers_router():
    from . import chat
    
    router = Router()
    
    chat_router = chat.get_chat_router()
    
    router.include_router(chat_router)
    
    return router
