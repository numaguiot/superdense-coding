import os
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

DIR_IMG = "images"
if not os.path.exists(DIR_IMG):
    os.makedirs(DIR_IMG)

def superdense_coding():
    #we test the 4 possible messages
    messages = ['00', '01', '10', '11']
    simulator = AerSimulator()
    results = {}
    for message in messages: 
        print(f"\n --- Test message: {message} ---")

        #initialization (2 qubits, 2 classical bits)
        qr = QuantumRegister(2, name="q")
        cr = ClassicalRegister(2, name="c")
        qc = QuantumCircuit(qr, cr)

        # Step 1: Create entanglement
        #we create a Bell pair between qubit 0 and qubit 1
        qc.h(0)
        qc.cx(0, 1)
        qc.barrier()

        # Step 2: Encode the message
        if message == '00':
            pass  # No operation needed
        elif message == '10':
            qc.x(0)  # Apply X gate
        elif message == '01':
            qc.z(0)  # Apply Z gate
        elif message == '11':
            qc.z(0)  # Apply Z gate
            qc.x(0)  # Apply X gate
        
        qc.barrier()

        # Step 3: Transmission
        # Alice sends qubit 0 to Bob
        # Bob now has both qubits (0 and 1)

        # Step 4: Decode the message
        qc.cx(0, 1)
        qc.h(0)
        qc.barrier()

        # Step 5: Measurement
        qc.measure([0, 1], [0, 1]) #q0 -> c0, q1 -> c1

        job = simulator.run(qc, shots=1000)
        result = job.result().get_counts()

        message_received = max(result, key=result.get)
        results[message] = message_received

        print(f" Message sent: {message}, Message received: {message_received}")

        if message == "11":
            path_img = os.path.join(DIR_IMG, "superdense_circuit_11.png")
            qc.draw(output="mpl", filename=path_img)
            print(f" Circuit diagram saved to {path_img}")

            path_hist = os.path.join(DIR_IMG, "superdense_histogram_11.png")
            fig = plot_histogram(result, title="Measurement Results for message '11'")
            fig.savefig(path_hist)
            print(f" Histogram saved to {path_hist}")

    print("\n FINAL RESULTS:")
    total_success = True
    for sent, received in results.items():
        if sent == received:
            print(f" '{sent}' -> '{received}': SUCCESS")
        else:
            print(f" '{sent}' -> '{received}': FAILURE")
            total_success = False
    if total_success:
        print("All messages were successfully transmitted and received!")
    

if __name__ == "__main__":
    superdense_coding()

