from src.qaswp import QASWPSession, VOCAB


def test_entanglement_stub_is_identical_on_both_ends():
    cli = QASWPSession(is_client=True)
    srv = QASWPSession(is_client=False)
    hello = cli.client_pass_1()
    resp = srv.server_pass_2(hello)
    assert resp["status"] == "ok"
    fin = cli.client_pass_3(resp)
    assert fin["status"] == "ok"
    assert cli.entanglement_id() == srv.entanglement_id()
