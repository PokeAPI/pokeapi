from .loaders import Loaders


class LoaderMiddleware:
    """
	Graphene middleware for attaching a new instance of Loaders to the
	request context.
	"""

    def resolve(self, next_middleware, root, info, **args):
        if not hasattr(info.context, "loaders"):
            info.context.loaders = Loaders()
        return next_middleware(root, info, **args)
