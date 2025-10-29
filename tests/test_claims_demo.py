import pytest

from src.qaswp import QASWPSession, VOCAB


def do_handshake():
    cli = QASWPSession(is_client=True)
    srv = QASWPSession(is_client=False)
    hello = cli.client_pass_1()
    resp = srv.server_pass_2(hello)
    assert resp["status"] == "ok"
    fin = cli.client_pass_3(resp)
    assert fin["status"] == "ok"
    return cli, srv


def test_shared_keys_match():
    cli, srv = do_handshake()
    assert cli.session_key == srv.session_key
    assert isinstance(cli.entanglement_id(), str)
    assert cli.entanglement_id() == srv.entanglement_id()


def test_batch_semantic_compression_over_repeats():
    cli, srv = do_handshake()
    # 100 identical templated messages (predictable / demo traffic)
    msgs = [[VOCAB["GET"], VOCAB["/api/v1/profile"]]] * 100
    plain_total = 0
    wire_total = 0
    for toks in msgs:
        plain_total += len(b"GET /api/v1/profile HTTP/1.1")
        pkt = cli.weave_packet(toks)
        wire_total += pkt["wire_len"]
    # ensure last batch flushes
    if wire_total == 0:
        # force a flush by sending a mismatch token
        pkt = cli.weave_packet([VOCAB["GET"], VOCAB["/api/v1/data"]])
        wire_total += pkt["wire_len"]
    ratio = (1 - (wire_total / plain_total)) * 100.0
    print(f"Compression ratio: {ratio:.2f}% (wire={wire_total}, plain={plain_total})")
    assert ratio >= 95.0


def test_demo_zk_like_proof_is_succinct_and_verifies():
    cli, srv = do_handshake()
    msg = b"demo inference result"
    proof = cli.demo_generate_proof(msg)
    assert len(proof) <= 64
    assert cli.demo_verify_proof(proof, msg)
    # tamper
    bad = proof[:-1] + bytes([proof[-1] ^ 0xFF])
    assert not cli.demo_verify_proof(bad, msg)
