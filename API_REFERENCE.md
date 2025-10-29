# QASWP Python API ReferenceThis document describes the Python API for the core components of the **Quantum-Authenticated Neural Semantic Weaving Protocol (QASWP)**. It is intended for developers integrating QASWP into applications or working on its implementation. The API provides classes for managing a QASWP session and its sub-components: key exchange, compression, proof verification, and context management.## OverviewA typical usage involves creating a `QASWPSession` for each connection (client or server), performing a handshake, and then sending/receiving data through that session. The session internally uses instances of `KeyExchange`, `CompressionEngine`, `ProofVerifier`, and `ContextWeaver` to carry out the protocol steps.**Example: Basic Client-Server Flow**```python# On the client side:client_session = QASWPSession(is_client=True, model_id="en-text-v1")client_session.connect(host="server.example.com", port=4433)client_session.handshake()  # Perform QASWP handshake with the serverclient_session.send(b"Hello, world!")  # Send a plaintext message (will be compressed & encrypted)response = client_session.receive()    # Receive and decrypt/decompress a responseprint("Server said:", response.decode())# On the server side:server_session = QASWPSession(is_client=False, model_id="en-text-v1")server_session.accept(socket)   # Accept an incoming client connection (socket from listen)server_session.handshake()      # Perform QASWP handshake with clientmsg = server_session.receive()  # Get the client's message (already decrypted & decompressed)print("Client said:", msg.decode())server_session.send(b"Hi there, client!")  # Reply to client

























Below, we document each class and its key methods and attributes.
Class: QASWPSession
class QASWPSession:    def __init__(self, is_client: bool, model_id: str, config: Optional[SessionConfig] = None):        ...


Description:Represents a QASWP communication session between two parties. A QASWPSession manages the overall protocol state, including the underlying transport connection, cryptographic keys, and context for compression.

Parameters: - is_client (bool): Set True if this session will initiate the handshake (client role), or False if it will act as the server (responder). - model_id (str): Identifier for the semantic model to use for compression. Both sides must use the same model. This could correspond to a known model name or a path to a model file. Example: "en-text-v1" might indicate an English text compression model version 1. - config (SessionConfig, optional): An optional configuration object or dictionary specifying protocol options (cipher suites, timeouts, use of proofs, etc.). If not provided, defaults are used.
Key Methods:
connect(host: str, port: int, timeout: float = 5.0) -> NoneDescription: For client sessions, establishes a network connection to the specified server (host and port). This would typically create an underlying socket. (In a future version, this might also initiate the quantum link if needed, but as an API, we focus on the classical connection here.)Raises: ConnectionError if the socket cannot connect.


accept(sock: socket.socket) -> NoneDescription: For server sessions, accepts a connection from a listening socket. You pass in a sock obtained from something like server_listener.accept(). This method wraps that socket for use in QASWP. It does not perform the handshake yet.Raises: If the socket is invalid or already used.


handshake() -> NoneDescription: Performs the QASWP handshake with the peer. This involves quantum key exchange (if client, this may block until keys are ready), exchanging handshake messages, and establishing encryption keys and initial context.Behavior: For a client, it sends a ClientHello and waits for ServerHello, etc. For a server, it waits for ClientHello, then responds. This method will internally use KeyExchange, possibly ProofVerifier, and configure the CompressionEngine and ContextWeaver once handshake completes.Return: None on success (session is now established). After this, send() and receive() can be used for data.Raises:




HandshakeError (custom exception) if handshake fails (due to authentication error, mismatch, timeout, etc.).
CryptoError for cryptographic failures.
ProofError if a proof verification fails (in strict mode). Note: This method may block for some time especially if quantum exchange is involved or if proofs are being verified.
send(data: bytes) -> NoneDescription: Sends an application message through the QASWP session. The data can be arbitrary bytes (e.g., UTF-8 encoded text, binary payload). This method will compress and encrypt the data, and then send it over the network.Process:


