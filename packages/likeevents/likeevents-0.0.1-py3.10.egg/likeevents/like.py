from .liketypes.reader import LikeABCReader
from .router import LikeRouter


class Like(LikeRouter):
    async def listen(self, reader: LikeABCReader) -> None:
        async for update in reader.read():
            await self.event(
                update_type=update._event(),
                event=update,
            )
