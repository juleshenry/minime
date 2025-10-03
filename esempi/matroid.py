import numpy as np
import random
import time
from enum import Enum, auto

class State(Enum):
    """Defines the states for the developer state machine."""
    JIRA_BOARD = auto()
    ATTEMPT_SOLUTION = auto()
    SPRAY_FEATURES = auto()
    DONE = auto()

class DeveloperStateMachine:
    """
    A state machine simulating a developer's workflow, including distractions.
    """
    def __init__(self):
        self.state = State.JIRA_BOARD
        self.task = None
        print("--- Starting Developer Workflow Simulation ---")

    def run(self):
        """Runs the state machine until it reaches the DONE state."""
        while self.state != State.DONE:
            if self.state == State.JIRA_BOARD:
                self._handle_jira_board()
            elif self.state == State.ATTEMPT_SOLUTION:
                self._handle_attempt_solution()
            elif self.state == State.SPRAY_FEATURES:
                self._handle_spray_features()
            time.sleep(1)
        print("--- Workflow Complete. Developer is resting. ---")

    def _handle_jira_board(self):
        """State for browsing the Jira board."""
        print("\n[STATE: JIRA_BOARD]")
        self.task = f"JIRA-TICKET-{random.randint(100, 999)}"
        print(f"Selected task: {self.task}")
        self.state = State.ATTEMPT_SOLUTION

    def _handle_attempt_solution(self):
        """State for attempting to solve the selected task."""
        print(f"\n[STATE: ATTEMPT_SOLUTION] - Working on {self.task}")
        print("Thinking really hard...")
        
        # Decide the outcome of the attempt
        if random.random() < 0.4:  # 40% chance of success
            print(f"Success! {self.task} has been resolved.")
            self.state = State.DONE
        else: # 60% chance of getting distracted
            print("This is too complex. I have a brilliant idea for a new feature!")
            self.state = State.SPRAY_FEATURES

    def _handle_spray_features(self):
        """State for getting distracted and adding random features."""
        print("\n[STATE: SPRAY_FEATURES] - Entering creative mode!")
        num_features = random.randint(1, 3)
        print(f"Implementing {num_features} new 'essential' feature(s)...")

        for i in range(num_features):
            self._generate_feature(i + 1)

        print("Okay, that's enough features for now. Back to the board.")
        self.state = State.JIRA_BOARD

    def _generate_feature(self, feature_num):
        """Generates a 'feature' using a random numpy operation."""
        op = random.choice(['add', 'multiply', 'dot', 'mean', 'std'])
        dim1, dim2 = random.randint(2, 4), random.randint(2, 4)
        a = np.random.rand(dim1, dim2) * 100
        b = np.random.rand(dim1, dim2) * 100
        
        result = None
        op_str = ""

        print(f"\n  Feature #{feature_num}: Applying a random numpy operation.")
        if op == 'add':
            result = np.add(a, b)
            op_str = "element-wise addition"
        elif op == 'multiply':
            result = np.multiply(a, b)
            op_str = "element-wise multiplication"
        elif op == 'dot':
            # Ensure dimensions are compatible for dot product
            b = np.random.rand(dim2, dim1) * 100
            result = np.dot(a, b)
            op_str = "dot product"
        elif op == 'mean':
            result = np.mean(a)
            op_str = "mean"
        elif op == 'std':
            result = np.std(a)
            op_str = "standard deviation"
        
        print(f"  New feature implemented: '{op_str}'. Result sample: {np.ravel(result)[0]:.2f}")


if __name__ == "__main__":
    developer_sim = DeveloperStateMachine()
    developer_sim.run()