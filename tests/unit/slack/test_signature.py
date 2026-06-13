from services.api.app.slack.signature import build_signature, verify_signature


def test_verify_signature_accepts_valid_request():
    body = b"text=review+PR+42"
    timestamp = "1000"
    signature = build_signature("secret", timestamp, body)
    assert verify_signature("secret", timestamp, body, signature, now=1000)


def test_verify_signature_rejects_stale_request():
    body = b"text=review+PR+42"
    timestamp = "1000"
    signature = build_signature("secret", timestamp, body)
    assert not verify_signature("secret", timestamp, body, signature, now=2000)

