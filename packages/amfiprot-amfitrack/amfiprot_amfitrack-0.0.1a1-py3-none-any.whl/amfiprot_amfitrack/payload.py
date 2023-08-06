import enum
import array
import struct

import amfiprot.payload
from amfiprot.payload import Payload


class PayloadType(enum.IntEnum):

    SOURCE_COIL_DATA = 0x10
    REQUEST_CALIBRATION_SIGNAL = 0x11

    CALIBRATE = 0x12
    CALIBRATE_IF_UNCALIBRATED = 0x13

    EMF = 0x14
    EMF_TIMESTAMP = 0x15
    EMF_IMU = 0x16
    EMF_IMU_TIMESTAMP = 0x17
    IMU = 0x18
    IMU_TIMESTAMP = 0x19
    EMF_IMU_FRAME_ID = 0x1A

    SET_SEND_IMU = 0x20
    SOURCE_COIL_CAL_DATA = 0x21
    SOURCE_COIL_CAL_IMU_DATA = 0x22

    METADATA = 0x80
    EMF_META = 0x81
    EMF_IMU_META = 0x82

    RAW_B_FIELD_X = 0xA0  # DEPRECATED
    RAW_B_FIELD_Y = 0xA1  # DEPRECATED
    RAW_B_FIELD_Z = 0xA2  # DEPRECATED
    RAW_B_FIELD_REF = 0xA3  # DEPRECATED
    RAW_B_FIELD = 0xA4
    NORM_B_FIELD = 0xA5
    B_FIELD_PHASE = 0xA6

    CALIBRATED_B_FIELD_X = 0xB3  # DEPRECATED
    CALIBRATED_B_FIELD_Y = 0xB4  # DEPRECATED
    CALIBRATED_B_FIELD_Z = 0xB5  # DEPRECATED
    SOURCE_CROSS_TALK = 0xC0
    RAW_ADC_SAMPLES = 0xE0

    RAW_FLOATS = 0xE1
    STOP_CALIBRATION_SIGNAL = 0xE2
    SET_PHASE_MODULATION = 0xE3
    SIGN_DATA = 0xE4
    PLL = 0xE5

"""
TODO: Instead of making separate classes for each EMF/IMU type payload (with lots of code duplication), maybe create EMF payload and use decorator
pattern to create the rest? Or create e.g. and EMF (data)class that has pos and quat data, so you access it via
packet.payload.emf.pos_x and packet.payload.imu.acc_x.
"""


class CalibratePayload(Payload):
    payload_type = PayloadType.CALIBRATE

    def __init__(self, source_tx_id=0xFF):
        self.data = array.array('B', source_tx_id)
        self.source_tx_id = source_tx_id

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return "<Calibrate> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'source_tx_id': self.source_tx_id
        }


class SetPhaseModulationPayload(Payload):
    payload_type = PayloadType.SET_PHASE_MODULATION

    def __init__(self, enable):
        self.data = array.array('B', [enable])
        self.enable = enable

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "<Set Phase Modulation>" + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'enable': self.enable
        }


class EmfPayload(Payload):
    payload_type = PayloadType.EMF

    def __init__(self, data):
        self.data = data
        self.emf = EmfData(data[0:21])
        self.sensor_status = data[21]
        self.source_coil_id = data[22]

    def __len__(self) -> int:
        """ Length of the payload in bytes (without the CRC byte) """
        return len(self.data)

    def __str__(self) -> str:
        return "<EMF> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'emf': self.emf,
            'sensor_status': self.sensor_status,
            'source_coil_id': self.source_coil_id,
        }


class EmfTimestampPayload(Payload):
    payload_type = PayloadType.EMF_TIMESTAMP

    def __init__(self, data):
        self.data = data
        self.emf = EmfData(data[0:21])
        self.sensor_status = data[21]
        self.source_coil_id = data[22]
        self.timestamp = int.from_bytes(data[23:27], byteorder='little', signed=False)

    def __len__(self) -> int:
        """ Length of the payload in bytes (without the CRC byte) """
        return len(self.data)

    def __str__(self) -> str:
        return "<EMF Timestamp> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'emf': self.emf,
            'timestamp': self.timestamp,
            'sensor_status': self.sensor_status,
            'source_coil_id': self.source_coil_id,
        }


