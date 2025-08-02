import binascii
from enum import IntEnum, auto
import numpy as np
import serial
import serial.tools.list_ports

VENDOR_ID = 0x1963
PRODUCT_ID = 0x00D1


class TonexPreset(IntEnum):
    A = (auto(),)
    B = (auto(),)
    Stomp = auto()


class TonexParam(IntEnum):
    NOISE_GATE_POST = auto()
    NOISE_GATE_ENABLE = auto()
    NOISE_GATE_THRESHOLD = auto()
    NOISE_GATE_RELEASE = auto()
    NOISE_GATE_DEPTH = auto()
    COMP_POST = auto()
    COMP_ENABLE = auto()
    COMP_THRESHOLD = auto()
    COMP_MAKE_UP = auto()
    COMP_ATTACK = auto()
    EQ_POST = auto()
    EQ_BASS = auto()
    EQ_BASS_FREQ = auto()
    EQ_MID = auto()
    EQ_MIDQ = auto()
    EQ_MID_FREQ = auto()
    EQ_TREBLE = auto()
    EQ_TREBLE_FREQ = auto()
    MODEL_AMP_ENABLE = auto()
    MODEL_SW1 = auto()
    MODEL_GAIN = auto()
    MODEL_VOLUME = auto()
    MODEX_MIX = auto()
    CABINET_UNKNOWN = auto()
    CABINET_TYPE = auto()
    VIR_CABINET_MODEL = auto()
    VIR_RESO = auto()
    VIR_MIC_1 = auto()
    VIR_MIC_1_X = auto()
    VIR_MIC_1_Z = auto()
    VIR_MIC_2 = auto()
    VIR_MIC_2_X = auto()
    VIR_MIC_2_Z = auto()
    VIR_BLEND = auto()
    MODEL_PRESENCE = auto()
    MODEL_DEPTH = auto()
    REVERB_POSITION = auto()
    REVERB_ENABLE = auto()
    REVERB_MODEL = auto()
    REVERB_SPRING1_TIME = auto()
    REVERB_SPRING1_PREDELAY = auto()
    REVERB_SPRING1_COLOR = auto()
    REVERB_SPRING1_MIX = auto()
    REVERB_SPRING2_TIME = auto()
    REVERB_SPRING2_PREDELAY = auto()
    REVERB_SPRING2_COLOR = auto()
    REVERB_SPRING2_MIX = auto()
    REVERB_SPRING3_TIME = auto()
    REVERB_SPRING3_PREDELAY = auto()
    REVERB_SPRING3_COLOR = auto()
    REVERB_SPRING3_MIX = auto()
    REVERB_SPRING4_TIME = auto()
    REVERB_SPRING4_PREDELAY = auto()
    REVERB_SPRING4_COLOR = auto()
    REVERB_SPRING4_MIX = auto()
    REVERB_ROOM_TIME = auto()
    REVERB_ROOM_PREDELAY = auto()
    REVERB_ROOM_COLOR = auto()
    REVERB_ROOM_MIX = auto()
    REVERB_PLATE_TIME = auto()
    REVERB_PLATE_PREDELAY = auto()
    REVERB_PLATE_COLOR = auto()
    REVERB_PLATE_MIX = auto()
    MODULATION_POST = auto()
    MODULATION_ENABLE = auto()
    MODULATION_MODEL = auto()
    MODULATION_CHORUS_SYNC = auto()
    MODULATION_CHORUS_TS = auto()
    MODULATION_CHORUS_RATE = auto()
    MODULATION_CHORUS_DEPTH = auto()
    MODULATION_CHORUS_LEVEL = auto()
    MODULATION_TREMOLO_SYNC = auto()
    MODULATION_TREMOLO_TS = auto()
    MODULATION_TREMOLO_RATE = auto()
    MODULATION_TREMOLO_SHAPE = auto()
    MODULATION_TREMOLO_SPREAD = auto()
    MODULATION_TREMOLO_LEVEL = auto()
    MODULATION_PHASER_SYNC = auto()
    MODULATION_PHASER_TS = auto()
    MODULATION_PHASER_RATE = auto()
    MODULATION_PHASER_DEPTH = auto()
    MODULATION_PHASER_LEVEL = auto()
    MODULATION_FLANGER_SYNC = auto()
    MODULATION_FLANGER_TS = auto()
    MODULATION_FLANGER_RATE = auto()
    MODULATION_FLANGER_DEPTH = auto()
    MODULATION_FLANGER_FEEDBACK = auto()
    MODULATION_FLANGER_LEVEL = auto()
    MODULATION_ROTARY_SYNC = auto()
    MODULATION_ROTARY_TS = auto()
    MODULATION_ROTARY_SPEED = auto()
    MODULATION_ROTARY_RADIUS = auto()
    MODULATION_ROTARY_SPREAD = auto()
    MODULATION_ROTARY_LEVEL = auto()
    DELAY_POST = auto()
    DELAY_ENABLE = auto()
    DELAY_MODEL = auto()
    DELAY_DIGITAL_SYNC = auto()
    DELAY_DIGITAL_TS = auto()
    DELAY_DIGITAL_TIME = auto()
    DELAY_DIGITAL_FEEDBACK = auto()
    DELAY_DIGITAL_MODE = auto()
    DELAY_DIGITAL_MIX = auto()
    DELAY_TAPE_SYNC = auto()
    DELAY_TAPE_TS = auto()
    DELAY_TAPE_TIME = auto()
    DELAY_TAPE_FEEDBACK = auto()
    DELAY_TAPE_MODE = auto()
    DELAY_TAPE_MIX = auto()

    LAST = auto()


