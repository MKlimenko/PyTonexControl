import pytonexcontrol


def test_noise_gate_on():
    controller = pytonexcontrol.TonexOneController()
    message = controller.prepare_message_single_parameter(
        pytonexcontrol.TonexParam.NOISE_GATE_ENABLE, 1
    )
    # fmt: off
    assert message == bytearray([0x7E, 0xB9, 0x03, 0x81, 0x09, 0x03, 0x82, 0x0A,
                                 0x00, 0x80, 0x0B, 0x03, 0xB9, 0x04, 0x02, 0x00,
                                 0x01, 0x88, 0x00, 0x00, 0x80, 0x3F, 0xB2, 0x71, 0x7E])
    # fmt: on


def test_noise_gate_off():
    controller = pytonexcontrol.TonexOneController()
    message = controller.prepare_message_single_parameter(
        pytonexcontrol.TonexParam.NOISE_GATE_ENABLE, 0
    )
    # fmt: off
    assert message == bytearray([0x7E, 0xB9, 0x03, 0x81, 0x09, 0x03, 0x82, 0x0A,
                                 0x00, 0x80, 0x0B, 0x03, 0xB9, 0x04, 0x02, 0x00,
                                 0x01, 0x88, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x34, 0x7E])
    # fmt: on


if __name__ == "__main__":
    test_noise_gate_on()
