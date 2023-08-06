import bluesky.plan_stubs as bps
import bluesky.plans as bp
import bluesky.preprocessors as bpp
from bluesky.run_engine import RunEngine
from databroker.v2 import temp
from frozendict import frozendict
from ophyd.sim import hw
from pkg_resources import resource_filename
from xarray import Dataset
from xpdacq.preprocessors.calibpreprocessor import CalibInfo, CalibPreprocessor

PONI_FILE = str(resource_filename("xpdacq", "tests/Ni_poni_file.poni"))


def test_set():
    ci = CalibInfo(name="calib_info")
    calib_result = (1.0, 200.0, 1000.0, 1500.0, 0.1, 0.2, 0.3, "Perkin detector")
    sts = ci.set(calib_result)
    assert sts is not None
    # check if the signals are set correctly
    assert ci.wavelength.get() == calib_result[0]
    assert ci.dist.get() == calib_result[1]
    assert ci.poni1.get() == calib_result[2]
    assert ci.poni2.get() == calib_result[3]
    assert ci.rot1.get() == calib_result[4]
    assert ci.rot2.get() == calib_result[5]
    assert ci.rot3.get() == calib_result[6]
    assert ci.detector.get() == calib_result[7]


def test_preprocessor_usage():
    devices = hw()
    det = devices.det
    det_z = devices.motor
    cp = CalibPreprocessor(det, locked_signals=[det_z])
    db = temp()
    RE = RunEngine()
    RE.subscribe(db.v1.insert)

    def simple_count():
        return cp(bp.count([det]))

    # case 1: no cache, no calib
    plan1 = simple_count()
    RE(plan1)
    assert not hasattr(db[-1], "calib")
    # add cache
    pos1 = 1.0
    calib_result1 = (1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, "Perkin detector")
    cp.add_calib_result({det_z.name: pos1}, calib_result1)
    pos2 = 2.0
    calib_result2 = (1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, "Perkin detector")
    cp.add_calib_result({det_z.name: pos2}, calib_result2)
    pos3 = 3.0
    # case 2: state in cache, use corresponding calib result
    plan2 = bpp.pchain(bps.mv(det_z, pos1), simple_count())
    RE(plan2)
    attrs = ("wavelength", "dist", "poni1", "poni2", "rot1", "rot2", "rot3", "detector")
    calib_data: Dataset = db[-1].calib.read()
    for i in range(len(attrs)):
        key = "{}_{}".format(det.name, attrs[i])
        assert calib_data[key].item() == calib_result1[i]
    # case 3: state not in cache, use latest calib result
    plan3 = bpp.pchain(bps.mv(det_z, pos3), simple_count())
    RE(plan3)
    calib_data: Dataset = db[-1].calib.read()
    for i in range(len(attrs)):
        key = "{}_{}".format(det.name, attrs[i])
        assert calib_data[key].item() == calib_result2[i]


def test_read_and_record():
    devices = hw()
    det = devices.det
    det_z = devices.motor
    cp = CalibPreprocessor(det, locked_signals=[det_z])
    calib_result = cp.read(PONI_FILE)
    RE = RunEngine()
    pos = 1.0
    plan = bpp.pchain(bps.mv(det_z, pos), cp.record(calib_result))
    RE(plan)
    assert cp._cache[frozendict({det_z.name: pos})] == calib_result


def test_disable_and_enable():
    devices = hw()
    det = devices.det
    cp = CalibPreprocessor(det)
    calib_result = (1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, "Perkin detector")
    cp.add_calib_result(dict(), calib_result)

    def plan1():
        return bps.trigger_and_read([det])

    def plan2():
        return cp(plan1())

    def get_steps(plan):
        count = 0
        for _ in plan:
            count += 1
        return count

    cp.disable()
    assert get_steps(plan1()) == get_steps(plan2())
    cp.enable()
    assert get_steps(plan1()) < get_steps(plan2())


def test_repr():
    devices = hw()
    det = devices.det
    cp = CalibPreprocessor(det)
    assert cp.__repr__() == "<CalibPreprocessor of det with 0 cache>"