class EmfImuPayload(Payload):
    payload_type = 0x16

    def __init__(self, data):
        self.data = data
        self.emf = EmfData(data[0:21])
        self.sensor_status = data[21]
        self.source_coil_id = data[22]
        self.imu = ImuData(data[23:47])

    def __len__(self) -> int:
        """ Length of the payload in bytes (without the CRC byte) """
        return len(self.data)

    def __str__(self) -> str:
        return "<EMF IMU> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'emf': self.emf,
            'imu': self.imu,
            'sensor_status': self.sensor_status,
            'source_coil_id': self.source_coil_id,
        }


class EmfImuTimestampPayload(Payload):
    payload_type = 0x16

    def __init__(self, data):
        self.data = data
        self.emf = EmfData(data[0:21])
        self.sensor_status = data[21]
        self.source_coil_id = data[22]
        self.imu = ImuData(data[23:47])
        self.timestamp = int.from_bytes(data[47:49], byteorder='little', signed=False)

    def __len__(self) -> int:
        """ Length of the payload in bytes (without the CRC byte) """
        return len(self.data)

    def __str__(self) -> str:
        return "<EMF IMU> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'emf': self.emf,
            'imu': self.imu,
            'sensor_status': self.sensor_status,
            'source_coil_id': self.source_coil_id,
        }


class EmfImuFrameIdPayload(amfiprot.payload.Payload):
    payload_type = PayloadType.EMF_IMU_FRAME_ID

    def __init__(self, data):
        self.data = data
        self.emf = EmfData(self.data[0:21])
        self.sensor_status = self.data[21]
        self.source_coil_id = self.data[22]
        self.calc_id = int.from_bytes(self.data[23:25], byteorder='little', signed=False)
        self.imu = ImuData(self.data[25:39])
        self.gpio_state = int.from_bytes(self.data[39:41], byteorder='little', signed=False)
        self.frame_id = int.from_bytes(self.data[42:45], byteorder='little', signed=False)

    def __len__(self) -> int:
        """ Length of the payload in bytes (without the CRC byte) """
        return len(self.data)

    def __str__(self) -> str:
        return "<EMF FrameID> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'frame_id': self.frame_id,
            'emf': self.emf,
            'imu': self.imu,
            'sensor_status': self.sensor_status,
            'source_coil_id': self.source_coil_id,
            'calc_id': self.calc_id,
            'gpio_state': self.gpio_state
        }


class RawBFieldPayload(amfiprot.payload.Payload):
    """
    B-field given as a two-dimensional array (source_on_sensor):
    ((x_on_x, x_on_y, x_on_z),
     (y_on_x, y_on_y, y_on_z),
     (z_on_x, z_on_y, z_on_z))
    """
    payload_type = PayloadType.RAW_B_FIELD

    def __init__(self, data):
        self.data = data
        b_field_data = struct.unpack("<9f", data[0:36])
        self.b_field = ((b_field_data[0], b_field_data[1], b_field_data[2]),
                        (b_field_data[3], b_field_data[4], b_field_data[5]),
                        (b_field_data[6], b_field_data[7], b_field_data[8]))
        self.current = struct.unpack("<3f", data[36:48])
        self.sensor_status = data[48]
        self.source_coil_id = data[49]
        self.frame_id = int.from_bytes(data[49:52], byteorder='little', signed=False)

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return "<Raw B-Field> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'b_field': self.b_field,
            'current': self.current,
            'sensor_status': self.sensor_status,
            'source_coil_id': self.source_coil_id,
            'frame_id': self.frame_id
        }


class SourceCoilCalDataPayload(amfiprot.payload.Payload):
    payload_type = PayloadType.SOURCE_COIL_CAL_DATA

    def __init__(self, data):
        self.data = data
        self.current = struct.unpack("<3f", data[0:12])
        self.frequency = struct.unpack("<3f", data[12:24])
        self.calibration = struct.unpack("<3f", data[24:36])

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return "<Source Coil Calibration Data> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'current': self.current,
            'frequency': self.frequency,
            'calibration': self.calibration
        }


