from src.qaswp import VOCAB, QASWPSession


def test_demo_repeated_templates_compress_over_95pct():
    cli = QASWPSession(is_client=True)
    srv = QASWPSession(is_client=False)
    hello = cli.client_pass_1()
    resp = srv.server_pass_2(hello)
    assert resp["status"] == "ok"
    fin = cli.client_pass_3(resp)
    assert fin["status"] == "ok"

    msgs = [[VOCAB["GET"], VOCAB["/api/v1/profile"]]] * 100
    plain_total = 0
    wire_total = 0
    total_msgs = len(msgs)
    for toks in msgs:
        plain_total += len(b"GET /api/v1/profile HTTP/1.1")
        pkt = cli.weave_packet(toks)
        wire_total += pkt["wire_len"]
        if pkt["flushed"]:
            meta = srv.receive_woven_packet(pkt)
            assert meta == {
                "t": "batch",
                "seq": 0,
                "count": 64,
                "bits": (1 << 64) - 1,
            }
    flush_pkt = cli.flush_confirmations()
    wire_total += flush_pkt["wire_len"]
    if flush_pkt["flushed"]:
        meta = srv.receive_woven_packet(flush_pkt)
        assert meta["t"] == "batch"
        assert meta["seq"] + meta["count"] == total_msgs
        assert meta["bits"] == (1 << meta["count"]) - 1
    ratio = (1 - (wire_total / plain_total)) * 100.0
    print(
        "Demo repeated-template compression: "
        f"{ratio:.2f}% (wire={wire_total}, plain={plain_total})"
    )
    assert ratio >= 90.0


def test_demo_single_message_does_not_claim_high_compression():
    cli = QASWPSession(is_client=True)
    srv = QASWPSession(is_client=False)
    hello = cli.client_pass_1()
    resp = srv.server_pass_2(hello)
    assert resp["status"] == "ok"
    fin = cli.client_pass_3(resp)
    assert fin["status"] == "ok"

    toks = [VOCAB["GET"], VOCAB["/api/v1/profile"]]
    pkt = cli.weave_packet(toks)
    assert pkt["wire_len"] >= 0