TonexParamRanges = {
    TonexParam.NOISE_GATE_POST: (0, 1),
    TonexParam.NOISE_GATE_ENABLE: (0, 1),
    TonexParam.NOISE_GATE_THRESHOLD: (-100, 0),
    TonexParam.NOISE_GATE_RELEASE: (5, 500),
    TonexParam.NOISE_GATE_DEPTH: (-100, -20),
    TonexParam.COMP_POST: (0, 1),
    TonexParam.COMP_ENABLE: (0, 1),
    TonexParam.COMP_THRESHOLD: (-40, 0),
    TonexParam.COMP_MAKE_UP: (-30, 10),
    TonexParam.COMP_ATTACK: (1, 51),
    TonexParam.EQ_POST: (0, 1),
    TonexParam.EQ_BASS: (0, 10),
    TonexParam.EQ_BASS_FREQ: (75, 600),
    TonexParam.EQ_MID: (0, 10),
    TonexParam.EQ_MIDQ: (0.2, 3.0),
    TonexParam.EQ_MID_FREQ: (150, 5000),
    TonexParam.EQ_TREBLE: (0, 10),
    TonexParam.EQ_TREBLE_FREQ: (1000, 4000),
    TonexParam.MODEL_AMP_ENABLE: (0, 1),
    TonexParam.MODEL_SW1: (0, 1),
    TonexParam.MODEL_GAIN: (0, 10),
    TonexParam.MODEL_VOLUME: (0, 10),
    TonexParam.MODEX_MIX: (0, 100),
    TonexParam.CABINET_UNKNOWN: (0, 1),
    TonexParam.CABINET_TYPE: (0, 2),
    TonexParam.VIR_CABINET_MODEL: (0, 10),
    TonexParam.VIR_RESO: (0, 10),
    TonexParam.VIR_MIC_1: (0, 2),
    TonexParam.VIR_MIC_1_X: (0, 10),
    TonexParam.VIR_MIC_1_Z: (0, 10),
    TonexParam.VIR_MIC_2: (0, 2),
    TonexParam.VIR_MIC_2_X: (0, 2),
    TonexParam.VIR_MIC_2_Z: (0, 10),
    TonexParam.VIR_BLEND: (-100, 100),
    TonexParam.MODEL_PRESENCE: (0, 10),
    TonexParam.MODEL_DEPTH: (0, 10),
    TonexParam.REVERB_POSITION: (0, 1),
    TonexParam.REVERB_ENABLE: (0, 1),
    TonexParam.REVERB_MODEL: (0, 5),
    TonexParam.REVERB_SPRING1_TIME: (0, 10),
    TonexParam.REVERB_SPRING1_PREDELAY: (0, 500),
    TonexParam.REVERB_SPRING1_COLOR: (-10, 10),
    TonexParam.REVERB_SPRING1_MIX: (0, 100),
    TonexParam.REVERB_SPRING2_TIME: (0, 10),
    TonexParam.REVERB_SPRING2_PREDELAY: (0, 500),
    TonexParam.REVERB_SPRING2_COLOR: (-10, 10),
    TonexParam.REVERB_SPRING2_MIX: (0, 100),
    TonexParam.REVERB_SPRING3_TIME: (0, 10),
    TonexParam.REVERB_SPRING3_PREDELAY: (0, 500),
    TonexParam.REVERB_SPRING3_COLOR: (-10, 10),
    TonexParam.REVERB_SPRING3_MIX: (0, 100),
    TonexParam.REVERB_SPRING4_TIME: (0, 10),
    TonexParam.REVERB_SPRING4_PREDELAY: (0, 500),
    TonexParam.REVERB_SPRING4_COLOR: (-10, 10),
    TonexParam.REVERB_SPRING4_MIX: (0, 100),
    TonexParam.REVERB_ROOM_TIME: (0, 10),
    TonexParam.REVERB_ROOM_PREDELAY: (0, 500),
    TonexParam.REVERB_ROOM_COLOR: (-10, 10),
    TonexParam.REVERB_ROOM_MIX: (0, 100),
    TonexParam.REVERB_PLATE_TIME: (0, 10),
    TonexParam.REVERB_PLATE_PREDELAY: (0, 500),
    TonexParam.REVERB_PLATE_COLOR: (-10, 10),
    TonexParam.REVERB_PLATE_MIX: (0, 100),
    # Modulation
    TonexParam.MODULATION_POST: (0, 1),
    TonexParam.MODULATION_ENABLE: (0, 1),
    TonexParam.MODULATION_MODEL: (0, 4),
    TonexParam.MODULATION_CHORUS_SYNC: (0, 1),
    TonexParam.MODULATION_CHORUS_TS: (0, 17),
    TonexParam.MODULATION_CHORUS_RATE: (0.1, 10),
    TonexParam.MODULATION_CHORUS_DEPTH: (0, 100),
    TonexParam.MODULATION_CHORUS_LEVEL: (0, 10),
    TonexParam.MODULATION_TREMOLO_SYNC: (0, 1),
    TonexParam.MODULATION_TREMOLO_TS: (0, 17),
    TonexParam.MODULATION_TREMOLO_RATE: (0.1, 10),
    TonexParam.MODULATION_TREMOLO_SHAPE: (0, 10),
    TonexParam.MODULATION_TREMOLO_SPREAD: (0, 100),
    TonexParam.MODULATION_TREMOLO_LEVEL: (0, 10),
    TonexParam.MODULATION_PHASER_SYNC: (0, 1),
    TonexParam.MODULATION_PHASER_TS: (0, 17),
    TonexParam.MODULATION_PHASER_RATE: (0.1, 10),
    TonexParam.MODULATION_PHASER_DEPTH: (0, 100),
    TonexParam.MODULATION_PHASER_LEVEL: (0, 10),
    TonexParam.MODULATION_FLANGER_SYNC: (0, 1),
    TonexParam.MODULATION_FLANGER_TS: (0, 17),
    TonexParam.MODULATION_FLANGER_RATE: (0.1, 10),
    TonexParam.MODULATION_FLANGER_DEPTH: (0, 100),
    TonexParam.MODULATION_FLANGER_FEEDBACK: (0, 100),
    TonexParam.MODULATION_FLANGER_LEVEL: (0, 10),
    TonexParam.MODULATION_ROTARY_SYNC: (0, 1),
    TonexParam.MODULATION_ROTARY_TS: (0, 17),
    TonexParam.MODULATION_ROTARY_SPEED: (0, 400),
    TonexParam.MODULATION_ROTARY_RADIUS: (0, 300),
    TonexParam.MODULATION_ROTARY_SPREAD: (0, 100),
    TonexParam.MODULATION_ROTARY_LEVEL: (0, 10),
    # Delay
    TonexParam.DELAY_POST: (0, 1),
    TonexParam.DELAY_ENABLE: (0, 1),
    TonexParam.DELAY_MODEL: (0, 1),
    TonexParam.DELAY_DIGITAL_SYNC: (0, 1),
    TonexParam.DELAY_DIGITAL_TS: (0, 17),
    TonexParam.DELAY_DIGITAL_TIME: (0, 1000),
    TonexParam.DELAY_DIGITAL_FEEDBACK: (0, 100),
    TonexParam.DELAY_DIGITAL_MODE: (0, 1),
    TonexParam.DELAY_DIGITAL_MIX: (0, 100),
    TonexParam.DELAY_TAPE_SYNC: (0, 1),
    TonexParam.DELAY_TAPE_TS: (0, 17),
    TonexParam.DELAY_TAPE_TIME: (0, 1000),
    TonexParam.DELAY_TAPE_FEEDBACK: (0, 100),
    TonexParam.DELAY_TAPE_MODE: (0, 1),
    TonexParam.DELAY_TAPE_MIX: (0, 100),
}


