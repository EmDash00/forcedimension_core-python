import importlib
import os
import unittest
from ctypes import c_int
from random import randint, random

import pydantic

import forcedimension_core.containers as containers
from forcedimension_core.constants import MAX_DOF, MAX_STATUS


class TestContainers(unittest.TestCase):
    def assertSequenceAlmostEqual(self, seq1, seq2):

        for elem1, elem2 in zip(seq1, seq2):
            self.assertAlmostEqual(elem1, elem2)

    def testVersion(self):
        major = randint(0, 100)
        minor = randint(0, 100)
        release = randint(0, 100)
        revision = randint(0, 100)

        version = containers.VersionTuple(major, minor, release, revision)

        self.assertTupleEqual(version, (major, minor, release, revision))
        self.assertEqual(
            str(version), f"{major}.{minor}.{release}-{revision}"
        )

    def testStatus(self):

        power = randint(0, 100)
        connected = randint(0, 100)
        started = randint(0, 100)
        reset = randint(0, 100)
        idle = randint(0, 100)
        force = randint(0, 100)
        brake = randint(0, 100)
        torque = randint(0, 100)
        wrist_detected = randint(0, 100)
        error = randint(0, 100)
        gravity = randint(0, 100)
        timeguard = randint(0, 100)
        wrist_init = randint(0, 100)
        redundancy = randint(0, 100)
        forceoffcause = randint(0, 100)
        locks = randint(0, 100)
        axis_checked = randint(0, 100)

        expected_field_order = (
            power,
            connected,
            started,
            reset,
            idle,
            force,
            brake,
            torque,
            wrist_detected,
            error,
            gravity,
            timeguard,
            wrist_init,
            redundancy,
            forceoffcause,
            locks,
            axis_checked
        )

        status = containers.Status(*expected_field_order)

        expected_fields = (
            ('power', c_int),
            ('connected', c_int),
            ('started', c_int),
            ('reset', c_int),
            ('idle', c_int),
            ('force', c_int),
            ('brake', c_int),
            ('torque', c_int),
            ('wrist_detected', c_int),
            ('error', c_int),
            ('gravity', c_int),
            ('timeguard', c_int),
            ('wrist_init', c_int),
            ('redundancy', c_int),
            ('forceoffcause', c_int),
            ('locks', c_int),
            ('axis_checked', c_int),
        )

        for expected_field, field in zip(
            expected_fields, status._fields_[:-1]
        ):
            self.assertTupleEqual(expected_field, field)

        self.assertTupleEqual(
            status._fields_[-1],
            ('__padding', c_int * (32 - MAX_STATUS))
        )

        self.assertEqual(power, status.power)
        self.assertEqual(connected, status.connected)
        self.assertEqual(started, status.started)
        self.assertEqual(reset, status.reset)
        self.assertEqual(idle, status.idle)
        self.assertEqual(force, status.force)
        self.assertEqual(brake, status.brake)
        self.assertEqual(torque, status.torque)
        self.assertEqual(wrist_detected, status.wrist_detected)
        self.assertEqual(error, status.error)
        self.assertEqual(gravity, status.gravity)
        self.assertEqual(timeguard, status.timeguard)
        self.assertEqual(wrist_init, status.wrist_init)
        self.assertEqual(redundancy, status.redundancy)
        self.assertEqual(forceoffcause, status.forceoffcause)
        self.assertEqual(locks, status.locks)
        self.assertEqual(axis_checked, status.axis_checked)

        field_order = tuple(status)
        self.assertTupleEqual(expected_field_order, field_order)

        self.assertTrue(len(status), MAX_STATUS)

        for i in range(len(status)):
            val = randint(0, 100)
            status[i] = val

            self.assertEqual(val, status[i])

        self.assertEqual(
            str(status),
            "Status(power={}, connected={}, started={}, reset={}, idle={}, "
            "force={}, brake={}, torque={}, wrist_detected={}, error={}, "
            "gravity={}, timeguard={}, wrist_init={}, redundancy={}, "
            "forceoffcause={}, locks={}, axis_checked={})".format(
                *status
            ),
        )

        s = containers.Status(1)
        self.assertEqual(s.power, 1)

        s = containers.Status(True)
        self.assertTrue(s.power)

        self.assertRaises(ValueError, lambda: containers.Status(None))  # type: ignore


    def testVector3(self):
        x = random()
        y = random()
        z = random()

        self.assertRaises(ValueError, lambda: containers.Vector3((x, y, z, 0)))
        self.assertRaises(ValueError, lambda: containers.Vector3((x, y)))

        v = containers.Vector3((x, y, z))

        self.assertEqual(3, len(v))

        self.assertAlmostEqual(x, v.x)
        self.assertAlmostEqual(y, v.y)
        self.assertAlmostEqual(z, v.z)

        v.x = random()
        v.y = random()
        v.z = random()

        self.assertAlmostEqual(v.x, v[0])
        self.assertAlmostEqual(v.y, v[1])
        self.assertAlmostEqual(v.z, v[2])

        for i in range(len(v)):
            val = random()
            v[i] = val
            self.assertAlmostEqual(val, v[i])

        self.assertIs(v.ptr, v.ptrs[0])

        for i in range(len(v)):
            v.ptr[i] = random()
            self.assertAlmostEqual(v.ptr[i], v[i])
            self.assertTrue(v.ptr[i], v.ptrs[i].contents)

    def testEnc3(self):
        enc0 = randint(0, 100)
        enc1 = randint(0, 100)
        enc2 = randint(0, 100)

        self.assertRaises(
            ValueError, lambda: containers.Enc3((enc0, enc1, enc2, 0))
        )
        self.assertRaises(
            ValueError, lambda: containers.Enc3((enc0, enc1))
        )

        enc = containers.Enc3((enc0, enc1, enc2))
        self.assertEqual(len(enc), 3)

        self.assertEqual(enc[0], enc0)
        self.assertEqual(enc[1], enc1)
        self.assertEqual(enc[2], enc2)

        for i in range(len(enc)):
            val = randint(0, 100)
            enc[i] = val
            self.assertEqual(val, enc[i])

        self.assertIs(enc.ptr, enc.ptrs[0])

        for i in range(len(enc)):
            enc.ptr[i] = randint(0, 100)
            self.assertEqual(enc.ptr[i], enc[i])
            self.assertEqual(enc.ptr[i], enc.ptrs[i].contents.value)

    def testMot3(self):
        mot0 = randint(0, 100)
        mot1 = randint(0, 100)
        mot2 = randint(0, 100)

        self.assertRaises(
            ValueError, lambda: containers.Mot3((mot0, mot1, mot2, 0))
        )
        self.assertRaises(
            ValueError, lambda: containers.Mot3((mot0, mot1))
        )

        mot = containers.Mot3((mot0, mot1, mot2))
        self.assertEqual(len(mot), 3)

        self.assertEqual(mot[0], mot0)
        self.assertEqual(mot[1], mot1)
        self.assertEqual(mot[2], mot2)

        for i in range(len(mot)):
            val = randint(0, 100)
            mot[i] = val
            self.assertEqual(val, mot[i])

        self.assertIs(mot.ptr, mot.ptrs[0])

        for i in range(len(mot)):
            mot.ptr[i] = randint(0, 100)
            self.assertEqual(mot.ptr[i], mot[i])
            self.assertEqual(mot.ptr[i], mot.ptrs[i].contents.value)

    def testEnc4(self):
        enc0 = randint(0, 100)
        enc1 = randint(0, 100)
        enc2 = randint(0, 100)
        enc3 = randint(0, 100)

        self.assertRaises(
            ValueError, lambda: containers.Enc4((enc0, enc1, enc2, enc3, 0))
        )
        self.assertRaises(
            ValueError, lambda: containers.Enc4((enc0, enc1, enc2))
        )

        enc = containers.Enc4((enc0, enc1, enc2, enc3))

        self.assertEqual(len(enc), 4)

        self.assertEqual(enc[0], enc0)
        self.assertEqual(enc[1], enc1)
        self.assertEqual(enc[2], enc2)
        self.assertEqual(enc[3], enc3)

        for i in range(len(enc)):
            val = randint(0, 100)
            enc[i] = val
            self.assertEqual(val, enc[i])

            enc.ptr[i] = randint(0, 100)
            self.assertEqual(enc.ptr[i], enc[i])

    def testDOFInt(self):
        self.assertRaises(
            ValueError, lambda: containers.DOFInt([0] * (MAX_DOF - 1))
        )
        self.assertRaises(
            ValueError, lambda: containers.DOFInt([0] * (MAX_DOF + 1))
        )

        dofs = [randint(0, 100) for _ in range(MAX_DOF)]

        dof_ints = containers.DOFInt(dofs)
        self.assertEqual(MAX_DOF, len(dof_ints))

        for i in range(MAX_DOF):
            self.assertEqual(dofs[i], dof_ints[i])
            self.assertEqual(dofs[i], dof_ints[i])

            dof_ints.ptr[i] = randint(0, 100)
            self.assertEqual(dof_ints.ptr[i], dof_ints[i])

    def testDOFMotorArray(self):
        self.assertRaises(
            ValueError, lambda: containers.DOFMotor([0] * (MAX_DOF - 1))
        )
        self.assertRaises(
            ValueError, lambda: containers.DOFMotor([0] * (MAX_DOF + 1))
        )

        dofs = [randint(0, 100) for _ in range(MAX_DOF)]

        dof_mots = containers.DOFMotor(dofs)
        self.assertEqual(MAX_DOF, len(dof_mots))

        for i in range(MAX_DOF):
            self.assertEqual(dofs[i], dof_mots[i])
            self.assertEqual(dofs[i], dof_mots[i])

            dof_mots.ptr[i] = randint(0, 100)
            self.assertEqual(dof_mots.ptr[i], dof_mots[i])

    def testDOFFloat(self):
        self.assertRaises(
            ValueError, lambda: containers.DOFFloat([0] * (MAX_DOF - 1))
        )
        self.assertRaises(
            ValueError, lambda: containers.DOFFloat([0] * (MAX_DOF + 1))
        )

        dofs = [random() for _ in range(MAX_DOF)]

        dof_floats = containers.DOFFloat(dofs)
        self.assertAlmostEqual(MAX_DOF, len(dof_floats))

        for i in range(MAX_DOF):
            self.assertAlmostEqual(dofs[i], dof_floats[i])
            self.assertAlmostEqual(dofs[i], dof_floats[i])

            dof_floats.ptr[i] = random()
            self.assertEqual(dof_floats.ptr[i], dof_floats[i])

    def testMat3x3(self):
        mat_data = [random() for _ in range(3 * 3 + 1)]

        self.assertRaises(
            ValueError, lambda: containers.Mat3x3(mat_data)
        )

        self.assertRaises(
            ValueError, lambda: containers.Mat3x3(mat_data[:8])
        )

        mat3x3 = containers.Mat3x3(mat_data[:9])

        for i in range(3):
            for j  in range(3):
                self.assertAlmostEqual(mat_data[3 * i + j], mat3x3[i, j])

                val = random()
                mat3x3[i, j] = val
                self.assertAlmostEqual(val, mat3x3[i, j])

        def getitemRaisesTypeErrorTuple():
            mat3x3[0]  # type: ignore

        def getitemRaisesTypeErrorFirstIndex():
            mat3x3[0.0, 0]  # type: ignore

        def getitemRaisesTypeErrorSecondIndex():
            mat3x3[0, 0.0]  # type: ignore

        def setitemRaisesTypeErrorTuple():
            mat3x3[0] = 1  # type: ignore

        def setitemRaisesTypeErrorFirstIndex():
            mat3x3[0.0, 0] = 1  # type: ignore

        def setitemRaisesTypeErrorSecondIndex():
            mat3x3[0, 0.0] = 1  # type: ignore

        self.assertRaises(TypeError, getitemRaisesTypeErrorTuple)
        self.assertRaises(TypeError, getitemRaisesTypeErrorFirstIndex)
        self.assertRaises(TypeError, getitemRaisesTypeErrorSecondIndex)

        self.assertRaises(TypeError, setitemRaisesTypeErrorTuple)
        self.assertRaises(TypeError, setitemRaisesTypeErrorFirstIndex)
        self.assertRaises(TypeError, setitemRaisesTypeErrorSecondIndex)

    def testMat6x6(self):
        mat_data = [random() for _ in range(6 * 6 + 1)]

        self.assertRaises(
            ValueError, lambda: containers.Mat6x6(mat_data)
        )

        self.assertRaises(
            ValueError, lambda: containers.Mat6x6(mat_data[:35])
        )
        mat6x6 = containers.Mat6x6(mat_data[:36])

        for i in range(6):
            for j  in range(6):
                self.assertAlmostEqual(mat_data[6 * i + j], mat6x6[i, j])

                val = random()
                mat6x6[i, j] = val
                self.assertAlmostEqual(val, mat6x6[i, j])


        def getitemRaisesTypeErrorTuple():
            mat6x6[0]  # type: ignore

        def getitemRaisesTypeErrorFirstIndex():
            mat6x6[0.0, 0]  # type: ignore

        def getitemRaisesTypeErrorSecondIndex():
            mat6x6[0, 0.0]  # type: ignore

        def setitemRaisesTypeErrorTuple():
            mat6x6[0] = 1  # type: ignore

        def setitemRaisesTypeErrorFirstIndex():
            mat6x6[0.0, 0] = 1  # type: ignore

        def setitemRaisesTypeErrorSecondIndex():
            mat6x6[0, 0.0] = 1  # type: ignore

        self.assertRaises(TypeError, getitemRaisesTypeErrorTuple)
        self.assertRaises(TypeError, getitemRaisesTypeErrorFirstIndex)
        self.assertRaises(TypeError, getitemRaisesTypeErrorSecondIndex)

        self.assertRaises(TypeError, setitemRaisesTypeErrorTuple)
        self.assertRaises(TypeError, setitemRaisesTypeErrorFirstIndex)
        self.assertRaises(TypeError, setitemRaisesTypeErrorSecondIndex)

    def testSerialization(self):

        class Data(pydantic.BaseModel):
            status: containers.Status = pydantic.Field(
                default_factory=containers.Status
            )

            vec3: containers.Vector3 = pydantic.Field(
                default_factory=containers.Vector3
            )

            enc3: containers.Enc3 = pydantic.Field(
                default_factory=containers.Mot3
            )

            mot3: containers.Mot3 = pydantic.Field(
                default_factory=containers.Mot3
            )

            enc4: containers.Enc4 = pydantic.Field(
                default_factory=containers.Enc4
            )

            dofint: containers.DOFInt = pydantic.Field(
                default_factory=containers.DOFInt
            )

            dofmotor: containers.DOFMotor = pydantic.Field(
                default_factory=containers.DOFMotor
            )

            doffloat: containers.DOFFloat = pydantic.Field(
                default_factory=containers.DOFFloat
            )

            mat3x3: containers.Mat3x3 = pydantic.Field(
                default_factory=containers.Mat3x3
            )

            mat6x6: containers.Mat6x6 = pydantic.Field(
                default_factory=containers.Mat6x6
            )

        data = Data()

        self.assertIsInstance(data.status, containers.Status)
        self.assertIsInstance(data.vec3, containers.Vector3)
        self.assertIsInstance(data.enc3, containers.Mot3)
        self.assertIsInstance(data.mot3, containers.Mot3)
        self.assertIsInstance(data.enc4, containers.Enc4)
        self.assertIsInstance(data.dofint, containers.DOFInt)
        self.assertIsInstance(data.dofmotor, containers.DOFMotor)
        self.assertIsInstance(data.doffloat, containers.DOFFloat)
        self.assertIsInstance(data.mat3x3, containers.Mat3x3)
        self.assertIsInstance(data.mat6x6, containers.Mat6x6)

        for status_elem1, status_elem2 in zip(
            data.status, containers.Status()
        ):
            self.assertEqual(status_elem1, status_elem2)  # type: ignore

        self.assertSequenceAlmostEqual(data.vec3, containers.Vector3())  # type: ignore
        self.assertSequenceEqual(data.enc3, containers.Mot3())  # type: ignore
        self.assertSequenceEqual(data.enc4, containers.Enc4())  # type: ignore
        self.assertSequenceEqual(data.dofint, containers.DOFInt())  # type: ignore
        self.assertSequenceEqual(data.dofmotor, containers.DOFMotor())  # type: ignore
        self.assertSequenceAlmostEqual(data.doffloat, containers.DOFFloat())  # type: ignore

        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(data.mat3x3[i, j], 0.0)

        for i in range(6):
            for j in range(6):
                self.assertAlmostEqual(data.mat6x6[i, j], 0.0)

        status = containers.Status(
            *tuple(bool(randint(0, 1)) for _ in range(MAX_STATUS))
        )
        enc3 = containers.Enc3(randint(0, 100) for _ in range(3))
        mot3 = containers.Mot3(randint(0, 100) for _ in range(3))
        enc4 = containers.Enc4(randint(0, 100) for _ in range(4))
        dofint = containers.DOFInt(randint(0, 100) for _ in range(MAX_DOF))
        dofmotor= containers.DOFMotor(randint(0, 100) for _ in range(MAX_DOF))
        doffloat = containers.DOFFloat(random() for _ in range(MAX_DOF))
        mat3x3 = containers.Mat3x3(random() for _ in range(3 * 3))
        mat6x6 = containers.Mat6x6(random() for _ in range(6 * 6))

        data = Data(
            status=status, enc3=enc3, mot3=mot3, enc4=enc4, dofint=dofint,
            dofmotor=dofmotor, doffloat=doffloat, mat3x3=mat3x3, mat6x6=mat6x6
        )

        data_dct = data.model_dump()
        self.assertIsInstance(data_dct['status'], dict)
        self.assertIsInstance(data_dct['vec3'], list)
        self.assertIsInstance(data_dct['enc3'], list)
        self.assertIsInstance(data_dct['mot3'], list)
        self.assertIsInstance(data_dct['enc4'], list)
        self.assertIsInstance(data_dct['dofint'], list)
        self.assertIsInstance(data_dct['dofmotor'], list)
        self.assertIsInstance(data_dct['doffloat'], list)
        self.assertIsInstance(data_dct['mat3x3'], list)
        self.assertIsInstance(data_dct['mat6x6'], list)

        for field_name in map(
            lambda field: field[0], data.status._fields_[:-1]
        ):
            self.assertEqual(
                getattr(data.status, field_name),
                data_dct['status'][field_name]
            )

        self.assertSequenceEqual(data_dct['vec3'], data.vec3)
        self.assertSequenceEqual(data_dct['enc3'], data.enc3)
        self.assertSequenceEqual(data_dct['mot3'], data.mot3)
        self.assertSequenceEqual(data_dct['enc4'], data.enc4)
        self.assertSequenceEqual(data_dct['dofint'], data.dofint)
        self.assertSequenceEqual(data_dct['dofmotor'], data.dofmotor)
        self.assertSequenceEqual(data_dct['doffloat'], data.doffloat)

        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(
                    data.mat3x3[i, j],
                    data_dct['mat3x3'][i][j]
                )

        for i in range(6):
            for j in range(6):
                self.assertAlmostEqual(
                    data.mat6x6[i, j],
                    data_dct['mat6x6'][i][j]
                )