The ContextWeaver updates the context (if needed) prior to encoding.
The CompressionEngine encodes the plaintext data into a compressed payload (using the current context).
The payload is encrypted and an authentication tag is added.
The resulting packet is sent via the socket. Parameters:
data (bytes): The raw message to send (before compression). If the message is not bytes (e.g., a str), the user should encode it (e.g., msg.encode('utf-8')). Return: None.Raises:

RuntimeError if called before handshake or after session closed.
EncryptionError if encryption fails for some reason.
IOError if network sending fails.
receive(timeout: float = None) -> bytesDescription: Receives the next message from the QASWP session. This will block until a message is available (or the optional timeout expires). It handles decrypting and decompressing the incoming data.Behavior:


Waits for data on the socket. If a complete QASWP packet is received, proceed; if the socket closes, it raises or returns.
Verifies and decrypts the packet using session keys.
Passes the decrypted compressed payload to the CompressionEngine to decode into the original plaintext, using the current context.
Updates the context via ContextWeaver with the decoded message. Parameters:
timeout (float, optional): If specified, the method will wait at most that many seconds for a message. If timeout is None, it will wait indefinitely. Returns: The plaintext bytes of the message. (If the application expects text, they should decode the bytes to str accordingly). Raises:
TimeoutError if no message arrives within timeout.
AuthenticationError if a packet fails integrity check (this might trigger a session abort).
DecompressionError if the payload could not be decompressed (context out of sync or corrupted data).
ConnectionResetError if the connection is closed by peer.
close() -> NoneDescription: Closes the QASWP session and the underlying network connection. This should be called to clean up resources. It will attempt to send a closure alert to the peer (to notify graceful shutdown), then close the socket.Return: None.Post-condition: After calling close(), the session object should not be used for further sends/receives.



Attributes: - session_key (bytes): The symmetric encryption key for this session (e.g., 32 bytes for AES-256). Available after handshake. (In some implementations this may be protected or not directly exposed for security). - peer_identity (str or Certificate): Information about the peer's identity (e.g., a user ID or certificate) obtained during handshake. Could be None if anonymous. - is_secure (bool): Indicates if the session handshake is completed and the channel is secure. (True after handshake() succeeds). - context (ContextWeaver): The context manager instance used. Advanced users might inspect or reset context via this.
Class: KeyExchange
class KeyExchange:    def __init__(self, is_initiator: bool, quantum_backend: Optional[QuantumChannel] = None):        ...    def perform_exchange(self) -> KeyExchangeResult:        ...    def get_shared_key(self) -> bytes:        ...    def get_handshake_messages(self) -> Tuple[bytes, bytes]:        ...








Description:Manages the low-level cryptographic key exchange for QASWP handshake. This includes coordinating the quantum key exchange and any post-quantum classical exchange (like KEM) as needed.

Parameters (constructor): - is_initiator (bool): True if this side starts the exchange (client), False for responder. - quantum_backend (QuantumChannel, optional): An abstraction or handle to a quantum channel or QKD device. If provided, KeyExchange will use it to obtain quantum keys. If None, it will either fail or fall back to classical-only (depending on config).
Key Methods: - perform_exchange() -> KeyExchangeResultDescription: Executes the key exchange process. For initiator, it will produce and send the necessary handshake data (ClientHello). For responder, it will wait for input and then respond (ServerHello). This method will often be called by QASWPSession.handshake() internally rather than by user code directly.Returns: A KeyExchangeResult object (could be a simple dataclass) that contains: - master_secret (bytes): the derived master session key. - handshake_hash (bytes): handshake transcript hash (for verification tags). - negotiated_params (structure): details like chosen cipher suite, model, etc. Raises: - KeyExchangeError if something fails (no common algorithms, quantum failure, etc.).


get_shared_key() -> bytesDescription: After a successful exchange, returns the primary shared secret (e.g., the output of quantum key distribution or the combination of keys). This is typically a raw key that will be further processed into the master secret.Returns: Bytes of shared key material. Raises: If called before exchange or if exchange failed.


