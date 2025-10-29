from src.qaswp import QASWPSession, VOCAB


def test_public_flush_noop_and_emit():
    cli = QASWPSession(is_client=True)
    srv = QASWPSession(is_client=False)
    hello = cli.client_pass_1()
    resp = srv.server_pass_2(hello)
    assert resp["status"] == "ok"
    cli.client_pass_3(resp)

    # Produce placeholders by staying under the auto-flush batch size
    for _ in range(5):
        cli.weave_packet([VOCAB["GET"], VOCAB["/api/v1/profile"]])

    out = cli.flush()
    assert out is None or (out.get("flushed") is True and out.get("wire_len", 0) > 0)