class TonexOneController:
    def __init__(self):
        self.ser = None
        self.running = False

    def connect(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == VENDOR_ID and port.pid == PRODUCT_ID:
                try:
                    print(f"Found ToneX One on {port.device}")
                    self.ser = serial.Serial(
                        port=port.device,
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0,
                        rtscts=False,
                        dsrdtr=False,
                    )

                    print("Connected to ToneX One")
                    return True
                except Exception as e:
                    print(f"Failed to open {port.device}: {str(e)}")

        print("ToneX One device not found. Please ensure it's connected.")
        return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
                print("Disconnected")
            except:
                pass
            self.ser = None

    def crc16(self, data: bytes) -> int:
        crc = 0xFFFF
        cnt = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0x8408
                else:
                    crc >>= 1
            cnt += 1
        return ~crc & 0xFFFF

    def add_framing(self, combined_message):
        dst = bytearray([0x7E]) + bytearray(
            b
            for byte in combined_message
            for b in ([0x7D, byte ^ 0x20] if byte in (0x7E, 0x7D) else [byte])
        )
        crc = np.uint16(self.crc16(combined_message)).tobytes()
        dst += bytearray(crc)
        dst += bytearray([0x7E])
        return dst

    def prepare_message_single_parameter(self, index, value):
        if type(index) is TonexParam:
            min_val, max_val = TonexParamRanges[index]
            if value < min_val or value > max_val:
                print(
                    f"Value {value} is out of range for {index}. Expected [{min_val}, {max_val}]"
                )
            index = int(index) - 1
        # fmt: off
        message = bytearray([
            #                                   len LSB   len MSB
            0xb9, 0x03, 0x81, 0x09, 0x03, 0x82, 0x0A,     0x00, 0x80, 0x0B, 0x03
        ])
        payload = bytearray([
            #                       param_idx           float values
            0xB9, 0x04, 0x02, 0x00, 0x00,         0x88, 0x00, 0x00, 0x00, 0x00
        ])
        # fmt: on
        print(binascii.hexlify(payload, " ").decode())
        payload[4] = np.uint16(index).tobytes()[0]
        print(binascii.hexlify(payload, " ").decode())

        payload[-4:] = np.float32(value).tobytes()
        combined_message = message + payload
        return self.add_framing(combined_message)

    def send_single_parameter(self, index, value):
        message = self.prepare_message_single_parameter(index, value)
        self.ser.write(message)

    def send_preset(self, preset):
        # fmt: off
        presets = {
            TonexPreset.A : bytearray([
                0x7E, 0xB9, 0x03, 0x81, 0x06, 0x03, 0x82, 0xA4, 0x00, 0x80, 0x0B, 0x03, 0xB9, 0x01, 0xB9, 0x0E,
                0x82, 0x4C, 0x42, 0x4C, 0x47, 0xB9, 0x03, 0x00, 0x04, 0x00, 0x88, 0x00, 0x00, 0x08, 0x41, 0x00,
                0x01, 0x00, 0xBA, 0x14, 0xB9, 0x03, 0x00, 0x00, 0x80, 0xFF, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x80,
                0xFF, 0xB9, 0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x00, 0xB9, 0x03, 0x0F,
                0x80, 0xFF, 0x2F, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x00, 0xB9, 0x03, 0x00, 0x00, 0x80, 0xFF, 0xB9,
                0x03, 0x80, 0xBF, 0x80, 0xBF, 0x80, 0xBF, 0xB9, 0x03, 0x80, 0x9F, 0x80, 0xFF, 0x00, 0xB9, 0x03,
                0x00, 0x80, 0xFF, 0x80, 0xFF, 0xB9, 0x03, 0x11, 0x11, 0x00, 0xB9, 0x03, 0x11, 0x22, 0x00, 0xB9,
                0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x0A, 0x00, 0x0A, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x80,
                0xFF, 0xB9, 0x03, 0x11, 0x00, 0x00, 0xB9, 0x03, 0x00, 0x00, 0x11, 0xB9, 0x03, 0x0B, 0x0B, 0x0B,
                0xB9, 0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x00, 0x80, 0xFF, 0x00, 0xBC, 0x06, 0x00, 0x00,
                0x01, 0x00, 0x02, 0x00, 0x00, 0x00, 0x81, 0xB8, 0x01, 0x01, 0x00, 0x88, 0x00, 0x00, 0xF0, 0x42,
                0xED, 0x64, 0x7E]),
            TonexPreset.B : bytearray([
                0x7E, 0xB9, 0x03, 0x81, 0x06, 0x03, 0x82, 0xA4, 0x00, 0x80, 0x0B, 0x03, 0xB9, 0x01, 0xB9, 0x0E,
                0x82, 0x4C, 0x42, 0x4C, 0x47, 0xB9, 0x03, 0x00, 0x04, 0x00, 0x88, 0x00, 0x00, 0x08, 0x41, 0x00,
                0x01, 0x00, 0xBA, 0x14, 0xB9, 0x03, 0x00, 0x00, 0x80, 0xFF, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x80,
                0xFF, 0xB9, 0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x00, 0xB9, 0x03, 0x0F,
                0x80, 0xFF, 0x2F, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x00, 0xB9, 0x03, 0x00, 0x00, 0x80, 0xFF, 0xB9,
                0x03, 0x80, 0xBF, 0x80, 0xBF, 0x80, 0xBF, 0xB9, 0x03, 0x80, 0x9F, 0x80, 0xFF, 0x00, 0xB9, 0x03,
                0x00, 0x80, 0xFF, 0x80, 0xFF, 0xB9, 0x03, 0x11, 0x11, 0x00, 0xB9, 0x03, 0x11, 0x22, 0x00, 0xB9,
                0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x0A, 0x00, 0x0A, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x80,
                0xFF, 0xB9, 0x03, 0x11, 0x00, 0x00, 0xB9, 0x03, 0x00, 0x00, 0x11, 0xB9, 0x03, 0x0B, 0x0B, 0x0B,
                0xB9, 0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x00, 0x80, 0xFF, 0x00, 0xBC, 0x06, 0x00, 0x00,
                0x01, 0x00, 0x02, 0x00, 0x00, 0x01, 0x81, 0xB8, 0x01, 0x01, 0x00, 0x88, 0x00, 0x00, 0xF0, 0x42,
                0x7C, 0x31, 0x7E]),
            TonexPreset.Stomp : bytearray([
                0x7E, 0xB9, 0x03, 0x81, 0x06, 0x03, 0x82, 0xA4, 0x00, 0x80, 0x0B, 0x03, 0xB9, 0x01, 0xB9, 0x0E,
                0x82, 0x4C, 0x42, 0x4C, 0x47, 0xB9, 0x03, 0x00, 0x04, 0x00, 0x88, 0x00, 0x00, 0x08, 0x41, 0x01,
                0x01, 0x00, 0xBA, 0x14, 0xB9, 0x03, 0x00, 0x00, 0x80, 0xFF, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x80,
                0xFF, 0xB9, 0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x00, 0xB9, 0x03, 0x0F,
                0x80, 0xFF, 0x2F, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x00, 0xB9, 0x03, 0x00, 0x00, 0x80, 0xFF, 0xB9,
                0x03, 0x80, 0xBF, 0x80, 0xBF, 0x80, 0xBF, 0xB9, 0x03, 0x80, 0x9F, 0x80, 0xFF, 0x00, 0xB9, 0x03,
                0x00, 0x80, 0xFF, 0x80, 0xFF, 0xB9, 0x03, 0x11, 0x11, 0x00, 0xB9, 0x03, 0x11, 0x22, 0x00, 0xB9,
                0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x0A, 0x00, 0x0A, 0xB9, 0x03, 0x80, 0xFF, 0x00, 0x80,
                0xFF, 0xB9, 0x03, 0x11, 0x00, 0x00, 0xB9, 0x03, 0x00, 0x00, 0x11, 0xB9, 0x03, 0x0B, 0x0B, 0x0B,
                0xB9, 0x03, 0x80, 0xFF, 0x3F, 0x00, 0xB9, 0x03, 0x00, 0x80, 0xFF, 0x00, 0xBC, 0x06, 0x00, 0x00,
                0x01, 0x00, 0x02, 0x00, 0x00, 0x02, 0x81, 0xB8, 0x01, 0x01, 0x00, 0x88, 0x00, 0x00, 0xF0, 0x42,
                0xFB, 0xC9, 0x7E])
        }
        # fmt: on
        self.ser.write(presets[preset])

    def read_state(self):
        dst = self.ser.read_all()
        print(dst)
        # fmt: off
        hello_request = bytearray([0xb9, 0x03, 0x00, 0x82, 0x06, 0x00, 0x80, 0x0b, 0x03, 0xb9, 0x02, 0x81, 0x06, 0x03, 0x0b])
        # fmt: on
        framed = self.add_framing(hello_request)
        self.ser.write(framed)
        import time

        time.sleep(0.1)
        dst = self.ser.read_all()
        print(dst)


def main():
    controller = TonexOneController()

    try:
        if not controller.connect():
            print("Failed to connect to device")
            return
        controller.read_state()
        # controller.send_preset(TonexPreset.A)
        # controller.send_preset(TonexPreset.B)
        # controller.send_preset(TonexPreset.Stomp)
        # controller.send_preset(TonexPreset.A)

        # controller.send_single_parameter(TonexParam.NOISE_GATE_ENABLE, 1)
        # controller.send_single_parameter(TonexParam.NOISE_GATE_ENABLE, 0)
        # controller.send_single_parameter(TonexParam.MODULATION_ENABLE, 1)
        # controller.send_single_parameter(TonexParam.MODULATION_ENABLE, 0)
        # controller.send_single_parameter(TonexParam.MODULATION_ENABLE, 1)
        # controller.send_single_parameter(TonexParam.MODULATION_ENABLE, 0)

    except KeyboardInterrupt:
        print("\nStopping slot cycling")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        controller.disconnect()


if __name__ == "__main__":
    main()
