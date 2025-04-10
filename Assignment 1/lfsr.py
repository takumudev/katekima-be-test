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


class GeneralLFSR:
    """
    A customizable Linear Feedback Shift Register (LFSR) with variable size and tap positions.
    """
    def __init__(self, size, taps, initial_state=None):
        """Initialize with register size, tap indices and optional initial state."""
        self.size = size
        self.taps = taps
        if initial_state is None:
            self.state = [0] * size
        else:
            if len(initial_state) != size or not all(b in [0, 1] for b in initial_state):
                raise ValueError("Initial state must be a list of {size} bits.")
            self.state = initial_state
    
    def set_size(self, size):
        """Set the register size and reset state and taps."""
        self.size = size
        self.state = [0] * size
        self.taps = []
    
    def get_size(self):
        """Return the current register size."""
        return self.size
    
    def set_state(self, state):
        """Set the state to a list matching the register size."""
        if len(state) != self.size or not all(b in [0, 1] for b in state):
            raise ValueError("State must be a list of {size} bits.")
        self.state = state
    
    def get_state(self):
        """Return the current state."""
        return self.state
    
    def set_taps(self, taps):
        """Set the tap sequence (indices for XOR feedback)."""
        self.taps = taps
    
    def reset(self):
        """Reset the state to all zeros."""
        self.state = [0] * self.size
    
    def next_stream_bit(self):
        """
        Generate the next stream bit (R0), compute the feedback by XORing the tap positions,
        shift the state right and insert feedback at the most significant bit.
        """
        stream_bit = self.state[0] # R0 (least significant bit)
        feedback = 0
        for i in self.taps:
            feedback ^= self.state[i] # XOR all tap positions
        self.state = [feedback] + self.state[:-1] # Shift right, new MSB = feedback
        return stream_bit


if __name__ == "__main__":
    # Demonstrate BasicLFSR functionality
    print("======== Basic LFSR ========")
    lfsr_basic = BasicLFSR()
    for i in range(20):
        state = lfsr_basic.get_state()
        stream_bit = lfsr_basic.next_stream_bit()
        print(f"t={i}: State: {state}, Stream bit: {stream_bit}")
    
    # Demonstrate GeneralLFSR functionality configured as BasicLFSR
    print("\n======== General LFSR (configured as Basic LFSR) ========")
    lfsr_general = GeneralLFSR(size=4, taps=[0, 3], initial_state=[0, 1, 1, 0])
    for i in range(20):
        state = lfsr_general.get_state()
        stream_bit = lfsr_general.next_stream_bit()
        print(f"t={i}: State: {state}, Stream bit: {stream_bit}")
