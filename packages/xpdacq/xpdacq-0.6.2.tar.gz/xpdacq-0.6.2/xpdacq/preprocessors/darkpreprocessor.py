import typing as T

import bluesky.plan_stubs as bps
from bluesky import Msg
from bluesky_darkframes import DarkFramePreprocessor, SnapshotDevice
from ophyd import Device
from ophyd.signal import Signal
from xpdacq.preprocessors.shutterconfig import ShutterConfig

Plan = T.Generator[Msg, T.Any, T.Any]
ShutterControl = T.Callable[[], Plan]


class DarkPreprocessor(DarkFramePreprocessor):
    """A plan preprocessor that ensures each Run records a dark frame.

    Specifically this adds a new Event stream, named ‘dark’ by default. It inserts one Event with a reading
    that contains a ‘dark’ frame. The same reading may be used across multiple runs, depending on the rules
    for when a dark frame is taken.

    Parameters
    ----------
    detector: Device
        The detector to take dark frame of.
    max_age: float
        Time after which a fresh dark frame should be acquired
    locked_signals: Iterable, optional
        Any changes to these signals invalidate the current dark frame and
        prompt us to take a new one. Typical examples would be exposure time or
        gain, anything that changes the expected dark frame.
    limit: integer or None, optional
        Number of dark frames to cache. If None, do not limit.
    stream_name: string, optional
        Event stream name for dark frames. Default is 'dark'.
    delay : float
        The time to wait between the moment that the shutter is closed and the moment to trigger the detector
        to take dark. Used to wait for the saturation to be cleaned.
    open_shutter : Any
        The function used by run engine to open the shutter. The syntax should be like

        ```
        def open_shutter() -> Any:
            return (yield from bps.mv(shutter, 'open')
        ```

        Default is the `xpdacq.beamtime.open_shutter_stub`.
    close_shutter : Any
        The function used by run engine to close the shutter. The syntax should be like

        ```
        def open_shutter() -> Any:
            return (yield from bps.mv(shutter, 'closed')
        ```

        Default is the `xpdacq.beamtime.close_shutter_stub`
    """

    def __init__(
        self,
        *,
        detector: Device,
        max_age: float = 0.,
        locked_signals: T.Optional[T.Iterable[Signal]] = None,
        limit: T.Optional[int] = None,
        stream_name='dark',
        shutter_config: ShutterConfig = None
    ):
        if shutter_config is None:
            shutter_config = ShutterConfig.from_xpdacq()
        self._shutter_config = shutter_config

        def _dark_plan(_detector):
            shutter = self._shutter_config.shutter
            open_state = self._shutter_config.open_state
            close_state = self._shutter_config.close_state
            delay = self._shutter_config.delay
            yield from bps.mv(shutter, close_state)
            if delay > 0.:
                yield from bps.sleep(delay)
            yield from bps.unstage(_detector)
            yield from bps.stage(_detector)
            yield from bps.trigger(_detector, group='bluesky-darkframes-trigger')
            yield from bps.wait('bluesky-darkframes-trigger')
            snapshot = SnapshotDevice(_detector)
            yield from bps.unstage(_detector)
            yield from bps.stage(_detector)
            yield from bps.mv(shutter, open_state)
            return snapshot

        super().__init__(
            dark_plan=_dark_plan,
            detector=detector,
            max_age=max_age,
            locked_signals=locked_signals,
            limit=limit,
            stream_name=stream_name
        )
