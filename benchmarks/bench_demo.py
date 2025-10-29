from src.qaswp import QASWPSession, VOCAB

def run():
    cli = QASWPSession(is_client=True)
    srv = QASWPSession(is_client=False)

    # Handshake
    hello = cli.client_pass_1()
    resp = srv.server_pass_2(hello)
    assert resp["status"] == "ok"
    cli.client_pass_3(resp)

    # Repeated predictable traffic (demo-mode claim)
    msgs = [[VOCAB["GET"], VOCAB["/api/v1/profile"]]] * 512
    plain_total, wire_total = 0, 0

    for toks in msgs:
        # demo-length baseline; keep consistent with tests
        plain_total += len(b"GET /api/v1/profile HTTP/1.1")
        pkt = cli.weave_packet(toks)
        wire_total += pkt["wire_len"]

    # Explicit end-of-stream flush to account trailing confirmations
    fl = cli.flush()
    if fl:
        wire_total += fl["wire_len"]

    ratio = (1 - (wire_total / max(1, plain_total))) * 100.0
    print(f"[BENCH] demo compression: {ratio:.2f}% (wire={wire_total}, plain={plain_total})")
    return ratio


if __name__ == "__main__":
    r = run()
    assert r >= 99.0, "Demo-mode repeated templates must achieve ≥99% compression"
