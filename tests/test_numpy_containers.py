import ctypes
import unittest
from random import randint, random

import pydantic
import numpy as np

import forcedimension_core.containers as containers
from forcedimension_core.constants import MAX_DOF, MAX_STATUS

class TestNumpyContainers(unittest.TestCase):
    def assertSequenceAlmostEqual(self, seq1, seq2):

        for elem1, elem2 in zip(seq1, seq2):
            self.assertAlmostEqual(elem1, elem2)

    def testVector3(self):
        x = random()
        y = random()
        z = random()

        self.assertRaises(ValueError, lambda: containers.numpy.Vector3((x, y, z, 0)))
        self.assertRaises(ValueError, lambda: containers.numpy.Vector3((x, y)))

        v = containers.numpy.Vector3((x, y, z))

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
            ValueError, lambda: containers.numpy.Enc3((enc0, enc1, enc2, 0))
        )
        self.assertRaises(
            ValueError, lambda: containers.numpy.Enc3((enc0, enc1))
        )

        enc = containers.numpy.Enc3((enc0, enc1, enc2))
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
            ValueError, lambda: containers.numpy.Mot3((mot0, mot1, mot2, 0))
        )
        self.assertRaises(
            ValueError, lambda: containers.numpy.Mot3((mot0, mot1))
        )

        mot = containers.numpy.Mot3((mot0, mot1, mot2))
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
            ValueError, lambda: containers.numpy.Enc4((enc0, enc1, enc2, enc3, 0))
        )
        self.assertRaises(
            ValueError, lambda: containers.numpy.Enc4((enc0, enc1, enc2))
        )

        enc = containers.numpy.Enc4((enc0, enc1, enc2, enc3))

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

    def testDOFIntArray(self):
        self.assertRaises(
            ValueError, lambda: containers.numpy.DOFInt([0] * (MAX_DOF - 1))
        )
        self.assertRaises(
            ValueError, lambda: containers.numpy.DOFInt([0] * (MAX_DOF + 1))
        )

        dofs = [randint(0, 100) for _ in range(MAX_DOF)]

        dof_ints = containers.numpy.DOFInt(dofs)
        self.assertEqual(MAX_DOF, len(dof_ints))
        self.assertTrue(np.shares_memory(dof_ints.delta, dof_ints[:3]))
        self.assertTrue(np.shares_memory(dof_ints.wrist, dof_ints[3:6]))
        self.assertTrue(np.shares_memory(dof_ints.wrist_grip, dof_ints[3:7]))
        self.assertEqual(
            ctypes.cast(
                ctypes.pointer(dof_ints.gripper), ctypes.c_void_p
            ).value,
            dof_ints[-1:].ctypes.data_as(ctypes.c_void_p).value
        )

        for i in range(MAX_DOF):
            self.assertEqual(dofs[i], dof_ints[i])
            self.assertEqual(dofs[i], dof_ints[i])

            dof_ints.ptr[i] = randint(0, 100)
            self.assertEqual(dof_ints.ptr[i], dof_ints[i])

    def testDOFMotorArray(self):
        self.assertRaises(
            ValueError, lambda: containers.numpy.DOFMotor([0] * (MAX_DOF - 1))
        )
        self.assertRaises(
            ValueError, lambda: containers.numpy.DOFMotor([0] * (MAX_DOF + 1))
        )

        dofs = [randint(0, 100) for _ in range(MAX_DOF)]

        dof_mots = containers.numpy.DOFMotor(dofs)
        self.assertEqual(MAX_DOF, len(dof_mots))

        for i in range(MAX_DOF):
            self.assertEqual(dofs[i], dof_mots[i])
            self.assertEqual(dofs[i], dof_mots[i])

            dof_mots.ptr[i] = randint(0, 100)
            self.assertEqual(dof_mots.ptr[i], dof_mots[i])

    def testDOFFloatArray(self):
        self.assertRaises(
            ValueError, lambda: containers.numpy.DOFFloat([0] * (MAX_DOF - 1))
        )
        self.assertRaises(
            ValueError, lambda: containers.numpy.DOFFloat([0] * (MAX_DOF + 1))
        )

        dofs = [random() for _ in range(MAX_DOF)]

        dof_floats = containers.numpy.DOFFloat(dofs)
        self.assertAlmostEqual(MAX_DOF, len(dof_floats))

        self.assertTrue(np.shares_memory(dof_floats.delta, dof_floats[:3]))
        self.assertTrue(np.shares_memory(dof_floats.wrist, dof_floats[3:6]))
        self.assertEqual(
            ctypes.cast(
                ctypes.pointer(dof_floats.gripper), ctypes.c_void_p
            ).value,
            dof_floats[-1:].ctypes.data_as(ctypes.c_void_p).value
        )

        for i in range(MAX_DOF):
            self.assertAlmostEqual(dofs[i], dof_floats[i])
            self.assertAlmostEqual(dofs[i], dof_floats[i])

            dof_floats.ptr[i] = random()
            self.assertEqual(dof_floats.ptr[i], dof_floats[i])

    def testMat3x3(self):
        mat_data = [random() for _ in range(3 * 3 + 1)]

        self.assertRaises(
            ValueError, lambda: containers.numpy.Mat3x3(mat_data)
        )

        self.assertRaises(
            ValueError, lambda: containers.numpy.Mat3x3(mat_data[:8])
        )

        mat3x3 = containers.numpy.Mat3x3(mat_data[:9])

        self.assertEqual(
            ctypes.cast(mat3x3.ptr, ctypes.c_void_p).value,
            mat3x3.ctypes.data_as(ctypes.c_void_p).value
        )

        for i in range(3):
            for j  in range(3):
                self.assertAlmostEqual(mat_data[3 * i + j], mat3x3[i, j])

                val = random()
                mat3x3[i, j] = val
                self.assertAlmostEqual(val, mat3x3[i, j])

        def getitemRaisesTypeErrorFirstIndex():
            mat3x3[0.0, 0]  # type: ignore

        def getitemRaisesTypeErrorSecondIndex():
            mat3x3[0, 0.0]  # type: ignore

        def setitemRaisesTypeErrorFirstIndex():
            mat3x3[0.0, 0] = 1  # type: ignore

        def setitemRaisesTypeErrorSecondIndex():
            mat3x3[0, 0.0] = 1  # type: ignore

        self.assertRaises(IndexError, getitemRaisesTypeErrorFirstIndex)
        self.assertRaises(IndexError, getitemRaisesTypeErrorSecondIndex)

        self.assertRaises(IndexError, setitemRaisesTypeErrorFirstIndex)
        self.assertRaises(IndexError, setitemRaisesTypeErrorSecondIndex)

    def testMat6x6(self):
        mat_data = [random() for _ in range(6 * 6 + 1)]

        self.assertRaises(
            ValueError, lambda: containers.numpy.Mat6x6(mat_data)
        )

        self.assertRaises(
            ValueError, lambda: containers.numpy.Mat6x6(mat_data[:35])
        )
        mat6x6 = containers.numpy.Mat6x6(mat_data[:36])

        self.assertEqual(
            ctypes.cast(mat6x6.ptr, ctypes.c_void_p).value,
            mat6x6.ctypes.data_as(ctypes.c_void_p).value
        )

        for i in range(6):
            for j  in range(6):
                self.assertAlmostEqual(mat_data[6 * i + j], mat6x6[i, j])

                val = random()
                mat6x6[i, j] = val
                self.assertAlmostEqual(val, mat6x6[i, j])


        def getitemRaisesTypeErrorFirstIndex():
            mat6x6[0.0, 0]  # type: ignore

        def getitemRaisesTypeErrorSecondIndex():
            mat6x6[0, 0.0]  # type: ignore

        def setitemRaisesTypeErrorFirstIndex():
            mat6x6[0.0, 0] = 1  # type: ignore

        def setitemRaisesTypeErrorSecondIndex():
            mat6x6[0, 0.0] = 1  # type: ignore

        self.assertRaises(IndexError, getitemRaisesTypeErrorFirstIndex)
        self.assertRaises(IndexError, getitemRaisesTypeErrorSecondIndex)

        self.assertRaises(IndexError, setitemRaisesTypeErrorFirstIndex)
        self.assertRaises(IndexError, setitemRaisesTypeErrorSecondIndex)

    def testSerialization(self):

        class Data(pydantic.BaseModel):
            vec3: containers.numpy.Vector3 = pydantic.Field(
                default_factory=containers.numpy.Vector3
            )

            enc3: containers.numpy.Enc3 = pydantic.Field(
                default_factory=containers.numpy.Mot3
            )

            mot3: containers.numpy.Mot3 = pydantic.Field(
                default_factory=containers.numpy.Mot3
            )

            enc4: containers.numpy.Enc4 = pydantic.Field(
                default_factory=containers.numpy.Enc4
            )

            dofint: containers.numpy.DOFInt = pydantic.Field(
                default_factory=containers.numpy.DOFInt
            )

            dofmotor: containers.numpy.DOFMotor = pydantic.Field(
                default_factory=containers.numpy.DOFMotor
            )

            doffloat: containers.numpy.DOFFloat = pydantic.Field(
                default_factory=containers.numpy.DOFFloat
            )

            mat3x3: containers.numpy.Mat3x3 = pydantic.Field(
                default_factory=containers.numpy.Mat3x3
            )

            mat6x6: containers.numpy.Mat6x6 = pydantic.Field(
                default_factory=containers.numpy.Mat6x6
            )

        data = Data()

        self.assertIsInstance(data.vec3, containers.numpy.Vector3)
        self.assertIsInstance(data.enc3, containers.numpy.Mot3)
        self.assertIsInstance(data.mot3, containers.numpy.Mot3)
        self.assertIsInstance(data.enc4, containers.numpy.Enc4)
        self.assertIsInstance(data.dofint, containers.numpy.DOFInt)
        self.assertIsInstance(data.dofmotor, containers.numpy.DOFMotor)
        self.assertIsInstance(data.doffloat, containers.numpy.DOFFloat)
        self.assertIsInstance(data.mat3x3, containers.numpy.Mat3x3)
        self.assertIsInstance(data.mat6x6, containers.numpy.Mat6x6)

        self.assertTrue(np.allclose(data.vec3, containers.numpy.Vector3()))  # type: ignore
        self.assertTrue(np.array_equal(data.enc3, containers.numpy.Mot3()))  # type: ignore
        self.assertTrue(np.array_equal(data.enc4, containers.numpy.Enc4()))  # type: ignore
        self.assertTrue(np.array_equal(data.dofint, containers.numpy.DOFInt()))  # type: ignore
        self.assertTrue(np.array_equal(data.dofmotor, containers.numpy.DOFMotor()))  # type: ignore
        self.assertTrue(np.allclose(data.doffloat, containers.numpy.DOFFloat()))  # type: ignore
        self.assertTrue(np.allclose(data.mat3x3, containers.numpy.Mat3x3()))  # type: ignore
        self.assertTrue(np.allclose(data.mat6x6, containers.numpy.Mat6x6()))  # type: ignore

        enc3 = containers.numpy.Enc3(tuple(randint(0, 100) for _ in range(3)))
        mot3 = containers.numpy.Mot3(tuple(randint(0, 100) for _ in range(3)))
        enc4 = containers.numpy.Enc4(tuple(randint(0, 100) for _ in range(4)))
        dofint = containers.numpy.DOFInt(tuple(randint(0, 100) for _ in range(MAX_DOF)))
        dofmotor= containers.numpy.DOFMotor(tuple(randint(0, 100) for _ in range(MAX_DOF)))
        doffloat = containers.numpy.DOFFloat(tuple(random() for _ in range(MAX_DOF)))
        mat3x3 = containers.numpy.Mat3x3(tuple(random() for _ in range(3 * 3)))
        mat6x6 = containers.numpy.Mat6x6(tuple(random() for _ in range(6 * 6)))

        data = Data(
            enc3=enc3, mot3=mot3, enc4=enc4, dofint=dofint,
            dofmotor=dofmotor, doffloat=doffloat, mat3x3=mat3x3, mat6x6=mat6x6
        )

        data_dct = data.model_dump()
        self.assertIsInstance(data_dct['vec3'], list)
        self.assertIsInstance(data_dct['enc3'], list)
        self.assertIsInstance(data_dct['mot3'], list)
        self.assertIsInstance(data_dct['enc4'], list)
        self.assertIsInstance(data_dct['dofint'], list)
        self.assertIsInstance(data_dct['dofmotor'], list)
        self.assertIsInstance(data_dct['doffloat'], list)
        self.assertIsInstance(data_dct['mat3x3'], list)
        self.assertIsInstance(data_dct['mat6x6'], list)

        self.assertTrue(np.allclose(data_dct['vec3'], data.vec3))
        self.assertTrue(np.array_equal(data_dct['enc3'], data.enc3))  # type: ignore
        self.assertTrue(np.array_equal(data_dct['mot3'], data.mot3))  # type: ignore
        self.assertTrue(np.array_equal(data_dct['enc4'], data.enc4))  # type: ignore
        self.assertTrue(np.array_equal(data_dct['dofint'], data.dofint))  # type: ignore
        self.assertTrue(np.array_equal(data_dct['dofmotor'], data.dofmotor)) # type: ignore
        self.assertTrue(np.allclose(data_dct['doffloat'], data.doffloat))

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
