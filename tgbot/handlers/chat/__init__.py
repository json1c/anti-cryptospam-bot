from aiogram import Router


def get_chat_router():
    from . import message
    
    router = Router()
    router.include_router(message.router)
    
    return router
