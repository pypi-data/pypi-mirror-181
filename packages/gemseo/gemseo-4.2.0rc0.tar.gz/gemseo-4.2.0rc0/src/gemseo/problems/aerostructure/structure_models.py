from numpy import complex128
from numpy import ones
from pydantic import BaseModel
from numpy.typing import NDArray


class InputModel(BaseModel):
    sweep: NDArray[complex128] = ones(1)
    thick_panels: NDArray[complex128] = ones(1)
    forces: NDArray[complex128] = ones(1)


class OutputModel(BaseModel):
    mass: NDArray[complex128] = ones(1)
    reserve_fact: NDArray[complex128] = ones(1)
    displ: NDArray[complex128] = ones(1)