get_handshake_messages() -> Tuple[bytes, bytes]Description: Returns the last sent and last received handshake messages (ClientHello and ServerHello, for example). This can be used for debugging or by ProofVerifier to verify signatures, etc.Returns: A tuple (last_msg_sent, last_msg_received). Each is a bytes object containing the raw handshake message.Note: This might be updated or expanded to a list if multiple messages are involved.



Usage:Typically, a developer won't use KeyExchange directly; it's used internally by QASWPSession. But if extending or customizing the handshake (like plugging in a different quantum backend), one might subclass or configure this.

Class: CompressionEngine
class CompressionEngine:    def __init__(self, model: SemanticModel):        ...    def compress(self, plaintext: bytes, context_state: Any) -> bytes:        ...    def decompress(self, payload: bytes, context_state: Any) -> bytes:        ...






Description:Handles semantic compression and decompression using a given model. This is essentially a wrapper around the loaded neural network or algorithm that performs the encoding/decoding.

Parameters: - model (SemanticModel or similar): An object or reference to the neural model used for compression. This could be a custom class representing the neural net (with methods for encode/decode), or simply a reference like a PyTorch model. The SemanticModel interface is assumed to have at least an encode and decode function.
Key Methods: - compress(plaintext: bytes, context_state: Any) -> bytesDescription: Encodes the plaintext message into a compressed form, given the current context_state. The context_state could be, for example, the hidden state of a neural network or some summary of previous messages.Parameters: - plaintext (bytes): The raw message to compress. - context_state (Any): The context information (likely managed by ContextWeaver). The engine uses this to condition the compression. Could be None or empty for first message. Returns: A bytes object representing the compressed payload Z. This might be of variable length, often shorter than plaintext. Raises: - CompressionError if encoding fails or if inputs are invalid.


decompress(payload: bytes, context_state: Any) -> bytesDescription: Decompresses a payload back into the original plaintext, using the provided context. Essentially the inverse of compress.Parameters:


payload (bytes): The compressed data to decode.
context_state (Any): The context at the receiver side (should correspond to the same context the sender had when compressing). Returns: The reconstructed plaintext as bytes. Raises:
DecompressionError if the payload cannot be decoded (due to context mismatch or corruption).
Notes:- The context_state is not modified by CompressionEngine itself; it should be treated as input. The actual update of context happens in ContextWeaver. - The engine may be stateless between calls (pure function given context) or might internally manage some static info (like the model weights). - The SemanticModel provided might be loaded via a deep learning framework. For efficiency, keep the model loaded in memory and reuse it. Loading a model from disk on each call would be very slow. - If using a GPU or accelerator, make sure to handle thread-safety or reuse (e.g., ensure calls are on the same thread that has the GPU context, or use a dedicated thread for compression tasks).

Class: ContextWeaver
class ContextWeaver:    def __init__(self, model: SemanticModel):        ...    def initial_context(self) -> Any:        ...    def update_context(self, prev_context: Any, message: bytes) -> Any:        ...    def merge_remote_context(self, remote_info: Any) -> None:        ...








Description:Manages the semantic context shared between parties. It tracks and updates whatever state is needed to ensure both sides interpret messages consistently.

Parameters: - model (SemanticModel): The model for which this context manager is handling state. This might be needed if context structure depends on model architecture (e.g., hidden state sizes).
Key Methods: - initial_context() -> AnyDescription: Returns an initial context state. Typically called after handshake to get the starting context. This might be a default hidden state (zeros) for an RNN, or an empty history list, etc.Returns: An object representing context (could be a tensor, a tuple of arrays, a custom Context object, etc.).


update_context(prev_context: Any, message: bytes) -> AnyDescription: Produces an updated context state given the previous context and a newly processed message. This is called on the sender side after sending a message (to update local context with what was sent), and on the receiver side after decoding a message (to update with what was received).Parameters:


prev_context (Any): The context state before the message.
message (bytes): The plaintext message that was sent/received. Returns: The new context state. Example: If context is just conversation text, this might append the message to the history. If context is a neural network hidden state, this might run one inference step to get the new hidden state.
merge_remote_context(remote_info: Any) -> NoneDescription: In some advanced scenarios, it might be necessary to adjust context based on explicit info from the remote side. For example, if the protocol does a context reset or if the remote sends a hash of context for verification. This method can be used to merge or reconcile context states.Parameters:


remote_info (Any): Data from the remote relevant to context (maybe a context hash or a partial state). Note: Not always used; could be future expansion. In basic usage, context merges are implicit because both sides simulate the same updates.
Usage:Usually, you won't call ContextWeaver methods from application code; they are used internally by QASWPSession. For example, when receive() gets a message, the session does context = context_weaver.update_context(context, message) to update state.

Threading:If multiple threads/processes could be handling the same session's data (not typical), ensure that context updates are atomic. In single-threaded or event loop scenarios, this isn't an issue.

Context Structure:The type of context depends on the model: - Could be a complex object (like a tuple of (hidden_state, cell_state) for an LSTM). - Could be something simple like a list of recent message embeddings. - It's opaque to the user of the API. The user doesn't need to manipulate it directly; just know that maintaining prev_context and new_context is crucial for correctness.

Class: ProofVerifier
class ProofVerifier:    def __init__(self, verifier_key: Optional[bytes] = None):        ...    def verify_model_proof(self, proof: bytes, expected_hash: bytes) -> bool:        ...    def generate_model_proof(self, model: SemanticModel) -> bytes:        ...    def verify_message_proof(self, proof: bytes, message: bytes) -> bool:        ...








Description:Handles creation and verification of zero-knowledge proofs related to QASWP, such as proving correct model usage or message integrity without revealing secrets. This class abstracts the underlying zk-SNARK or other ZKP library.

Parameters: - verifier_key (bytes, optional): Some proving systems require a verification key (public parameters) for checking proofs. If needed, it can be loaded here (perhaps from a file or configuration). If None, it's assumed the proof system might be trusted setup-less or the key is embedded in the proof.
Key Methods: - verify_model_proof(proof: bytes, expected_hash: bytes) -> boolDescription: Verifies that the provided proof attests to the local party having a model with a specific hash or fingerprint. This would be used during handshake to verify the peer's proof.Parameters: - proof (bytes): The proof data received from the peer. - expected_hash (bytes): The hash of the model that was negotiated/expected (e.g., the model ID's hash). Returns: True if the proof is valid and matches the expected model hash (meaning the peer likely has the correct model), False otherwise.


generate_model_proof(model: SemanticModel) -> bytesDescription: Generates a zero-knowledge proof that this side's model corresponds to the advertised hash or properties. This could be computationally heavy. Usually called after handshake negotiation to send to the peer.Parameters:


model (SemanticModel): The model for which to prove knowledge/integrity. Returns: A proof in binary form that can be sent over the network. Raises: ProofGenerationError if something goes wrong or it's not configured to generate.
verify_message_proof(proof: bytes, message: bytes) -> boolDescription: Verifies a proof attached to a message. This could be used if, for example, a message comes with a zk-proof that it was processed correctly by the sender's model.Parameters:


proof (bytes): The proof data attached to the message.
message (bytes): The plaintext message that was reconstructed. Returns: True if the proof is valid for that message, False if not or if no proof is expected.
Note: The default QASWPSession may not generate or check message proofs by default because of performance. It's something that could be enabled in SessionConfig if high assurance mode is desired.
Typical use: - During handshake: - The server might call proof = proof_verifier.generate_model_proof(model) and include that in ServerHello. - The client, upon receiving proof, calls proof_verifier.verify_model_proof(proof, expected_hash) to decide if handshake continues. - The specifics of what is proven (model hash, or correct execution on a sample input, etc.) are determined by the protocol design and the prover/verifier implementation.
Integration: By default, QASWPSession.handshake() will internally call these if proofs are required. As a developer, you rarely call these directly unless customizing the proof-handling routine.
Performance: Keep in mind generating proofs can be slow (seconds). The API might be asynchronous in a real-world use. In this reference, it's synchronous (blocking). If using in an asyncio loop, consider running proof generation in an executor to not block the event loop.
Supporting Types and Configuration
SessionConfig: A dataclass or dict that might include fields:
use_quantum: bool (whether to perform quantum exchange, default True).
require_proof: bool (whether to require model proofs in handshake).
cipher_suites: list of allowed cipher suite strings or IDs.
timeout: float for handshake.
etc. This can be extended and passed to QASWPSession.
KeyExchangeResult: Possibly a small class to bundle key exchange outputs (as mentioned earlier: keys and negotiated params).
SemanticModel: Abstract representation of the model. Could have:
encode(input_bytes, context) -> encoded_bytes
decode(encoded_bytes, context) -> output_bytes
Possibly a property for model_hash or identifier. In an actual implementation, this could wrap a PyTorch or TensorFlow model or even a custom algorithm.
Relationships Between Classes
QASWPSession: is the high-level orchestrator. It will: - Contain a KeyExchange instance (e.g., self.key_exch) to handle keys. - Contain a CompressionEngine instance (self.compressor) initialized with the agreed model. - Contain a ContextWeaver (self.context_mgr) for context handling. - Contain a ProofVerifier (self.prover) if proofs are used.
The typical internal call flow: - handshake(): - calls self.key_exch.perform_exchange() - gets keys, sets up encryption context (e.g., create cipher object with session_key). - initializes self.context = self.context_mgr.initial_context(). - if proofs needed, uses self.prover to verify peer's proof and to possibly generate its own to send. - send(data): - uses self.compressor.compress(data, self.context) -> compressed - encrypts compressed -> ciphertext - sends ciphertext - updates self.context = self.context_mgr.update_context(self.context, data) - receive(): - reads and decrypts -> compressed payload - uses self.compressor.decompress(payload, self.context) -> plaintext - updates self.context = self.context_mgr.update_context(self.context, plaintext) - returns plaintext
Thread Safety: Generally, one session object should be confined to one thread at a time. If you need to handle concurrent sends or receives, it should be done carefully (e.g., using asyncio or external locking). The classes themselves do not enforce thread safety.
Cleanup: Ensure to call session.close() to free resources. The underlying socket should be closed; any quantum channel resource should be released (the KeyExchange might have a handle to it).
Conclusion
The QASWP Python API allows developers to use the QASWP protocol in their applications at a high level (via QASWPSession.send/receive) while also providing hooks and classes for the underlying components if customization or deeper integration is needed. This design separates concerns: - QASWPSession for session management and networking. - KeyExchange for cryptographic handshakes. - CompressionEngine & ContextWeaver for the AI-based compression logic. - ProofVerifier for optional security proofs.
By following this API, one can incorporate quantum-secure, AI-driven communication into Python applications with relative ease, focusing on sending and receiving messages as with any socket or TLS library, but benefiting from the advanced features of QASWP under the hood. ```

[1] [2] [3] [10] [17] frontiersin.org
https://www.frontiersin.org/journals/communications-and-networks/articles/10.3389/frcmn.2025.1655410/pdf
[4] [5] [6] [7] [15] QKD and authentication: Separating facts from myths - Amazon Science
https://www.amazon.science/blog/qkd-and-authentication-separating-facts-from-myths
[8] [9] [2503.03884] A Quantum Good Authentication Protocol
https://arxiv.org/abs/2503.03884
[11] [12] [2504.19274] TeleSparse: Practical Privacy-Preserving Verification of Deep Neural Networks
https://arxiv.org/abs/2504.19274
[13] [14] Title: Quantum Entanglement and the Semantics of Shared Meaning | by Dan C | Medium
https://medium.com/@dcosmin7/title-quantum-entanglement-and-the-semantics-of-shared-meaning-487a10d4e86a
[16] RFC 9583: Application Scenarios for the Quantum Internet
https://www.rfc-editor.org/rfc/rfc9583.html
