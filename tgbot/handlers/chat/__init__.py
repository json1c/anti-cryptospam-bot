from aiogram import Router


def get_chat_router():
    from . import join_tracker, message
    
    router = Router()
    router.include_router(message.router)
    router.include_router(join_tracker.router)
    
    return router
