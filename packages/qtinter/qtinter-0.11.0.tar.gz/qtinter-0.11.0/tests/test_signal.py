import asyncio
import qtinter
import unittest
from shim import QtCore, Signal, exec_qt_loop


class SenderObject(QtCore.QObject):
    signal0 = Signal()
    signal1 = Signal(object)
    signal2 = Signal(str, object)


class TestSignal(unittest.TestCase):

    def setUp(self) -> None:
        if QtCore.QCoreApplication.instance() is not None:
            self.app = QtCore.QCoreApplication.instance()
        else:
            self.app = QtCore.QCoreApplication([])

    def tearDown(self) -> None:
        self.app = None

    def test_builtin_signal(self):
        # Test asyncsignal() with built-in signal QTimer.timeout
        timer = QtCore.QTimer()
        timer.setInterval(100)
        timer.start()

        async def coro():
            await qtinter.asyncsignal(timer.timeout)
            return 123

        with qtinter.using_qt_from_asyncio():
            self.assertEqual(asyncio.run(coro()), 123)

    def test_signal_with_no_argument(self):
        sender = SenderObject()

        async def coro():
            asyncio.get_running_loop().call_soon(sender.signal0.emit)
            return await qtinter.asyncsignal(sender.signal0)

        with qtinter.using_qt_from_asyncio():
            self.assertEqual(asyncio.run(coro()), ())

    def test_signal_with_one_argument(self):
        sender = SenderObject()
        arg = object()

        async def coro():
            asyncio.get_running_loop().call_soon(sender.signal1.emit, arg)
            return await qtinter.asyncsignal(sender.signal1)

        with qtinter.using_qt_from_asyncio():
            self.assertEqual(asyncio.run(coro()), (arg,))

    def test_signal_with_two_arguments(self):
        sender = SenderObject()

        async def coro():
            asyncio.get_running_loop().call_soon(
                sender.signal2.emit, "Hello", (1.5, "metre"))
            return await qtinter.asyncsignal(sender.signal2)

        with qtinter.using_qt_from_asyncio():
            self.assertEqual(asyncio.run(coro()), ("Hello", (1.5, "metre")))

    def test_cancellation(self):
        # asyncsignal should be able to be cancelled
        timer = QtCore.QTimer()
        timer.setInterval(0)

        async def coro():
            await qtinter.asyncsignal(timer.timeout)

        async def main():
            task = asyncio.create_task(coro())
            await asyncio.sleep(0)
            task.cancel()
            timer.start()
            await task

        with qtinter.using_qt_from_asyncio():
            with self.assertRaises(asyncio.CancelledError):
                asyncio.run(main())

    def test_sender_gone(self):
        # If the sender is garbage collected, asyncsignal should hang forever.
        timer = QtCore.QTimer()
        timer.setInterval(100)
        timer.start()

        def delete_timer():
            nonlocal timer
            timer = None

        async def coro():
            asyncio.get_running_loop().call_soon(delete_timer)
            await qtinter.asyncsignal(timer.timeout)

        with qtinter.using_qt_from_asyncio():
            with self.assertRaises(asyncio.TimeoutError):
                asyncio.run(asyncio.wait_for(coro(), 0.5))

    def test_destroyed(self):
        # Should be able to catch destroyed signal
        timer = QtCore.QTimer()
        timer.setInterval(100)
        timer.start()

        def delete_timer():
            nonlocal timer
            timer = None

        async def coro():
            asyncio.get_running_loop().call_soon(delete_timer)
            await qtinter.asyncsignal(timer.destroyed)
            return 123

        with qtinter.using_qt_from_asyncio():
            self.assertEqual(asyncio.run(coro()), 123)

    def test_copy_args(self):
        # asyncsignal must copy the signal arguments, because some arguments
        # are temporary objects that go out of scope when the slot returns.
        # If not copied, SIGSEGV will be raised.
        from qtinter.bindings import QtPositioning

        source = QtPositioning.QGeoPositionInfoSource.createDefaultSource(
            self.app)

        async def emit():
            # Emit signal from a different thread to make Qt send a temporary
            # copy of the argument via queued connection.
            await asyncio.get_running_loop().run_in_executor(
                None,
                source.positionUpdated.emit,
                QtPositioning.QGeoPositionInfo())

        async def coro():
            asyncio.get_running_loop().call_soon(asyncio.create_task, emit())
            position: QtPositioning.QGeoPositionInfo = \
                (await qtinter.asyncsignal(source.positionUpdated))[0]
            return position.coordinate().toString()

        with qtinter.using_qt_from_asyncio():
            self.assertEqual(asyncio.run(coro()), "")


class TestAsyncSignalStream(unittest.TestCase):
    def setUp(self):
        if QtCore.QCoreApplication.instance() is not None:
            self.app = QtCore.QCoreApplication.instance()
        else:
            self.app = QtCore.QCoreApplication([])

    def tearDown(self):
        self.app = None

    def test_timer(self):
        timer = QtCore.QTimer()
        timer.setInterval(100)
        timer.start()

        async def coro():
            n = 0
            async for _ in qtinter.asyncsignalstream(timer.timeout):
                n += 1
                if n == 10:
                    break

        import time
        t1 = time.time()
        with qtinter.using_qt_from_asyncio():
            asyncio.run(coro())
        t2 = time.time()

        self.assertTrue(0.9 < t2 - t1 < 1.5, t2 - t1)


class TestMultiSignal(unittest.TestCase):
    def setUp(self):
        if QtCore.QCoreApplication.instance() is not None:
            self.app = QtCore.QCoreApplication.instance()
        else:
            self.app = QtCore.QCoreApplication([])

    def tearDown(self):
        self.app = None

    def test_empty_map(self):
        # Passing an empty signal map is a no-op
        ms = qtinter.multisignal(dict())
        ms.connect(lambda: None)

    def test_multiple_senders(self):
        # Test multisignal usage with multiple senders.

        timer1 = QtCore.QTimer()
        timer1.setInterval(100)
        timer1.start()

        timer2 = QtCore.QTimer()
        timer2.setInterval(250)
        timer2.start()

        ms = qtinter.multisignal({timer1.timeout: 'A', timer2.timeout: 4})
        result = []
        ms.connect(lambda s, a: result.append((s, a)))

        qt_loop = QtCore.QEventLoop()
        timer2.timeout.connect(qt_loop.quit)
        exec_qt_loop(qt_loop)

        self.assertEqual(result, [('A', ()), ('A', ()), (4, ())])


if __name__ == "__main__":
    unittest.main()