class SignDataPayload(amfiprot.Payload):
    payload_type = PayloadType.SIGN_DATA

    def __init__(self, data):
        self.data = data
        self.coil = data[0]
        unpacked_floats = struct.unpack("<4f", data[1:17])
        self.pll_freq = unpacked_floats[0]
        self.phase_division = unpacked_floats[1]
        self.remainder_offset = unpacked_floats[2]
        self.remainder = unpacked_floats[3]

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return "<Sign data> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'coil': self.coil,
            'pll_freq': self.pll_freq,
            'phase_division': self.phase_division,
            'remainder_offset': self.remainder_offset,
            'remainder': self.remainder
        }


class PllPayload(amfiprot.Payload):
    payload_type = PayloadType.PLL

    def __init__(self, data):
        self.data = data
        self.frequency = struct.unpack("<3f", data[0:12])
        self.phase_error = struct.unpack("<3f", data[12:24])

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return "<PLL frequencies> " + str(self.to_dict())

    @property
    def type(self) -> PayloadType:
        return self.payload_type

    def to_bytes(self) -> array.array:
        return array.array('B', self.data)

    def to_dict(self) -> dict:
        return {
            'frequency': self.frequency,
            'phase_error': self.phase_error
        }


amfitrack_payload_mappings = {
    PayloadType.CALIBRATE: CalibratePayload,
    PayloadType.SOURCE_COIL_CAL_DATA: SourceCoilCalDataPayload,
    PayloadType.SET_PHASE_MODULATION: SetPhaseModulationPayload,
    PayloadType.EMF: EmfPayload,
    PayloadType.EMF_TIMESTAMP: EmfTimestampPayload,
    PayloadType.EMF_IMU: EmfImuPayload,
    PayloadType.EMF_IMU_TIMESTAMP: EmfImuTimestampPayload,
    PayloadType.EMF_IMU_FRAME_ID: EmfImuFrameIdPayload,
    PayloadType.RAW_B_FIELD: RawBFieldPayload,
    PayloadType.SIGN_DATA: SignDataPayload,
    PayloadType.PLL: PllPayload
}


def interpret_amfitrack_payload(payload: amfiprot.Payload, payload_type):
    if payload_type in amfitrack_payload_mappings:
        return amfitrack_payload_mappings[payload_type](payload.to_bytes())  # type: ignore
    else:
        return payload


class EmfData:
    def __init__(self, data):
        self.pos_x = float(int.from_bytes(data[0:3], byteorder='little', signed=True)) / 100.0
        self.pos_y = float(int.from_bytes(data[3:6], byteorder='little', signed=True)) / 100.0
        self.pos_z = float(int.from_bytes(data[6:9], byteorder='little', signed=True)) / 100.0

        self.quat_x = float(int.from_bytes(data[9:12], byteorder='little', signed=True)) / 1000000.0
        self.quat_y = float(int.from_bytes(data[12:15], byteorder='little', signed=True)) / 1000000.0
        self.quat_z = float(int.from_bytes(data[15:18], byteorder='little', signed=True)) / 1000000.0
        self.quat_w = float(int.from_bytes(data[18:21], byteorder='little', signed=True)) / 1000000.0


class ImuData:
    def __init__(self, data):
        self.acc_x = float(int.from_bytes(data[0:2], byteorder='little', signed=True)) * 0.000122  # In g
        self.acc_y = float(int.from_bytes(data[2:4], byteorder='little', signed=True)) * 0.000122
        self.acc_z = float(int.from_bytes(data[4:6], byteorder='little', signed=True)) * 0.000122

        self.gyro_x = float(int.from_bytes(data[6:8], byteorder='little', signed=True)) * 0.07  # In deg per sec
        self.gyro_y = float(int.from_bytes(data[8:10], byteorder='little', signed=True)) * 0.07
        self.gyro_z = float(int.from_bytes(data[10:12], byteorder='little', signed=True)) * 0.07

        self.quat_x = float(int.from_bytes(data[12:15], byteorder='little', signed=True)) / 1000000.0
        self.quat_y = float(int.from_bytes(data[15:18], byteorder='little', signed=True)) / 1000000.0
        self.quat_z = float(int.from_bytes(data[18:21], byteorder='little', signed=True)) / 1000000.0
        self.quat_w = float(int.from_bytes(data[21:24], byteorder='little', signed=True)) / 1000000.0
