class BasicLFSR:
    """
    A 4-bit Linear Feedback Shift Register (LFSR) with fixed taps at R0 and R3 (indices 3 and 0), initialized to 0110.
    """
    def __init__(self):
        # Initial state: 0110, where state[0]=R3, state[1]=R2, state[2]=R1, state[3]=R0
        self.state = [0, 1, 1, 0]
    
    def set_state(self, state):
        """Set the state to a 4-bit list of 0s and 1s."""
        if len(state) != 4 or not all(b in [0, 1] for b in state):
            raise ValueError("State must be a list of 4 bits (0 or 1).")
        self.state = state
    
    def get_state(self):
        """Return the current state."""
        return self.state
    
    def next_stream_bit(self):
        """
        Generate the next stream bit (R0), compute the feedback as R0 XOR R3,
        shift the state right, and insert feedback at R3.
        """
        stream_bit = self.state[3] # R0 is shifted out as the stream bit
        feedback = self.state[3] ^ self.state[0] # R0 XOR R3
        self.state = [feedback] + self.state[:-1] # Shift right, new R3 = feedback
        return stream_bit


if __name__ == "__main__":
    # Demonstrate BasicLFSR functionality
    print("Basic LFSR:")
    lfsr_basic = BasicLFSR()
    for i in range(20):
        state = lfsr_basic.get_state()
        stream_bit = lfsr_basic.next_stream_bit()
        print(f"t={i}: State: {state}, Stream bit: {stream_bit}")