from src.qaswp import QASWPSession


def test_demo_zk_like_proof_succinct_and_verifies():
    cli = QASWPSession(is_client=True)
    cli.client_pass_1()
    msg = b"demo inference result"
    proof = cli.demo_generate_proof(msg)
    assert len(proof) <= 64
    assert cli.demo_verify_proof(proof, msg)
