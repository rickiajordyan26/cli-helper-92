from typing import Callable, Iterator, TypeVar, Generic, Iterable

I = TypeVar("I")
O = TypeVar("O")

# Creative type alias representing a stream transformer function
StreamOp = Callable[[Iterable[I]], Iterator[O]]

class StreamPipeline(Generic[I]):
    """A fluid pipeline for transforming CLI output sequences creatively.

    Supports chaining stream operations using the custom `>>` operator to defer
    execution until collection, keeping the memory footprint low.
    """

    def __init__(self, data: Iterable[I]) -> None:
        """Initializes the pipeline with a lazy iterable source."""
        self._data: Iterable[I] = data

    def __rshift__(self, operator: StreamOp[I, O]) -> "StreamPipeline[O]":
        """Applies a StreamOp stage to the current pipeline lazily.

        Args:
            operator: A generator-function transforming Iterable[I] to Iterator[O].
        """
        return StreamPipeline(operator(self._data))

    def consume(self, sep: str = "\n") -> str:
        """Resolves the pipeline and collapses it into a single formatted string."

        Returns:
            A single joined string representing the evaluated sequence.
        """
        return sep.join(str(item) for item in self._data)


def prefix_tag(tag: str) -> StreamOp[str, str]:
    """Curried stream transformer that prefixes each text item with a styled tag."""
    def _prefix(stream: Iterable[str]) -> Iterator[str]:
        for text in stream:
            yield f"[{tag.upper()}] {text}"
    return _prefix


def truncate_elements(limit: int) -> StreamOp[str, str]:
    """Truncates string items to a maximum length, appending an ellipsis if exceeded."""
    def _truncate(stream: Iterable[str]) -> Iterator[str]:
        for text in stream:
            yield text[:limit] + "..." if len(text) > limit else text
    return _truncate
