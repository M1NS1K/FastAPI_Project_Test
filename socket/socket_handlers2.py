from .app import socket_manager as sm

@sm.on('leave')
async def handle_leave(sid, *args, **kwargs):
    await sm.emit('lobby', 'User left')