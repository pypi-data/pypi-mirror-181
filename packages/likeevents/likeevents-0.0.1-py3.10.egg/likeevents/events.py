from typing import Any, Callable

from .liketypes import (
    LikeAsyncCallbackType,
    LikeCallbackType,
    LikeEventObject,
    LikeFilterObject,
    LikeHandlerObject,
    enums,
    mixins,
)


class LikeEventObserver(mixins.LikeEventObserverMixin):
    def __init__(self, event_name: str) -> None:
        super(LikeEventObserver, self).__init__(event_name=event_name)

        self.handlers: list[LikeHandlerObject] = []

    def register(
        self,
        callback: LikeAsyncCallbackType,
        *filters: LikeCallbackType,
    ) -> LikeAsyncCallbackType:
        self.handlers.append(
            LikeHandlerObject(
                callback=callback,
                filters=[LikeFilterObject(filter) for filter in filters],
            )
        )

        return callback

    async def trigger(self, event: LikeEventObject, **kwargs: Any) -> Any:
        for handler in self.handlers:
            result, data = await handler.check(event, **kwargs)
            if result:
                kwargs.update(data, handler=handler)

                return await handler.callback(event)  # noqa
        return enums.RouterHandleEnum.UNHANDLED

    def __call__(
        self, *filters: LikeCallbackType
    ) -> Callable[[LikeAsyncCallbackType], LikeAsyncCallbackType]:
        def wrapper(callback: LikeAsyncCallbackType) -> LikeAsyncCallbackType:
            self.register(callback, *filters)
            return callback

        return wrapper
