"""Program to entangle states to GHZ."""

import logging
from typing import List

from netsquid.components.instructions import INSTR_CNOT, INSTR_H, INSTR_MEASURE
from netsquid.components.qprogram import QuantumProgram

logger = logging.getLogger(__name__)


# TODO Use physical gates for noise
class CreateGHZ(QuantumProgram):
    """Turn the bell states into cool GHZ states.

    Properties
    ----------
    bell_qubits : List[int]
        A list of memory positions to find qubits at.

    Methods
    -------
    program
        Defines the program to be run.
    """

    default_num_qubits = -1

    def __init__(self, bell_qubits: List[int]) -> None:
        """Initialise.

        Parameters
        ----------
        bell_qubits : List[int]
            A list of memory positions to act upon.
        """
        super().__init__()
        # we don't want to do operations on 0.
        self.bell_qubits = bell_qubits[1:]

    def program(self) -> None:
        """Create a GHZ state from qubits in memory."""
        logger.debug("Beginning GHZ creation.")
        logger.debug(f"Using qubits {self.bell_qubits}")

        for qubit in self.bell_qubits:
            self.apply(
                INSTR_CNOT, [0, qubit], physical=False, output_key=f"cnot-{qubit}"
            )
            logger.debug(f"Applying CNOT 0->{qubit}")

        for qubit in self.bell_qubits:
            self.apply(
                INSTR_MEASURE, qubit, output_key=f"measure-{qubit}", physical=False
            )
            logger.debug(f"Measurement on qubit {qubit}")

        yield self.run()
