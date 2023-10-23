import unittest
from ctypes import c_int
from random import randint, random
from typing import Sequence

import forcedimension_core.containers as containers
from forcedimension_core.dhd.constants import MAX_DOF, MAX_STATUS


class TestContainers(unittest.TestCase):
    def testVersion(self):
        major = randint(0, 100)
        minor = randint(0, 100)
        release = randint(0, 100)
        revision = randint(0, 100)

        version = containers.VersionTuple(major, minor, release, revision)

        self.assertTupleEqual(version, (major, minor, release, revision))

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
            ValueError, lambda: containers.DOFMotorArray([0] * (MAX_DOF - 1))
        )
        self.assertRaises(
            ValueError, lambda: containers.DOFMotorArray([0] * (MAX_DOF + 1))
        )

        dofs = [randint(0, 100) for _ in range(MAX_DOF)]

        dof_mots = containers.DOFMotorArray(dofs)
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

    def testMat6x6(self):
        mat_data = [random() for _ in range(6 * 6 + 1)]

        self.assertRaises(
            ValueError, lambda: containers.Mat3x3(mat_data)
        )

        self.assertRaises(
            ValueError, lambda: containers.Mat3x3(mat_data[:35])
        )
        mat6x6 = containers.Mat6x6(mat_data[:36])

        for i in range(6):
            for j  in range(6):
                self.assertAlmostEqual(mat_data[6 * i + j], mat6x6[i, j])

                val = random()
                mat6x6[i, j] = val
                self.assertAlmostEqual(val, mat6x6[i, j])
