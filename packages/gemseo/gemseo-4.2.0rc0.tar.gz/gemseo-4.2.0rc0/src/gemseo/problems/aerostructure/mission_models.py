from numpy import complex128
from numpy import ones
from pydantic import BaseModel
from numpy.typing import NDArray


class InputModel(BaseModel):
    lift: NDArray[complex128] = ones(1)
    mass: NDArray[complex128] = ones(1)
    drag: NDArray[complex128] = ones(1)
    reserve_fact: NDArray[complex128] = ones(1)


class OutputModel(BaseModel):
    range: NDArray[complex128]
    c_lift: NDArray[complex128]
    c_rf: NDArray[complex128]
