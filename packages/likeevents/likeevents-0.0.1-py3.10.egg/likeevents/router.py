from typing import Any

from .events import LikeEventObserver
from .liketypes.base import LikeEventObject
from .liketypes.enums import RouterHandleEnum
from .liketypes.mixins.allow_attributes import LikeAllowAttributesMixin


class LikeRouter(LikeAllowAttributesMixin):
    def __init__(self) -> None:
        super(LikeRouter, self).__init__()

    def register(self, name: str, observer: LikeEventObserver) -> None:
        self.observers[name] = observer

    def include_router(self, router: "LikeRouter") -> None:
        self.observers.update(router.observers)

    async def event(self, update_type: str, event: LikeEventObject, **kwargs: dict) -> Any:
        observer = self.observers[update_type]
        return await self._event(observer=observer, update_type=update_type, event=event, **kwargs)

    async def _event(  # noqa
        self, observer: LikeEventObserver, update_type: str, event: LikeEventObject, **kwargs
    ) -> Any:
        response = await observer.trigger(event, **kwargs)

        if response == RouterHandleEnum.UNHANDLED:
            for router in self.sub_routers:
                response = await router.event(update_type=update_type, event=event, **kwargs)
                if response != RouterHandleEnum.UNHANDLED:
                    break

        return response
