import time
import random

class Node:
    """Represents a single node in a distributed system, simulating Raft-like behavior."""
    def __init__(self, node_id, is_leader=False):
        self.node_id = node_id
        self.is_leader = is_leader
        self.current_value = None  # Value currently proposed by the leader
        self.committed_value = None  # Value agreed upon by a majority and committed
        self.log = []  # Simplified log to store proposed values

    def __str__(self):
        status = "Leader" if self.is_leader else "Follower"
        return f"Node {self.node_id} ({status}) - Committed: {self.committed_value}"

    def receive_proposal(self, leader_id, value):
        """Simulates a follower receiving a log entry proposal from the leader."""
        print(f"  Node {self.node_id} (Follower) received proposal from Leader {leader_id}: '{value}'")
        # In a real Raft, this would involve complex log consistency checks.
        # For this simplified demo, a follower accepts if it's a new proposal.
        if not self.current_value or self.current_value != value:
            self.current_value = value
            self.log.append(value)  # Add to its log
            print(f"  Node {self.node_id} accepts proposal.")
            return True  # Acknowledge acceptance
        print(f"  Node {self.node_id} already has or rejected proposal.")
        return False

    def commit_value(self, value):
        """Simulates a follower committing a value after majority agreement."""
        if self.current_value == value and self.committed_value != value:
            self.committed_value = value
            print(f"  Node {self.node_id} COMMITTED value: '{value}'")
            return True
        return False

def simulate_raft_consensus(num_nodes, proposal_value):
    """Simulates a simplified Raft-like consensus process."""
    print(f"--- Simulating Raft-like Consensus with {num_nodes} nodes ---")

    # 1. Initialize Nodes and Elect a Leader (simplified for demo)
    nodes = []
    leader_id = random.randint(0, num_nodes - 1)  # Randomly pick a leader
    for i in range(num_nodes):
        nodes.append(Node(i, is_leader=(i == leader_id)))

    leader = nodes[leader_id]
    followers = [node for node in nodes if not node.is_leader]

    print(f"\nInitial State:")
    for node in nodes:
        print(f"- {node}")
    print(f"\nLeader elected: Node {leader.node_id}\n")

    # 2. Leader Proposes a Value
    print(f"Leader {leader.node_id} proposes value: '{proposal_value}'")
    leader.current_value = proposal_value
    leader.log.append(proposal_value)  # Leader adds to its own log immediately

    # 3. Leader Sends Proposal to Followers (simulated RPC)
    acknowledgements = 1  # Leader itself implicitly acknowledges its own proposal
    for follower in followers:
        if follower.receive_proposal(leader.node_id, proposal_value):
            acknowledgements += 1
        time.sleep(0.05)  # Simulate network delay

    print(f"\nProposal acknowledgements: {acknowledgements} out of {num_nodes} nodes")

    # 4. Leader Checks for Majority
    majority_threshold = num_nodes // 2 + 1
    print(f"Majority threshold for commitment: {majority_threshold}")

    if acknowledgements >= majority_threshold:
        print(f"Majority reached! Leader {leader.node_id} COMMITS value: '{proposal_value}'")
        leader.committed_value = proposal_value

        # 5. Leader Informs Followers to Commit (simulated RPC)
        print("\nLeader informs followers to commit...")
        for follower in followers:
            follower.commit_value(proposal_value)
            time.sleep(0.05)  # Simulate network delay
    else:
        print("Majority not reached. Value not committed.")

    print("\n--- Final State ---")
    for node in nodes:
        print(f"- {node}")

# Run multiple simulations to demonstrate the concept
if __name__ == "__main__":
    simulate_raft_consensus(num_nodes=5, proposal_value="Hello Raft!")
    print("\n" + "="*40 + "\n")
    simulate_raft_consensus(num_nodes=3, proposal_value="Another Value")
    print("\n" + "="*40 + "\n")
    simulate_raft_consensus(num_nodes=7, proposal_value="Distributed Consensus")
